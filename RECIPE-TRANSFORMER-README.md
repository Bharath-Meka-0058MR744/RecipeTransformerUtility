# Recipe Transformer Utility v4.0

A comprehensive Python utility to transform recipe JSON files to conform to the `recipe-schema-draft-01.json` standard as defined in the **AI Enablement - Connectors Metadata Standardization** specification.

## Overview

This utility implements the complete recipe metadata standardization framework for IBM webMethods Hybrid Integration, enabling AI-powered workflow creation by providing consistent, normalized metadata for connectors, applications, and integration recipes.

## Features

### Core Capabilities
- ✅ **Full Schema Compliance**: Implements recipe-schema-draft-01.json specification
- ✅ **Application Metadata**: Extracts and transforms connector/application information
- ✅ **Interaction Support**: Handles actions and triggers with authentication metadata
- ✅ **Provenance Tracking**: Maintains lifecycle metadata (status, visibility, timestamps)
- ✅ **Dependency Management**: Tracks application and interaction dependencies
- ✅ **Tag System**: Supports categories, keywords, and platform availability
- ✅ **Compatibility Info**: Runtime and version requirements
- ✅ **Usage Statistics**: Download counts, ratings, and active instances

### Transformation Features
- ✅ Validates existing recipe-schema-draft-01.json format
- ✅ Transforms application metadata with actions/triggers
- ✅ Extracts connector information from workflow recipes
- ✅ Generates unique UUIDs and semantic versions
- ✅ Converts names to kebab-case format
- ✅ Infers trigger types (webhook, polling, listener)
- ✅ Extracts authentication types from capabilities
- ✅ Preserves all original metadata
- ✅ Outputs clean, formatted JSON

## Recipe Schema Structure

The standard schema (`recipe-schema-draft-01.json`) defines recipes with:

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
    "category": ["Category1", "Category2"],
    "availableOn": ["workflow", "flow.cloud", "flow.anywhere"],
    "keyword": ["keyword1", "keyword2"],
    "supportsEdge": false
  },
  "provenance": {
    "status": "draft|published|deprecated|archived",
    "visibility": "public|private|organization",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z",
    "publishedAt": "2024-01-01T00:00:00Z",
    "owner": {
      "userId": "user-id",
      "tenantId": "tenant-id",
      "orgId": "org-id"
    }
  },
  "dependencies": {
    "applications": [
      {
        "id": "application-id",
        "label": "Application Name",
        "icon": "icon-name"
      }
    ],
    "interactions": [
      {
        "type": "trigger|action",
        "applicationId": "application-id",
        "id": "interaction-id",
        "label": "Interaction Name",
        "triggerType": "webhook|polling|listener",
        "authType": "oauth2|credentials|api-key"
      }
    ]
  },
  "compatibility": {
    "runtime": "workflow-engine|integration-server",
    "minRuntimeVersion": "10.15.0",
    "maxRuntimeVersion": "12.0.0"
  },
  "configurations": {},
  "usageStatistics": {
    "downloadCount": 1247,
    "activeInstances": 89,
    "rating": {
      "average": 4.7,
      "count": 156
    },
    "lastUsed": "2024-12-20T18:30:00Z"
  }
}
```

## Usage

### Basic Usage

```bash
python recipe_transformer.py <input_recipe.json> [output_file.json]
```

### Examples

**Transform application metadata with actions/triggers:**
```bash
python recipe_transformer.py resources/jira-application.json
# Output: resources/jira-application_transformed.json
```

**Transform interaction metadata:**
```bash
python recipe_transformer.py resources/jira-interactions.json
# Extracts 9 actions and 30 triggers with authentication info
```

**Validate existing recipe:**
```bash
python recipe_transformer.py workflowSample.json
# Validates and enhances already-compliant recipes
```

**Transform with custom output path:**
```bash
python recipe_transformer.py recipes/myRecipe.json output/standardized_recipe.json
```

### Web Application

A Flask-based web interface is also available:

```bash
cd webapp
./run.sh
# Access at http://localhost:5001
```

See [WEBAPP-QUICKSTART.md](WEBAPP-QUICKSTART.md) for details.

## Input Formats Supported

### 1. Recipe Schema Format (Already Compliant)
Recipes that already follow `recipe-schema-draft-01.json`:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440105",
  "name": "slack-message-to-google-tasks",
  "label": "Create Google Task for Slack Message",
  "description": {...},
  "version": "1.0.0",
  "tags": {...},
  "provenance": {...},
  "dependencies": {...}
}
```

