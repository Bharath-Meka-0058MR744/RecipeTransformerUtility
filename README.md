# Recipe Transformer Utility v2.0

A Python utility to transform recipe JSON files to conform to the `newSchema.json` standard format while **preserving ALL original content**.

## Overview

This utility helps standardize recipe/connector definitions by transforming various input formats into a consistent schema that follows the `newSchema.json` specification. **Version 2.0 ensures NO DATA LOSS** - all original content is preserved in the transformed output.

## Features

- ✅ Validates if input already conforms to schema
- ✅ Transforms complex recipe structures to standard connector format
- ✅ Extracts connector information from workflow recipes
- ✅ Generates unique IDs for each connector
- ✅ Preserves connector icons and metadata
- ✅ **PRESERVES ALL ORIGINAL DATA** - no content loss (v2.0)
- ✅ Stores complete original recipe in `originalRecipeData` field
- ✅ Extracts and preserves actions, triggers, operations
- ✅ Maintains custom fields and nested data structures
- ✅ Outputs clean, formatted JSON with transformation metadata

## Schema Format

The standard schema (`newSchema.json`) defines connectors with the following structure:

```json
{
    "id": "unique-uuid",
    "name": "connector-name",
    "label": "Display Label",
    "description": "Connector description",
    "version": "1.0.0",
    "icon": "icon-name",
    "tags": {
        "category": ["Category"],
        "deprecated": false,
        "availableOn": ["workflow", "flow.cloud", "flow.anywhere"]
    },
    "capabilities": {
        "auths": [...],
        "interactionTypes": ["actions", "triggers"]
    },
    "sourceMetadata": {
        "scope": "global",
        "framework": "cloudstreams",
        "provider": "ProviderName"
    },
    "configurations": {
        "allowCustomOperations": true,
        "allowDeleteApplication": false,
        "allowUpdateApplication": false
    }
},
    "originalRecipeData": {
        // Complete original recipe data preserved here
    },
    "recipeDetails": {
        // Extracted recipe details (actions, triggers, etc.)
    },
    "actions": [...],
    "triggers": [...],
    "operations": [...],
    "transformationMetadata": {
        "transformedAt": "2024-01-01T00:00:00Z",
        "transformerVersion": "2.0.0",
        "schemaVersion": "newSchema.json",
        "preservedOriginalData": true
    }
}
```

## Usage

### Basic Usage

```bash
python3 recipe_transformer.py <input_recipe.json> [output_file.json]
```

### Examples

**Transform a complex recipe (preserves all content):**
```bash
python3 recipe_transformer.py recipes/boxComplexRecipe.json recipes/transformed_recipe.json
# Input: 361 KB → Output: ~361 KB (all content preserved)
```

**Validate an existing recipe (auto-generates output filename):**
```bash
python3 recipe_transformer.py recipes/boxRecipev1.json
# Output: recipes/boxRecipev1_transformed.json
```

**Transform with custom output path:**
```bash
python3 recipe_transformer.py recipes/myRecipe.json output/standardized_recipe.json
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

### 1. Standard Schema Format (Already Compliant)
If your input already follows the `newSchema.json` format, the utility will validate and pass it through:

```json
[
    {
        "id": "...",
        "name": "connector-name",
        "label": "Connector Label",
        ...
    }
]
```

### 2. Complex Recipe Format
Extracts connector definitions from complex workflow recipes:

```json
{
    "output": {
        "recipe": {
            "connectors": ["Clock", "Box", "Loop"],
            ...
        },
        "connectors_icons": [
            {"connector": "Box", "icon": "box"},
            ...
        ]
    }
}
```

## Output

The utility generates a JSON array of connector definitions that conform to the standard schema:

```json
[
    {
        "id": "generated-uuid",
        "name": "clock",
        "label": "Clock",
        "description": "Clock connector for workflow integration.",
        "version": "1.0.0",
        "icon": "clock",
        "tags": {...},
        "capabilities": {...},
        "sourceMetadata": {...},
        "configurations": {...}
    },
    ...
]
```

## Transformation Logic (v2.0)

1. **Format Detection**: Identifies if input is already in standard format
2. **Connector Extraction**: Extracts connector names and metadata from complex structures
3. **ID Generation**: Creates unique UUIDs for each connector
4. **Metadata Mapping**: Maps icons, names, and other properties
5. **Schema Compliance**: Ensures all required fields are present
6. **Data Preservation**: Stores complete original data in `originalRecipeData`
7. **Content Extraction**: Extracts actions, triggers, operations into dedicated fields
8. **Custom Field Preservation**: Maintains all custom fields with `original_` prefix
9. **Metadata Addition**: Adds transformation metadata for tracking
10. **Validation**: Verifies output conforms to schema standards

### Key Improvements in v2.0

- **Zero Data Loss**: All original content is preserved in the output
- **Dual Storage**: Data stored both in `originalRecipeData` (complete) and extracted fields (structured)
- **File Size Preservation**: Output file size matches or exceeds input size (no compression)
- **Transformation Tracking**: Metadata tracks when and how transformation occurred

## Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

## File Structure

```
.
├── recipe_transformer.py          # Main utility script (CLI & library)
├── newSchema.json                 # Standard schema definition
├── README.md                      # Main documentation
├── RECIPE-TRANSFORMER-README.md   # Detailed documentation
└── webapp/                        # Web interface
    ├── app.py                     # Flask application
    ├── run.sh                     # Startup script
    └── templates/                 # HTML templates
```

## Error Handling

The utility handles various error scenarios:

- **Missing input file**: Clear error message with file path
- **Invalid JSON**: Reports JSON parsing errors
- **Missing schema**: Alerts if `newSchema.json` is not found
- **Unknown format**: Attempts best-effort transformation with warnings

## Exit Codes

- `0`: Success
- `1`: Error (file not found, invalid JSON, etc.)

## Examples of Transformation

### Example 1: Complex Recipe → Standard Format

**Input** (`boxComplexRecipe.json`):
```json
{
    "output": {
        "recipe": {
            "connectors": ["Clock", "Box", "Loop", "Developer Tools"]
        },
        "connectors_icons": [
            {"connector": "Clock", "icon": "Clock"},
            {"connector": "Box", "icon": "box"}
        ]
    }
}
```

**Output** (`boxComplexRecipe_transformed.json`):
```json
[
    {
        "id": "9a9f3828-b3f2-4887-88b4-613135d33c9e",
        "name": "Clock",
        "label": "Clock",
        "icon": "Clock",
        ...
    },
    {
        "id": "43c61bdb-6f2c-470a-bc68-6f5a7deda5f5",
        "name": "Box",
        "label": "Box",
        "icon": "box",
        ...
    }
]
```

### Example 2: Already Compliant Format

**Input** (`boxRecipev1.json`):
```json
[
    {
        "id": "clock-connector-id",
        "name": "clock",
        "label": "Clock",
        ...
    }
]
```

**Output**: Same as input (validated and passed through)

## Contributing

To extend the transformer for new input formats:

1. Add a new transformation method in the `RecipeTransformer` class
2. Update the `transform()` method to detect and route to your new method
3. Ensure output conforms to `newSchema.json` structure

## License

This utility is part of the wmiorecipes project.

## Support

For issues or questions, please refer to the main project documentation or create an issue in the repository.
