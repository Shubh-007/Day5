#!/bin/bash

# Elation Health Chart Review - Run Both Services

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================================================="
echo "🚀 Elation Health Chart Review - Starting All Services"
echo "==========================================================================${NC}"

# Function to run backend
run_backend() {
    echo -e "\n${GREEN}▶️  Starting Backend API...${NC}"
    cd backend
    source venv/bin/activate
    python app.py
}

# Function to run frontend
run_frontend() {
    echo -e "\n${GREEN}▶️  Starting Frontend...${NC}"
    cd frontend
    npm run dev
}

# Start both in background
run_backend &
BACKEND_PID=$!

sleep 2

run_frontend &
FRONTEND_PID=$!

echo -e "\n${GREEN}=========================================================================="
echo "✨ All Services Running!"
echo "=========================================================================="
echo ""
echo -e "${YELLOW}📍 Backend API:${NC} http://localhost:8000"
echo -e "${YELLOW}📍 Frontend:${NC} http://localhost:3000"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for Ctrl+C and cleanup
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

wait
