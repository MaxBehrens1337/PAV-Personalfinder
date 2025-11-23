.PHONY: help setup start stop restart logs status health seed clean reset ollama-status frontend-logs backend-logs db-backup

# Default target
help:
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║          PAV Personalfinder - Makefile Commands           ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "🚀 Setup & Start:"
	@echo "  make setup           - Komplettes automatisches Setup (empfohlen für Erstinstallation)"
	@echo "  make start           - Starte alle Services"
	@echo "  make stop            - Stoppe alle Services"
	@echo "  make restart         - Neustart aller Services"
	@echo ""
	@echo "📊 Monitoring & Logs:"
	@echo "  make logs            - Zeige Logs aller Services"
	@echo "  make status          - Zeige Status aller Services"
	@echo "  make health          - Führe Gesundheits-Check durch"
	@echo "  make frontend-logs   - Nur Frontend-Logs"
	@echo "  make backend-logs    - Nur Backend-Logs"
	@echo "  make ollama-status   - Prüfe Ollama/LLM Status"
	@echo ""
	@echo "💾 Daten & Verwaltung:"
	@echo "  make seed            - Lade Demo-Daten"
	@echo "  make db-backup       - Erstelle Datenbank-Backup"
	@echo "  make clean           - Stoppe Services und entferne Container"
	@echo "  make reset           - Vollständiger Reset (ACHTUNG: Löscht alle Daten!)"
	@echo ""
	@echo "🛠️  Entwicklung:"
	@echo "  make shell-backend   - Öffne Shell im Backend-Container"
	@echo "  make shell-frontend  - Öffne Shell im Frontend-Container"
	@echo "  make shell-db        - Öffne PostgreSQL-Shell"
	@echo ""

# Complete automated setup
setup:
	@echo "Starting automated setup..."
	@bash setup.sh

# Start all services
start:
	@echo "🚀 Starting PAV Personalfinder..."
	@docker-compose up -d
	@echo "✓ Services started!"
	@echo ""
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "Use 'make logs' to see logs"
	@echo "Use 'make health' to check health"

# Stop all services
stop:
	@echo "⏸️  Stopping all services..."
	@docker-compose down
	@echo "✓ Services stopped!"

# Restart all services
restart:
	@echo "🔄 Restarting all services..."
	@docker-compose restart
	@echo "✓ Services restarted!"

# Show logs from all services
logs:
	@docker-compose logs -f

# Show status of all services
status:
	@echo "📊 Service Status:"
	@echo ""
	@docker-compose ps
	@echo ""
	@echo "💡 Use 'make logs' to see detailed logs"

# Health check
health:
	@echo "🏥 Running health checks..."
	@echo ""
	@bash scripts/health-check.sh || echo "⚠️  health-check.sh not found - creating it..."

# Load seed data
seed:
	@echo "💾 Loading demo data..."
	@docker-compose exec backend python ../scripts/seed_data.py
	@echo "✓ Demo data loaded!"
	@echo ""
	@echo "You can now login with:"
	@echo "  admin / admin123"
	@echo "  hr_manager / hr123"
	@echo "  viewer / viewer123"

# Clean up (stop and remove containers)
clean:
	@echo "🧹 Cleaning up..."
	@docker-compose down -v
	@echo "✓ Cleanup complete!"

# Complete reset (WARNING: deletes all data!)
reset:
	@echo "⚠️  WARNING: This will delete ALL data including database volumes!"
	@read -p "Are you sure? Type 'yes' to continue: " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		echo "Resetting..."; \
		docker-compose down -v; \
		rm -f .env; \
		echo "✓ Reset complete! Run 'make setup' to start fresh."; \
	else \
		echo "Cancelled."; \
	fi

# Check Ollama status
ollama-status:
	@echo "🤖 Ollama/LLM Status:"
	@echo ""
	@echo "Checking if Ollama is running..."
	@curl -s http://localhost:11434/api/tags 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "⚠️  Ollama is not responding yet"
	@echo ""
	@echo "Ollama logs (last 20 lines):"
	@docker-compose logs --tail=20 ollama

# Frontend logs only
frontend-logs:
	@docker-compose logs -f frontend

# Backend logs only
backend-logs:
	@docker-compose logs -f backend

# Database backup
db-backup:
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	@docker-compose exec -T db pg_dump -U pav_user pav_personalfinder > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✓ Backup created in backups/"
	@ls -lh backups/ | tail -1

# Shell access
shell-backend:
	@docker-compose exec backend bash

shell-frontend:
	@docker-compose exec frontend sh

shell-db:
	@docker-compose exec db psql -U pav_user -d pav_personalfinder

# Re-index employees in Qdrant (requires authentication token)
reindex:
	@echo "🔄 Re-indexing employees in Qdrant..."
	@echo "Note: You need an admin token for this operation"
	@echo "Get token by logging in at http://localhost:3000"
	@read -p "Enter your JWT token: " token; \
	curl -X POST http://localhost:8000/api/ai-match/reindex \
		-H "Authorization: Bearer $$token" \
		-H "Content-Type: application/json"