### 2. Application Metadata Format
Application/connector definitions with capabilities:

```json
{
  "id": "com.softwareag.cloudstreams.jira_v2.1",
  "name": "atlassianJira",
  "label": "Atlassian Jira",
  "description": "JIRA issue tracking product",
  "version": "2.1",
  "icon": "atlassian-jira-icon",
  "tags": {
    "categories": ["Collaboration", "Productivity"]
  },
  "capabilities": {
    "auths": [
      {
        "name": "credentials",
        "label": "Credentials",
        "type": "credentials"
      }
    ],
    "interactionTypes": ["actions", "triggers"]
  }
}
```

### 3. Interaction Metadata Format
Application with actions and triggers:

```json
{
  "id": "app-id",
  "name": "application-name",
  "label": "Application Label",
  "actions": [
    {
      "id": "action-id",
      "name": "actionName",
      "label": "Action Label",
      "description": "Action description"
    }
  ],
  "triggers": [
    {
      "id": "trigger-id",
      "name": "triggerName",
      "label": "Trigger Label",
      "description": "Trigger description"
    }
  ]
}
```

### 4. Complex Recipe Format
Workflow recipes with connector information:

```json
{
  "output": {
    "recipe": {
      "connectors": ["Clock", "Box", "Loop"],
      "name": "Box Integration"
    },
    "connectors_icons": [
      {"connector": "Box", "icon": "box"}
    ]
  }
}
```

## Transformation Logic

### Process Flow

1. **Format Detection**: Identifies input format and structure
2. **Validation**: Checks if already compliant with schema
3. **Extraction**: Pulls metadata from various locations
4. **Normalization**: Converts to standard formats
   - Names → kebab-case
   - Versions → semantic versioning (MAJOR.MINOR.PATCH)
   - IDs → UUIDs
5. **Enhancement**: Adds missing required fields
6. **Interaction Processing**: Extracts actions/triggers with auth info
7. **Dependency Mapping**: Links applications and interactions
8. **Provenance Creation**: Generates lifecycle metadata
9. **Validation**: Ensures output conforms to schema
10. **Output**: Saves formatted JSON

### Key Transformations

**Name Normalization:**
- `Atlassian Jira` → `atlassian-jira`
- `ServiceNow_SanDiego` → `servicenow-sandiego`

**Version Conversion:**
- `2.1` → `2.1.0`
- `San Diego` → `1.0.0`

**Interaction Extraction:**
- Actions: Extracted with authentication type
- Triggers: Extracted with trigger type inference
- Auth types: Mapped from capabilities.auths

**Trigger Type Inference:**
- Webhook: Based on name/description keywords
- Polling: Default for most triggers
- Listener: Based on event-driven patterns

## Output Examples

### Example 1: Application Metadata → Recipe

**Input** (`jira-application.json`):
```json
{
  "id": "com.softwareag.cloudstreams.jira_v2.1",
  "name": "atlassianJira",
  "label": "Atlassian Jira",
  "version": "2.1",
  "capabilities": {
    "auths": [{"type": "credentials"}],
    "interactionTypes": ["actions", "triggers"]
  }
}
```

**Output** (`jira-application_transformed.json`):
```json
{
  "id": "c6ea5726-4107-47df-a85d-06675981e374",
  "name": "atlassianjira",
  "label": "Atlassian Jira",
  "description": {
    "overview": "Integration recipe for Atlassian Jira",
    "details": "This recipe provides comprehensive integration capabilities..."
  },
  "version": "2.1.0",
  "tags": {
    "category": ["Collaboration", "Productivity"],
    "availableOn": ["workflow"],
    "keyword": []
  },
  "provenance": {
    "status": "draft",
    "visibility": "private",
    "createdAt": "2026-04-08T05:51:09.123456Z",
    "updatedAt": "2026-04-08T05:51:09.123456Z",
    "publishedAt": null,
    "owner": {"userId": "system"}
  },
  "dependencies": {
    "applications": [
      {
        "id": "com.softwareag.cloudstreams.jira_v2.1",
        "label": "Atlassian Jira",
        "icon": "atlassian-jira-icon"
      }
    ]
  },
  "compatibility": {},
  "configurations": {},
  "usageStatistics": {}
}
```

### Example 2: Interactions → Recipe with Dependencies

**Input** (`jira-interactions.json`):
- 9 actions (getProjectDetails, createProject, etc.)
- 30 triggers (newIssue, issueUpdated, etc.)

