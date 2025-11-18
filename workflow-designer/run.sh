#!/bin/bash

echo "🚀 Starting JioSign Workflow Designer..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Create workflows directory if it doesn't exist
mkdir -p workflows

# Run the application
streamlit run app.py --server.port 8502 --server.headless true

