# Recipe Transformer Utility v4.0

A comprehensive Python utility to transform recipe JSON files to conform to the `recipe-schema-draft-01.json` standard as defined in the **AI Enablement - Connectors Metadata Standardization** specification.

## 🎯 Overview

This utility implements the complete recipe metadata standardization framework for IBM webMethods Hybrid Integration, enabling AI-powered workflow creation by providing consistent, normalized metadata for connectors, applications, and integration recipes.

## ✨ Key Features

- ✅ **Full Schema Compliance**: Implements recipe-schema-draft-01.json specification
- ✅ **Application Metadata**: Extracts and transforms connector/application information
- ✅ **Interaction Support**: Handles actions and triggers with authentication metadata
- ✅ **Provenance Tracking**: Maintains lifecycle metadata (status, visibility, timestamps)
- ✅ **Dependency Management**: Tracks application and interaction dependencies
- ✅ **Tag System**: Supports categories, keywords, and platform availability
- ✅ **Compatibility Info**: Runtime and version requirements
- ✅ **Usage Statistics**: Download counts, ratings, and active instances
- ✅ **Format Detection**: Auto-detects and transforms various input formats
- ✅ **Validation**: Ensures output conforms to schema standards

## 🚀 Quick Start

### Basic Usage

```bash
python recipe_transformer.py <input_recipe.json> [output_file.json]
```

### Examples

**Transform application metadata:**
```bash
python recipe_transformer.py resources/jira-application.json
# Output: resources/jira-application_transformed.json
```

**Transform with interactions (actions/triggers):**
```bash
python recipe_transformer.py resources/jira-interactions.json
# Extracts 9 actions and 30 triggers with authentication info
```

**Validate existing recipe:**
```bash
python recipe_transformer.py workflowSample.json
# Validates and enhances already-compliant recipes
```

**Custom output path:**
```bash
python recipe_transformer.py recipes/input.json output/transformed.json
```

## 📋 Recipe Schema Structure

```json
{
  "id": "uuid",
  "name": "kebab-case-name",
  "label": "Display Name",
  "description": {
    "overview": "Brief description (≤150 chars)",
    "details": "Comprehensive markdown description"
  },
  "version": "1.0.0",
  "tags": {
    "category": ["Category1"],
    "availableOn": ["workflow", "flow.cloud"],
    "keyword": ["keyword1", "keyword2"]
  },
  "provenance": {
    "status": "draft|published|deprecated|archived",
    "visibility": "public|private|organization",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z",
    "owner": {"userId": "user-id"}
  },
  "dependencies": {
    "applications": [
      {"id": "app-id", "label": "App Name", "icon": "icon"}
    ],
    "interactions": [
      {
        "type": "trigger|action",
        "applicationId": "app-id",
        "id": "interaction-id",
        "label": "Interaction Name",
        "authType": "oauth2|credentials"
      }
    ]
  },
  "compatibility": {
    "runtime": "workflow-engine",
    "minRuntimeVersion": "10.15.0"
  },
  "usageStatistics": {
    "downloadCount": 1247,
    "activeInstances": 89,
    "rating": {"average": 4.7, "count": 156}
  }
}
```

## 📥 Supported Input Formats

### 1. Recipe Schema Format (Already Compliant)
Recipes that already follow `recipe-schema-draft-01.json` are validated and enhanced.

### 2. Application Metadata Format
Application/connector definitions with capabilities:
```json
{
  "id": "com.softwareag.cloudstreams.jira_v2.1",
  "name": "atlassianJira",
  "label": "Atlassian Jira",
  "capabilities": {
    "auths": [{"type": "credentials"}],
    "interactionTypes": ["actions", "triggers"]
  }
}
```

### 3. Interaction Metadata Format
Applications with actions and triggers:
```json
{
  "id": "app-id",
  "name": "application-name",
  "actions": [...],
  "triggers": [...]
}
```

### 4. Complex Recipe Format
Workflow recipes with connector information:
```json
{
  "output": {
    "recipe": {
      "connectors": ["Clock", "Box", "Loop"]
    },
    "connectors_icons": [...]
  }
}
```

## 🔄 Transformation Process

1. **Format Detection** → Identifies input structure
2. **Validation** → Checks schema compliance
3. **Extraction** → Pulls metadata from various locations
4. **Normalization** → Converts to standard formats
5. **Enhancement** → Adds missing required fields
6. **Interaction Processing** → Extracts actions/triggers
7. **Dependency Mapping** → Links applications and interactions
8. **Output** → Saves formatted JSON

## 📊 Example Transformation

**Input** (`jira-interactions.json`):
```
✓ Loaded input file (8.42 KB)
```

**Output** (`jira-interactions_transformed.json`):
```
Recipe Details:
  ID:      bd681b7b-9d10-4ddd-8673-5a6d87113425
  Name:    atlassian-jira
  Label:   Atlassian Jira
  Version: 1.0.0
  Status:  draft

Dependencies:
  Applications: 1
    - Atlassian Jira
  Interactions: 39
    - Actions:  9
    - Triggers: 30

✓ Output saved: 10.08 KB
```

