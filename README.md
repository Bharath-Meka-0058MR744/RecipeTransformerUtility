# Recipe Transformer Utility

A Python utility to transform recipe JSON files to conform to the `newSchema.json` standard format.

## Overview

This utility helps standardize recipe/connector definitions by transforming various input formats into a consistent schema that follows the `newSchema.json` specification.

## Features

- ✅ Validates if input already conforms to schema
- ✅ Transforms complex recipe structures to standard connector format
- ✅ Extracts connector information from workflow recipes
- ✅ Generates unique IDs for each connector
- ✅ Preserves connector icons and metadata
- ✅ Outputs clean, formatted JSON

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
}
```

## Usage

### Basic Usage

```bash
python3 recipe-transformer.py <input_recipe.json> [output_file.json]
```

### Examples

**Transform a complex recipe:**
```bash
python3 recipe-transformer.py recipes/boxComplexRecipe.json recipes/transformed_recipe.json
```

**Validate an existing recipe (auto-generates output filename):**
```bash
python3 recipe-transformer.py recipes/boxRecipev1.json
# Output: recipes/boxRecipev1_transformed.json
```

**Transform with custom output path:**
```bash
python3 recipe-transformer.py recipes/myRecipe.json output/standardized_recipe.json
```

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

## Transformation Logic

1. **Format Detection**: Identifies if input is already in standard format
2. **Connector Extraction**: Extracts connector names and metadata from complex structures
3. **ID Generation**: Creates unique UUIDs for each connector
4. **Metadata Mapping**: Maps icons, names, and other properties
5. **Schema Compliance**: Ensures all required fields are present
6. **Validation**: Verifies output conforms to schema standards

## Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

## File Structure

```
.
├── recipe-transformer.py          # Main utility script
├── RECIPE-TRANSFORMER-README.md   # This documentation
└── recipes/
    ├── newSchema.json             # Standard schema definition
    ├── boxRecipev1.json           # Example: Already compliant
    ├── boxComplexRecipe.json      # Example: Complex format
    └── *_transformed.json         # Generated output files
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
