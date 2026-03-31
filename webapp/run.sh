#!/bin/bash
# Recipe Transformer Web Application Startup Script

echo "=========================================="
echo "Recipe Transformer Web Application"
echo "=========================================="
echo ""

# Check if we're in the webapp directory
if [ ! -f "app.py" ]; then
    echo "Error: Please run this script from the webapp directory"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Start the application
echo "Starting Flask server..."
echo "Access the application at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""
echo "Note: Using port 5001 to avoid conflicts with macOS AirPlay"
echo "=========================================="
echo ""

python3 app.py

# Made with Bob
