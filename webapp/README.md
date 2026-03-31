# Recipe Transformer Web Application

A web-based interface for transforming recipe JSON schemas to conform to the newSchema.json standard.

## Features

- 🔄 **Transform Recipe Schemas**: Convert complex recipe structures to standardized format
- ✅ **Validate Schemas**: Check if input already conforms to newSchema.json
- 📋 **Copy & Download**: Easy export of transformed schemas
- 🎨 **Modern UI**: Clean, responsive interface with real-time feedback
- ⌨️ **Keyboard Shortcuts**: Efficient workflow with keyboard support

## Project Structure

```
webapp/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/
│       └── app.js        # Frontend logic
└── templates/
    └── index.html        # Main HTML template
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Navigate to the webapp directory**:
   ```bash
   cd webapp
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install Flask flask-cors
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

   Or make it executable and run:
   ```bash
   chmod +x app.py
   ./app.py
   ```

2. **Access the application**:
   Open your browser and navigate to:
   ```
   http://localhost:5001
   ```
   
   **Note:** Using port 5001 to avoid conflicts with macOS AirPlay Receiver.

## Usage

### Basic Workflow

1. **Input Schema**: Paste your recipe JSON in the left panel
2. **Validate** (Optional): Click "Validate" to check if it already conforms to the schema
3. **Transform**: Click the "Transform ➜" button to convert the schema
4. **Export**: Copy or download the transformed output from the right panel

### Sample Data

Click the "Load Sample" button to load example recipe data and see how the transformation works.

### Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Transform the input schema
- **Tab**: Insert spaces for indentation in the input area

## API Endpoints

The application provides the following REST API endpoints:

### Transform Recipe
```
POST /api/transform
Content-Type: application/json

{
  "input": { ... recipe data ... }
}
```

**Response**:
```json
{
  "success": true,
  "output": [ ... transformed connectors ... ],
  "message": "Successfully transformed N connector(s)"
}
```

### Validate Schema
```
POST /api/validate
Content-Type: application/json

{
  "input": { ... recipe data ... }
}
```

**Response**:
```json
{
  "success": true,
  "valid": true,
  "message": "Input conforms to schema"
}
```

### Get Schema
```
GET /api/schema
```

**Response**:
```json
{
  "success": true,
  "schema": [ ... newSchema.json content ... ]
}
```

## Input Format Examples

### Complex Recipe Structure
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
      }
    ]
  }
}
```

### Already Formatted (Validation Only)
```json
[{
  "id": "unique-id",
  "name": "connector-name",
  "label": "Connector Label",
  "description": "Connector description",
  "version": "1.0.0",
  "tags": { ... },
  "capabilities": { ... },
  "sourceMetadata": { ... },
  "configurations": { ... }
}]
```

## Output Format

The output conforms to the newSchema.json standard with:

- **Unique IDs**: UUID v4 for each connector
- **Standardized Structure**: Consistent field names and types
- **Authentication Methods**: OAuth 2.0 and other auth types
- **Capabilities**: Actions, triggers, and templates
- **Metadata**: Source information and configurations

## Troubleshooting

### Port Already in Use
The application uses port 5001 by default to avoid conflicts with macOS AirPlay Receiver (port 5000).

If port 5001 is also in use, modify the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Change to any available port
```

**To disable AirPlay Receiver on macOS:**
- System Settings → General → AirDrop & Handoff → Turn off "AirPlay Receiver"

### Module Not Found
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Schema File Not Found
The application expects `newSchema.json` in the parent directory. Ensure the file structure is:
```
recipeTxUtility/
├── newSchema.json
├── recipe-transformer.py
└── webapp/
    └── app.py
```

## Development

### Running in Debug Mode
The application runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Customization
- **Styles**: Edit `static/css/style.css`
- **Frontend Logic**: Edit `static/js/app.js`
- **Backend Logic**: Edit `app.py`
- **UI Layout**: Edit `templates/index.html`

## Security Notes

- This is a development server. For production, use a WSGI server like Gunicorn or uWSGI
- Input validation is performed on both frontend and backend
- CORS is enabled for development; configure appropriately for production

## License

Part of the Recipe Transformer Utility project.

## Support

For issues or questions, refer to the main project README or documentation.