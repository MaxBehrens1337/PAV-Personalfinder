"""
AI Matching Service
Core service for AI-powered employee matching using Ollama + Qdrant
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.config import settings
from app.models.mitarbeiter import Mitarbeiter, MitarbeiterStatus
from app.schemas.ai_matching import AIMatchRequest, AIMatchResponse, AIMatchResult


class AIMatchingService:
    """Service for AI-powered employee matching"""

    def __init__(self):
        self.embedding_model = None
        self.qdrant_client = None
        self.ollama_client = None
        self._initialized = False

    def initialize(self):
        """Initialize AI services (lazy loading)"""
        if self._initialized:
            return

        try:
            # Initialize embedding model
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

            # Initialize Qdrant client
            self.qdrant_client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )

            # Create collection if not exists
            self._ensure_collection_exists()

            # Initialize Ollama client
            self.ollama_client = ollama.Client(host=settings.OLLAMA_HOST)

            self._initialized = True
            print("✅ AI Matching Service initialized successfully")

        except Exception as e:
            print(f"⚠️  AI Matching Service initialization failed: {e}")
            print("    Falling back to classical search mode")
            self._initialized = False

    def _ensure_collection_exists(self):
        """Ensure Qdrant collection exists"""
        collections = self.qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if settings.QDRANT_COLLECTION_NAME not in collection_names:
            self.qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Created Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")

    def index_mitarbeiter(self, db: Session, mitarbeiter_id: int):
        """
        Index a single employee in Qdrant

        Args:
            db: Database session
            mitarbeiter_id: Employee ID to index
        """
        if not self._initialized:
            return

        try:
            mitarbeiter = db.query(Mitarbeiter).filter(Mitarbeiter.id == mitarbeiter_id).first()
            if not mitarbeiter:
                return

            # Create text representation
            qualifikationen = [mq.qualifikation.name for mq in mitarbeiter.qualifikationen]
            combined_text = f"{mitarbeiter.full_name}, {mitarbeiter.abteilung}, {mitarbeiter.position}. Skills: {', '.join(qualifikationen)}"

            # Generate embedding
            embedding = self.embedding_model.encode(combined_text).tolist()

            # Create payload
            payload = {
                "mitarbeiter_id": mitarbeiter.id,
                "personal_nummer": mitarbeiter.personal_nummer,
                "name": mitarbeiter.full_name,
                "abteilung": mitarbeiter.abteilung,
                "position": mitarbeiter.position,
                "status": mitarbeiter.status.value,
                "qualifikationen": qualifikationen,
                "combined_text": combined_text
            }

            # Upsert to Qdrant
            self.qdrant_client.upsert(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=mitarbeiter.id,
                        vector=embedding,
                        payload=payload
                    )
                ]
            )

        except Exception as e:
            print(f"Error indexing employee {mitarbeiter_id}: {e}")

    def index_all_mitarbeiter(self, db: Session):
        """
        Index all employees in Qdrant

        Args:
            db: Database session
        """
        if not self._initialized:
            self.initialize()

        if not self._initialized:
            return

        try:
            mitarbeiter_list = db.query(Mitarbeiter).all()
            print(f"Indexing {len(mitarbeiter_list)} employees...")

            for mitarbeiter in mitarbeiter_list:
                self.index_mitarbeiter(db, mitarbeiter.id)

            print(f"✅ Indexed {len(mitarbeiter_list)} employees successfully")

        except Exception as e:
            print(f"Error indexing employees: {e}")

    async def match_employees(self, request: AIMatchRequest, db: Session) -> AIMatchResponse:
        """
        Match employees based on AI-powered analysis

        Args:
            request: Match request with query and filters
            db: Database session

        Returns:
            AIMatchResponse with ranked results
        """
        start_time = time.time()

        # Initialize if needed
        if not self._initialized:
            self.initialize()

        # Fall back to classical search if AI not available
        if not self._initialized or not request.use_ai:
            return await self._classical_search(request, db, start_time)

        try:
            # Step 1: Generate embedding for query
            query_embedding = self.embedding_model.encode(request.query).tolist()

            # Step 2: Search in Qdrant for top candidates
            search_results = self.qdrant_client.search(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                query_vector=query_embedding,
                limit=min(request.max_results * 2, 50),  # Get more candidates for LLM to evaluate
                score_threshold=0.3  # Only consider reasonably similar results
            )

            # Step 3: Use Ollama LLM to evaluate and rank candidates
            matches = []
            for result in search_results[:request.max_results]:
                match = await self._evaluate_candidate_with_llm(
                    query=request.query,
                    candidate_payload=result.payload,
                    similarity_score=result.score,
                    db=db
                )
                if match:
                    matches.append(match)

            execution_time = time.time() - start_time

            return AIMatchResponse(
                query=request.query,
                total_matches=len(matches),
                ai_enabled=True,
                matches=matches,
                execution_time_seconds=round(execution_time, 2),
                timestamp=datetime.now()
            )

        except Exception as e:
            print(f"Error in AI matching: {e}")
            # Fall back to classical search
            return await self._classical_search(request, db, start_time)

    async def _evaluate_candidate_with_llm(
        self,
        query: str,
        candidate_payload: Dict[str, Any],
        similarity_score: float,
        db: Session
    ) -> Optional[AIMatchResult]:
        """
        Evaluate a candidate using Ollama LLM

        Args:
            query: User query
            candidate_payload: Candidate data from Qdrant
            similarity_score: Vector similarity score
            db: Database session

        Returns:
            AIMatchResult or None if evaluation fails
        """
        try:
            # Get full employee data
            mitarbeiter = db.query(Mitarbeiter).filter(
                Mitarbeiter.id == candidate_payload["mitarbeiter_id"]
            ).first()

            if not mitarbeiter:
                return None

            # Create prompt for LLM
            qualifikationen_details = []
            for mq in mitarbeiter.qualifikationen:
                qualifikationen_details.append(
                    f"- {mq.qualifikation.name} ({mq.level.value})"
                )

            prompt = f"""Analyze this employee match for the given requirement.

