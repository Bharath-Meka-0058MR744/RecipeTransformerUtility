# Recipe Transformer Web Application - Quick Start Guide

## 🚀 Quick Start

### Option 1: Using the Startup Script (Recommended)

```bash
cd webapp
./run.sh
```

### Option 2: Manual Start

```bash
cd webapp
pip3 install -r requirements.txt
python3 app.py
```

### Option 3: Direct Python Execution

```bash
cd webapp
python3 -m flask run
```

## 📱 Access the Application

Once started, open your browser and navigate to:

```
http://localhost:5001
```

**Note:** Using port 5001 to avoid conflicts with macOS AirPlay Receiver on port 5000.

## 🎯 How to Use

1. **Load Sample Data** (Optional)
   - Click "Load Sample" to see an example recipe structure

2. **Input Your Schema**
   - Paste your recipe JSON in the left input area
   - The input can be:
     - Complex recipe structures with connectors
     - Simple connector lists
     - Already formatted schemas (for validation)

3. **Validate** (Optional)
   - Click "Validate" to check if your input already conforms to newSchema.json

4. **Transform**
   - Click the "Transform ➜" button
   - The transformed schema will appear in the right panel

5. **Export Results**
   - Click "Copy" to copy to clipboard
   - Click "Download JSON" to save as a file

## ⌨️ Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Transform the input
- **Tab**: Insert spaces for indentation

## 📂 Project Structure

```
recipeTxUtility/
├── newSchema.json              # Target schema specification
├── recipe-transformer.py       # Original CLI utility
├── recipe_transformer.py       # Python module (for import)
└── webapp/                     # Web application
    ├── app.py                  # Flask backend
    ├── run.sh                  # Startup script
    ├── requirements.txt        # Python dependencies
    ├── README.md              # Detailed documentation
    ├── static/
    │   ├── css/
    │   │   └── style.css      # Application styles
    │   └── js/
    │       └── app.js         # Frontend logic
    └── templates/
        └── index.html         # Main HTML template
```

## 🔧 API Endpoints

The web application exposes REST API endpoints:

### Transform Recipe
```bash
curl -X POST http://localhost:5001/api/transform \
  -H "Content-Type: application/json" \
  -d '{"input": {...}}'
```

### Validate Schema
```bash
curl -X POST http://localhost:5001/api/validate \
  -H "Content-Type: application/json" \
  -d '{"input": {...}}'
```

### Get Schema Reference
```bash
curl http://localhost:5001/api/schema
```

## 📝 Example Input

```json
{
  "output": {
    "recipe": {
      "connectors": ["salesforce", "slack", "jira"]
    },
    "connectors_icons": [
      {
        "connector": "salesforce",
        "icon": "salesforce-icon"
      },
      {
        "connector": "slack",
        "icon": "slack-icon"
      },
      {
        "connector": "jira",
        "icon": "jira-icon"
      }
    ]
  }
}
```

## 📤 Example Output

```json
[
  {
    "id": "e2d3790e-c3bf-4b10-8fec-cc53eb7e20eb",
    "name": "salesforce",
    "label": "Salesforce",
    "description": "Salesforce connector for workflow integration.",
    "version": "1.0.0",
    "icon": "salesforce-icon",
    "tags": {
      "category": ["Integration"],
      "deprecated": false,
      "availableOn": ["workflow", "flow.cloud", "flow.anywhere"]
    },
    "capabilities": {
      "auths": [
        {
          "name": "oauth2",
          "label": "OAuth v2.0 (Authorization Code Flow)",
          "type": "oauth_v20_authorization_code"
        }
      ],
      "interactionTypes": ["actions", "triggers"]
    },
    "sourceMetadata": {
      "scope": "global",
      "framework": "cloudstreams",
      "provider": "SalesforceProvider"
    },
    "configurations": {
      "allowCustomOperations": true,
      "allowDeleteApplication": false,
      "allowUpdateApplication": false
    }
  }
]
```

## 🛠️ Troubleshooting

### Port Already in Use
The application now uses port 5001 by default to avoid conflicts with macOS AirPlay Receiver (which uses port 5000).

If port 5001 is also occupied, edit `webapp/app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Or any available port
```

**To disable AirPlay Receiver on macOS:**
1. Open System Settings
2. Go to General → AirDrop & Handoff
3. Turn off "AirPlay Receiver"

### Dependencies Not Found
Reinstall dependencies:
```bash
cd webapp
pip3 install -r requirements.txt
```

### Module Import Error
Ensure `recipe_transformer.py` exists in the parent directory:
```bash
ls -la ../recipe_transformer.py
```

### Browser Can't Connect
- Check if the server is running
- Verify the URL: `http://localhost:5001`
- Check firewall settings
- Try `http://127.0.0.1:5001` instead

## 🎨 Features

- ✅ Real-time JSON validation
- ✅ Syntax highlighting in text areas
- ✅ Responsive design (mobile-friendly)
- ✅ Copy to clipboard functionality
- ✅ Download as JSON file
- ✅ Sample data loader
- ✅ Status messages and error handling
- ✅ Keyboard shortcuts
- ✅ Auto-format JSON on paste

## 📚 Additional Resources

- **Detailed Documentation**: See `webapp/README.md`
- **CLI Utility**: See `RECIPE-TRANSFORMER-README.md`
- **Schema Reference**: See `newSchema.json`

## 🔒 Security Notes

- This is a development server
- For production, use a WSGI server (Gunicorn, uWSGI)
- Configure CORS appropriately for production
- Validate and sanitize all inputs

## 💡 Tips

1. Use the "Load Sample" button to understand the expected input format
2. Validate your input before transforming to catch errors early
3. Use keyboard shortcuts for faster workflow
4. The application auto-formats JSON when you paste it

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the detailed README in `webapp/README.md`
3. Verify your input JSON is valid

---

**Happy Transforming! 🎉**