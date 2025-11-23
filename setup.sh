#!/bin/bash

# PAV Personalfinder - Automatisches Setup-Script
# Dieses Script führt alle notwendigen Schritte für Sie aus!

set -e  # Exit on error

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║              PAV Personalfinder Setup                      ║"
echo "║                                                            ║"
echo "║  Automatisches Setup für KI-gestütztes Mitarbeiter-Matching║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Check if Docker is installed
echo -e "${YELLOW}[1/8] Prüfe Docker-Installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker ist nicht installiert!${NC}"
    echo "Bitte installieren Sie Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker gefunden: $(docker --version)${NC}\n"

# Check if Docker Compose is installed
echo -e "${YELLOW}[2/8] Prüfe Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose ist nicht installiert!${NC}"
    echo "Bitte installieren Sie Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose gefunden: $(docker-compose --version)${NC}\n"

# Create .env file if it doesn't exist
echo -e "${YELLOW}[3/8] Erstelle Environment-Konfiguration (.env)...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    # Generate a random secret key
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "your-super-secret-key-change-this-in-production-$(date +%s)")
    # Replace SECRET_KEY in .env (works on both macOS and Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/your-super-secret-key-change-this-in-production-min-32-chars/$SECRET_KEY/" .env
    else
        sed -i "s/your-super-secret-key-change-this-in-production-min-32-chars/$SECRET_KEY/" .env
    fi
    echo -e "${GREEN}✓ .env-Datei erstellt mit generiertem Secret Key${NC}\n"
else
    echo -e "${GREEN}✓ .env-Datei existiert bereits${NC}\n"
fi

# Stop any running containers
echo -e "${YELLOW}[4/8] Stoppe alte Container (falls vorhanden)...${NC}"
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓ Bereinigt${NC}\n"

# Pull/Build images
echo -e "${YELLOW}[5/8] Baue Docker Images (das kann 5-10 Minuten dauern)...${NC}"
docker-compose build
echo -e "${GREEN}✓ Images gebaut${NC}\n"

# Start services
echo -e "${YELLOW}[6/8] Starte alle Services...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Services gestartet${NC}\n"

# Wait for services to be ready
echo -e "${YELLOW}[7/8] Warte auf Service-Bereitschaft...${NC}"
echo "   • PostgreSQL..."
sleep 5
echo "   • Backend API..."
sleep 5
echo "   • Frontend..."
sleep 3
echo "   • Qdrant Vector DB..."
sleep 2
echo "   • Ollama (lädt Llama-Modell - das kann beim ersten Mal 10-15 Min dauern)..."
sleep 5

# Check if backend is healthy
echo "   • Prüfe Backend Health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo -e "${GREEN}   ✓ Backend ist bereit!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}   ⚠ Backend antwortet nicht nach 30 Sekunden${NC}"
        echo "   Das ist OK - es startet möglicherweise noch. Prüfen Sie die Logs mit: docker-compose logs backend"
    fi
    sleep 1
done

# Load seed data
echo -e "\n${YELLOW}[8/8] Lade Demo-Daten...${NC}"
echo "   Erstelle 3 Demo-User, 15 Mitarbeiter, Qualifikationen..."
sleep 2

# Try to load seed data
if docker-compose exec -T backend python ../scripts/seed_data.py 2>/dev/null; then
    echo -e "${GREEN}✓ Demo-Daten geladen!${NC}\n"
else
    echo -e "${YELLOW}⚠ Demo-Daten konnten nicht geladen werden${NC}"
    echo "   Sie können dies später manuell tun mit: make seed"
    echo "   oder: docker-compose exec backend python ../scripts/seed_data.py${NC}\n"
fi

# Success message
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║                    ✓ Setup erfolgreich!                   ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 Ihre PAV Personalfinder Instanz ist bereit!${NC}\n"

echo "📍 URLs:"
echo "   Frontend:  ${BLUE}http://localhost:3000${NC}"
echo "   Backend:   ${BLUE}http://localhost:8000${NC}"
echo "   API Docs:  ${BLUE}http://localhost:8000/docs${NC}"
echo ""

echo "👤 Demo-Accounts:"
echo "   Admin:     ${GREEN}admin${NC} / ${GREEN}admin123${NC}"
echo "   HR Manager:${GREEN}hr_manager${NC} / ${GREEN}hr123${NC}"
echo "   Viewer:    ${GREEN}viewer${NC} / ${GREEN}viewer123${NC}"
echo ""

echo "📝 Nächste Schritte:"
echo "   1. Öffnen Sie ${BLUE}http://localhost:3000${NC} im Browser"
echo "   2. Melden Sie sich mit ${GREEN}admin / admin123${NC} an"
echo "   3. Gehen Sie zu ${YELLOW}KI-Suche${NC} und probieren Sie: 'Finde SAP-Experten für Logistik'"
echo ""

echo "🛠️  Nützliche Befehle:"
echo "   make logs      - Zeige alle Logs"
echo "   make status    - Zeige Service-Status"
echo "   make stop      - Stoppe alle Services"
echo "   make restart   - Neustart"
echo "   make health    - Gesundheits-Check"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${YELLOW}💡 Tipp: Ollama lädt beim ersten Start das Llama-Modell (~4.7 GB).${NC}"
echo -e "${YELLOW}   Das kann 10-15 Minuten dauern. Prüfen Sie den Status mit: make ollama-status${NC}\n"

# Offer to open browser
if command -v open &> /dev/null; then
    read -p "Browser öffnen? (j/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[JjYy]$ ]]; then
        open http://localhost:3000
    fi
elif command -v xdg-open &> /dev/null; then
    read -p "Browser öffnen? (j/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[JjYy]$ ]]; then
        xdg-open http://localhost:3000
    fi
fi

echo -e "${GREEN}Viel Erfolg mit PAV Personalfinder! 🎉${NC}"
