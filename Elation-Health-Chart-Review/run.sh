#!/bin/bash

# Elation Health Chart Review - Local Development Setup and Run

set -e

echo "🚀 Elation Health Chart Review - Starting Development Environment"
echo "=========================================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check for Node
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is required but not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $(python3 --version | cut -d' ' -f2) found${NC}"
echo -e "${GREEN}✓ Node $(node --version) found${NC}"

# Create virtual environment for backend if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo -e "\n${YELLOW}📦 Creating Python virtual environment...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    cd ..
    echo -e "${GREEN}✓ Backend environment ready${NC}"
fi

# Install frontend dependencies if node_modules doesn't exist
if [ ! -d "frontend/node_modules" ]; then
    echo -e "\n${YELLOW}📦 Installing frontend dependencies...${NC}"
    cd frontend
    npm install --silent
    cd ..
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
fi

echo -e "\n${GREEN}=========================================================================="
echo "✨ Development Environment Ready!"
echo "=========================================================================="
echo ""
echo -e "${YELLOW}To start the services, run in separate terminals:${NC}"
echo ""
echo -e "${GREEN}Terminal 1 - Backend API (http://localhost:8000):${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo -e "${GREEN}Terminal 2 - Frontend (http://localhost:3000):${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo -e "${YELLOW}Or run both together in background:${NC}"
echo "  ./run-dev.sh"
echo ""