Requirement: {query}

Employee:
- Name: {mitarbeiter.full_name}
- Department: {mitarbeiter.abteilung}
- Position: {mitarbeiter.position}
- Status: {mitarbeiter.status.value}
- Qualifications:
{chr(10).join(qualifikationen_details) if qualifikationen_details else '  None listed'}

Task: Evaluate this match and provide:
1. Match score (0-100%)
2. Brief reasoning (1-2 sentences)
3. Key strengths (2-3 bullet points)
4. Potential gaps (1-2 bullet points, if any)

Respond in JSON format:
{{
  "match_score": <number 0-100>,
  "reasoning": "<brief explanation>",
  "strengths": ["<strength1>", "<strength2>"],
  "gaps": ["<gap1>"] or null
}}"""

            # Call Ollama
            response = self.ollama_client.generate(
                model=settings.OLLAMA_MODEL,
                prompt=prompt,
                options={
                    "temperature": 0.3,
                    "num_predict": 300,
                }
            )

            # Parse LLM response
            response_text = response['response'].strip()

            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            llm_eval = json.loads(response_text)

            # Create match result
            return AIMatchResult(
                mitarbeiter_id=mitarbeiter.id,
                personal_nummer=mitarbeiter.personal_nummer,
                full_name=mitarbeiter.full_name,
                abteilung=mitarbeiter.abteilung,
                position=mitarbeiter.position,
                email=mitarbeiter.email,
                status=mitarbeiter.status.value,
                match_score=float(llm_eval.get("match_score", similarity_score * 100)),
                reasoning=llm_eval.get("reasoning", "Good potential match based on profile"),
                strengths=llm_eval.get("strengths", []),
                gaps=llm_eval.get("gaps"),
                qualifikationen=candidate_payload.get("qualifikationen", [])
            )

        except Exception as e:
            print(f"Error evaluating candidate with LLM: {e}")
            # Return basic match without LLM evaluation
            return AIMatchResult(
                mitarbeiter_id=candidate_payload["mitarbeiter_id"],
                personal_nummer=candidate_payload["personal_nummer"],
                full_name=candidate_payload["name"],
                abteilung=candidate_payload["abteilung"],
                position=candidate_payload["position"],
                email="",
                status=candidate_payload["status"],
                match_score=similarity_score * 100,
                reasoning="Match based on semantic similarity",
                strengths=["Profile matches search criteria"],
                gaps=None,
                qualifikationen=candidate_payload.get("qualifikationen", [])
            )

    async def _classical_search(
        self,
        request: AIMatchRequest,
        db: Session,
        start_time: float
    ) -> AIMatchResponse:
        """
        Fallback classical search when AI is not available

        Args:
            request: Match request
            db: Database session
            start_time: Start time for execution tracking

        Returns:
            AIMatchResponse with classical search results
        """
        query = db.query(Mitarbeiter)

        # Apply filters
        if request.filters:
            if "abteilung" in request.filters:
                query = query.filter(Mitarbeiter.abteilung == request.filters["abteilung"])
            if "status" in request.filters:
                query = query.filter(Mitarbeiter.status == request.filters["status"])

        # Simple text search on name, abteilung, position
        search_term = f"%{request.query}%"
        query = query.filter(
            (Mitarbeiter.vorname.ilike(search_term)) |
            (Mitarbeiter.nachname.ilike(search_term)) |
            (Mitarbeiter.abteilung.ilike(search_term)) |
            (Mitarbeiter.position.ilike(search_term))
        )

        mitarbeiter_list = query.limit(request.max_results).all()

        # Convert to match results
        matches = []
        for mitarbeiter in mitarbeiter_list:
            qualifikationen = [mq.qualifikation.name for mq in mitarbeiter.qualifikationen]
            matches.append(
                AIMatchResult(
                    mitarbeiter_id=mitarbeiter.id,
                    personal_nummer=mitarbeiter.personal_nummer,
                    full_name=mitarbeiter.full_name,
                    abteilung=mitarbeiter.abteilung,
                    position=mitarbeiter.position,
                    email=mitarbeiter.email,
                    status=mitarbeiter.status.value,
                    match_score=75.0,  # Default score for classical search
                    reasoning="Match based on text search",
                    strengths=["Profile matches search terms"],
                    gaps=None,
                    qualifikationen=qualifikationen
                )
            )

        execution_time = time.time() - start_time

        return AIMatchResponse(
            query=request.query,
            total_matches=len(matches),
            ai_enabled=False,
            matches=matches,
            execution_time_seconds=round(execution_time, 2),
            timestamp=datetime.now()
        )


# Global instance
ai_matching_service = AIMatchingService()