**Output**:
- Recipe with 1 application dependency
- 39 interactions (9 actions + 30 triggers)
- Each interaction includes:
  - Type (action/trigger)
  - Application ID reference
  - Authentication type
  - Trigger type (for triggers)

## API Alignment

This transformer aligns with the AI Enablement - Connectors Metadata Standardization API endpoints:

- `GET /applications` → Application metadata
- `GET /applications/{aid}/interactions` → Actions and triggers
- `GET /recipes` → Recipe listings
- `GET /recipes/{rid}` → Recipe details
- `GET /recipes/{rid}/dependencies` → Dependency information

## Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

## File Structure

```
.
├── recipe_transformer.py              # Main utility (v4.0)
├── recipe-schema-draft-01.json        # Standard schema definition
├── workflowSample.json                # Sample compliant recipe
├── README.md                          # Quick start guide
├── RECIPE-TRANSFORMER-README.md       # This file (detailed docs)
├── resources/                         # Sample metadata files
│   ├── jira-application.json
│   ├── jira-interactions.json
│   ├── slack-application.json
│   ├── servicenow-application.json
│   └── AI+Enablement+-+Connectors+Metadata+Standarization.doc
└── webapp/                            # Web interface
    ├── app.py
    ├── run.sh
    └── templates/
```

## Error Handling

The utility handles various scenarios:

- **Missing input file**: Clear error with file path
- **Invalid JSON**: Reports parsing errors with line numbers
- **Missing schema**: Continues with built-in validation
- **Unknown format**: Best-effort transformation with warnings
- **Invalid versions**: Converts to valid semver format
- **Invalid UUIDs**: Generates new UUIDs
- **Invalid names**: Converts to kebab-case

## Exit Codes

- `0`: Success
- `1`: Error (file not found, invalid JSON, etc.)

## Validation Rules

### Required Fields
- `id`: Must be valid UUID
- `name`: Must be kebab-case (lowercase, hyphens only)
- `label`: Non-empty string
- `description.overview`: Required, ≤150 characters recommended
- `version`: Must be semantic version (MAJOR.MINOR.PATCH)
- `tags.category`: At least one category
- `tags.availableOn`: At least one platform
- `provenance`: Complete lifecycle metadata
- `dependencies.applications`: At least one application

### Optional Fields
- `description.details`: Markdown supported
- `tags.keyword`: Array of search keywords
- `tags.supportsEdge`: Boolean flag
- `dependencies.interactions`: Actions and triggers
- `compatibility`: Runtime requirements
- `configurations`: System properties
- `usageStatistics`: Usage metrics

## Platform Support

### Supported Platforms (availableOn)
- `workflow`: Workflow Engine
- `flow.cloud`: Flow Cloud
- `flow.anywhere`: Flow Anywhere (DADA)

### Supported Runtimes
- `workflow-engine`: Workflow runtime
- `integration-server`: Integration Server runtime

### Authentication Types
- `credentials`: Username/password
- `oauth2`: OAuth 2.0 (various flows)
- `oauth_v20_authorization_code`: OAuth 2.0 Authorization Code
- `api-key`: API key authentication
- `aws-signature-v4`: AWS Signature v4
- `connection`: Connection-based auth

### Trigger Types
- `webhook`: HTTP webhook triggers
- `polling`: Polling-based triggers
- `listener`: Event listener triggers

## Contributing

To extend the transformer:

1. Add new extraction methods for specific formats
2. Update `_transform_to_recipe_schema()` to handle new cases
3. Add validation rules in `_validate_and_enhance()`
4. Update tests and documentation

## Version History

### v4.0 (Current)
- Full implementation of recipe-schema-draft-01.json
- Support for interactions (actions/triggers)
- Authentication type extraction
- Trigger type inference
- Enhanced provenance tracking
- Improved validation and error handling
- Alignment with AI Enablement specification

### v3.0
- Basic recipe-schema-draft-01.json support
- Application extraction
- Workflow sample reference

### v2.0
- Data preservation features
- Original data storage

### v1.0
- Initial release
- Basic transformation

## License

This utility is part of the IBM webMethods integration project.

## Support

For issues or questions:
1. Check this documentation
2. Review sample files in `resources/`
3. Examine `workflowSample.json` for reference
4. Consult AI Enablement - Connectors Metadata Standardization specification

## References

- Recipe Schema: `recipe-schema-draft-01.json`
- Specification: `resources/AI+Enablement+-+Connectors+Metadata+Standarization.doc`
- Sample Recipe: `workflowSample.json`
- Application Samples: `resources/*.json`