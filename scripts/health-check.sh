#!/bin/bash

# PAV Personalfinder - Health Check Script
# Prüft ob alle Services korrekt laufen

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              PAV Personalfinder - Health Check            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check HTTP endpoint
check_http() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}

    echo -n "  Checking $name... "

    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)

    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $http_code)"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code, expected $expected_code)"
        return 1
    fi
}

# Function to check container status
check_container() {
    local name=$1

    echo -n "  Checking $name container... "

    status=$(docker-compose ps -q $name 2>/dev/null)

    if [ -n "$status" ]; then
        running=$(docker inspect -f '{{.State.Running}}' $(docker-compose ps -q $name) 2>/dev/null)
        if [ "$running" = "true" ]; then
            echo -e "${GREEN}✓ Running${NC}"
            return 0
        else
            echo -e "${RED}✗ Not running${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Not found${NC}"
        return 1
    fi
}

total_checks=0
passed_checks=0

echo -e "${YELLOW}[1/3] Container Status${NC}"
echo ""

containers=("frontend" "backend" "db" "qdrant" "ollama")
for container in "${containers[@]}"; do
    ((total_checks++))
    if check_container "$container"; then
        ((passed_checks++))
    fi
done

echo ""
echo -e "${YELLOW}[2/3] HTTP Endpoints${NC}"
echo ""

((total_checks++))
if check_http "Frontend" "http://localhost:3000"; then
    ((passed_checks++))
fi

((total_checks++))
if check_http "Backend Health" "http://localhost:8000/health"; then
    ((passed_checks++))
fi

((total_checks++))
if check_http "Backend API Docs" "http://localhost:8000/docs"; then
    ((passed_checks++))
fi

((total_checks++))
if check_http "Qdrant" "http://localhost:6333/health"; then
    ((passed_checks++))
fi

((total_checks++))
if check_http "Ollama" "http://localhost:11434" "404"; then
    ((passed_checks++))
fi

echo ""
echo -e "${YELLOW}[3/3] Database Connection${NC}"
echo ""

echo -n "  Checking PostgreSQL connection... "
((total_checks++))
if docker-compose exec -T db pg_isready -U pav_user -d pav_personalfinder >/dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
    ((passed_checks++))
else
    echo -e "${RED}✗ FAILED${NC}"
fi

# Count tables
echo -n "  Checking database tables... "
table_count=$(docker-compose exec -T db psql -U pav_user -d pav_personalfinder -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ')
if [ "$table_count" -gt 0 ]; then
    echo -e "${GREEN}✓ OK${NC} ($table_count tables)"
else
    echo -e "${YELLOW}⚠ Warning${NC} (No tables found - run 'make seed')"
fi

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

percentage=$((passed_checks * 100 / total_checks))

if [ $passed_checks -eq $total_checks ]; then
    echo -e "${GREEN}✓ All checks passed! ($passed_checks/$total_checks)${NC}"
    echo ""
    echo "🎉 Your PAV Personalfinder is healthy and ready!"
    echo ""
    echo "📍 Access the application at:"
    echo "   Frontend: ${BLUE}http://localhost:3000${NC}"
    echo "   Backend:  ${BLUE}http://localhost:8000${NC}"
    echo ""
    exit 0
elif [ $percentage -ge 70 ]; then
    echo -e "${YELLOW}⚠ Mostly healthy ($passed_checks/$total_checks checks passed)${NC}"
    echo ""
    echo "Some services might still be starting up."
    echo "Wait a minute and run 'make health' again."
    echo ""
    exit 1
else
    echo -e "${RED}✗ Health check failed ($passed_checks/$total_checks checks passed)${NC}"
    echo ""
    echo "🔍 Troubleshooting steps:"
    echo "  1. Check logs: make logs"
    echo "  2. Restart services: make restart"
    echo "  3. Check README.md troubleshooting section"
    echo ""
    exit 2
fi
