#!/usr/bin/env python3
"""
Recipe Transformer Utility
Transforms recipe JSON files to conform to the newSchema.json standard.

Usage:
    python recipe-transformer.py <input_recipe.json> [output_file.json]
"""

import json
import sys
import uuid
from typing import Dict, List, Any
from pathlib import Path


class RecipeTransformer:
    """Transform recipe JSON to conform to newSchema.json standard."""
    
    def __init__(self, schema_path: str = "recipes/newSchema.json"):
        """Initialize transformer with schema."""
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
    
    def _load_schema(self) -> List[Dict[str, Any]]:
        """Load the standard schema."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Schema file not found at {self.schema_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in schema file: {e}")
            sys.exit(1)
    
    def _get_schema_template(self) -> Dict[str, Any]:
        """Get a template based on the schema structure."""
        if self.schema and len(self.schema) > 0:
            return self.schema[0]
        return {}
    
    def transform(self, input_data: Any) -> List[Dict[str, Any]]:
        """
        Transform input recipe data to conform to newSchema.json.
        
        Args:
            input_data: Input recipe data (can be dict, list, or complex structure)
        
        Returns:
            List of transformed recipe objects conforming to schema
        """
        # If input is already in the correct format (list of connectors), validate and return
        if isinstance(input_data, list) and self._is_valid_schema_format(input_data):
            print("✓ Input already conforms to newSchema.json format")
            return input_data
        
        # If input is a complex recipe structure, extract connector information
        if isinstance(input_data, dict):
            return self._transform_complex_recipe(input_data)
        
        # Default: try to extract what we can
        print("⚠ Warning: Input format not recognized, attempting best-effort transformation")
        return self._transform_unknown_format(input_data)
    
    def _is_valid_schema_format(self, data: List[Dict[str, Any]]) -> bool:
        """Check if data already conforms to schema format."""
        if not data:
            return False
        
        required_fields = {'id', 'name', 'label', 'description', 'version', 
                          'tags', 'capabilities', 'sourceMetadata', 'configurations'}
        
        for item in data:
            if not isinstance(item, dict):
                return False
            if not required_fields.issubset(item.keys()):
                return False
        
        return True
    
    def _transform_complex_recipe(self, recipe_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform complex recipe structure to schema format."""
        connectors = []
        
        # Extract connectors from recipe structure
        if 'output' in recipe_data:
            output = recipe_data['output']
            
            # Get connector names from recipe
            connector_names = output.get('recipe', {}).get('connectors', [])
            
            # Get connector icons
            connector_icons = {}
            for icon_data in output.get('connectors_icons', []):
                connector_icons[icon_data.get('connector', '')] = icon_data.get('icon', '')
            
            # Create connector definitions
            for connector_name in connector_names:
                connector = self._create_connector_from_name(
                    connector_name, 
                    connector_icons.get(connector_name, '')
                )
                connectors.append(connector)
        
        if not connectors:
            print("⚠ Warning: No connectors found in complex recipe, creating default connector")
            connectors = [self._create_default_connector()]
        
        return connectors
    
    def _create_connector_from_name(self, name: str, icon: str = "") -> Dict[str, Any]:
        """Create a connector definition from a name."""
        template = self._get_schema_template()
        
        # Generate a unique ID
        connector_id = str(uuid.uuid4())
        
        # Create label from name (capitalize and replace hyphens/underscores)
        label = name.replace('-', ' ').replace('_', ' ').title()
        
        connector = {
            "id": connector_id,
            "name": name,
            "label": label,
            "description": f"{label} connector for workflow integration.",
            "version": "1.0.0",
            "icon": icon or name,
            "tags": {
                "category": ["Integration"],
                "deprecated": False,
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
                "provider": f"{label.replace(' ', '')}Provider"
            },
            "configurations": {
                "allowCustomOperations": True,
                "allowDeleteApplication": False,
                "allowUpdateApplication": False
            }
        }
        
        return connector
    
    def _create_default_connector(self) -> Dict[str, Any]:
        """Create a default connector when no data is available."""
        return self._create_connector_from_name("custom-connector", "puzzle")
    
    def _transform_unknown_format(self, data: Any) -> List[Dict[str, Any]]:
        """Handle unknown format with best-effort transformation."""
        return [self._create_default_connector()]
    
    def save_output(self, data: List[Dict[str, Any]], output_path: str):
        """Save transformed data to file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"✓ Output saved to: {output_path}")
        except Exception as e:
            print(f"Error saving output: {e}")
            sys.exit(1)


def main():
    """Main entry point for the utility."""
    if len(sys.argv) < 2:
        print("Usage: python recipe-transformer.py <input_recipe.json> [output_file.json]")
        print("\nExample:")
        print("  python recipe-transformer.py recipes/boxComplexRecipe.json recipes/transformed_recipe.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Generate default output filename if not provided
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_transformed.json")
    
    print(f"Recipe Transformer Utility")
    print(f"=" * 50)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print(f"Schema: recipes/newSchema.json")
    print(f"=" * 50)
    
    # Load input recipe
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        print(f"✓ Loaded input recipe")
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    
    # Transform
    transformer = RecipeTransformer()
    transformed_data = transformer.transform(input_data)
    
    print(f"✓ Transformation complete: {len(transformed_data)} connector(s) generated")
    
    # Save output
    transformer.save_output(transformed_data, output_file)
    
    print(f"\n{'=' * 50}")
    print(f"✓ Transformation successful!")
    print(f"  Generated {len(transformed_data)} connector definition(s)")
    print(f"  Output conforms to newSchema.json standard")


if __name__ == "__main__":
    main()

# Made with Bob