## 🌐 Web Application

A Flask-based web interface is available for browser-based transformations:

```bash
cd webapp
./run.sh
# Access at http://localhost:5001
```

Features:
- Drag-and-drop file upload
- Real-time transformation
- Download transformed recipes
- Visual validation feedback

See [WEBAPP-QUICKSTART.md](WEBAPP-QUICKSTART.md) for details.

## 📚 Documentation

- **[RECIPE-TRANSFORMER-README.md](RECIPE-TRANSFORMER-README.md)** - Comprehensive documentation
- **[WEBAPP-QUICKSTART.md](WEBAPP-QUICKSTART.md)** - Web application guide
- **[recipe-schema-draft-01.json](recipe-schema-draft-01.json)** - Schema specification
- **[workflowSample.json](workflowSample.json)** - Sample compliant recipe

## 🔧 Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

For web application:
- Flask
- See `webapp/requirements.txt`

## 📁 Project Structure

```
.
├── recipe_transformer.py              # Main utility (v4.0)
├── recipe-schema-draft-01.json        # Standard schema
├── workflowSample.json                # Sample recipe
├── README.md                          # This file
├── RECIPE-TRANSFORMER-README.md       # Detailed docs
├── WEBAPP-QUICKSTART.md               # Web app guide
├── resources/                         # Sample metadata
│   ├── jira-application.json
│   ├── jira-interactions.json
│   ├── slack-application.json
│   ├── servicenow-application.json
│   └── AI+Enablement+-+Connectors+Metadata+Standarization.doc
└── webapp/                            # Web interface
    ├── app.py
    ├── run.sh
    ├── requirements.txt
    └── templates/
```

## 🎯 Use Cases

### For Developers
- Transform legacy recipe formats to new standard
- Validate recipe metadata before publishing
- Extract application and interaction metadata
- Generate AI-ready recipe definitions

### For AI Systems
- Consume standardized recipe metadata
- Discover available connectors and capabilities
- Generate workflow definitions automatically
- Recommend appropriate integrations

### For Integration Platforms
- Standardize connector metadata across frameworks
- Enable cross-platform recipe portability
- Support AI-powered workflow authoring
- Maintain consistent metadata quality

## 🔍 Validation Rules

### Required Fields
- `id`: Valid UUID
- `name`: Kebab-case format
- `label`: Non-empty string
- `description.overview`: ≤150 characters
- `version`: Semantic version (MAJOR.MINOR.PATCH)
- `tags.category`: At least one category
- `tags.availableOn`: At least one platform
- `provenance`: Complete lifecycle metadata
- `dependencies.applications`: At least one application

### Automatic Conversions
- Names → kebab-case (`Atlassian Jira` → `atlassian-jira`)
- Versions → semver (`2.1` → `2.1.0`)
- IDs → UUIDs (if invalid)
- Authentication types → standardized values
- Trigger types → inferred from metadata

## 🌟 Platform Support

### Supported Platforms
- `workflow` - Workflow Engine
- `flow.cloud` - Flow Cloud
- `flow.anywhere` - Flow Anywhere (DADA)

### Authentication Types
- `credentials` - Username/password
- `oauth2` - OAuth 2.0
- `api-key` - API key
- `aws-signature-v4` - AWS Signature v4

### Trigger Types
- `webhook` - HTTP webhook triggers
- `polling` - Polling-based triggers
- `listener` - Event listener triggers

## 🐛 Error Handling

The utility handles:
- Missing input files
- Invalid JSON syntax
- Unknown input formats
- Invalid versions/UUIDs/names
- Missing required fields

All errors include clear messages and suggestions.

## 📈 Version History

### v4.0 (Current)
- Full recipe-schema-draft-01.json implementation
- Interaction support (actions/triggers)
- Authentication type extraction
- Trigger type inference
- Enhanced validation
- AI Enablement specification alignment

### v3.0
- Basic recipe-schema support
- Application extraction

### v2.0
- Data preservation features

### v1.0
- Initial release

## 🤝 Contributing

To extend the transformer:
1. Add extraction methods for new formats
2. Update transformation logic
3. Add validation rules
4. Update documentation

## 📄 License

This utility is part of the IBM webMethods integration project.

## 🆘 Support

For issues or questions:
1. Check [RECIPE-TRANSFORMER-README.md](RECIPE-TRANSFORMER-README.md)
2. Review sample files in `resources/`
3. Examine `workflowSample.json`
4. Consult the AI Enablement specification

## 🔗 References

- **Recipe Schema**: `recipe-schema-draft-01.json`
- **Specification**: `resources/AI+Enablement+-+Connectors+Metadata+Standarization.doc`
- **Sample Recipe**: `workflowSample.json`
- **Application Samples**: `resources/*.json`

---

**Made with ❤️ for AI-powered integration**
