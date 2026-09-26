#!/bin/bash
# Quick Start Script for Elation Health RAG Chatbot
# Usage: bash QUICK-START.sh

echo "🚀 Elation Health RAG Chatbot - Quick Start"
echo "==========================================="
echo ""

# Check if we have the required directories
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Not in the Elation-Health-Chart-Review directory"
    exit 1
fi

echo "✅ Step 1: Starting Backend Server..."
echo "   Command: cd backend && python app.py"
echo ""
echo "   To run in separate terminal:"
echo "   $ cd $(pwd)/backend"
echo "   $ python app.py"
echo ""

echo "✅ Step 2: Starting Frontend Server..."
echo "   Command: cd frontend && npm run dev"
echo ""
echo "   To run in separate terminal:"
echo "   $ cd $(pwd)/frontend"
echo "   $ npm run dev"
echo ""

echo "✅ Step 3: Open in Browser"
echo "   URL: http://localhost:5173"
echo ""

echo "✅ Step 4: Test RAG Chatbot"
echo "   1. Click on any patient in Dashboard"
echo "   2. Scroll down to '🤖 RAG Clinical Assistant'"
echo "   3. Click to expand the chatbot"
echo "   4. Select a suggested question or type your own"
echo "   5. Watch the response appear with sources!"
echo ""

echo "📚 Documentation"
echo "   • Quick Start:      cat CHATBOT-QUICKSTART.md"
echo "   • Full Guide:       cat RAG-CHATBOT-FEATURE.md"
echo "   • Testing Guide:    cat PATIENT-TESTING-GUIDE.md"
echo "   • Patient Profiles: cat SYNTHETIC-PATIENT-DATA.md"
echo ""

echo "🧪 Test Patients (13 total)"
echo "   Easy:    Emily Watson, Linda Martinez, Jessica Thompson"
echo "   Medium:  James Morrison, Sarah Johnson, David Chen"
echo "   Hard:    Margaret O'Brien, Thomas Anderson, Robert Mitchell ⭐⭐⭐"
echo ""

echo "💡 Try These Questions"
echo "   • What drug interactions should I check?"
echo "   • Are there any abnormal lab values?"
echo "   • What clinical guidelines apply?"
echo "   • What allergies does this patient have?"
echo "   • What preventive care is due?"
echo ""

echo "🎉 Ready to Go!"
echo "   Start the backend and frontend in separate terminals above."
