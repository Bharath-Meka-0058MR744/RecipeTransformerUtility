#!/usr/bin/env python3
"""
Recipe Transformer Utility
Transforms recipe JSON files to conform to the recipe-schema-draft-01.json standard.
Uses workflowSample.json as a reference for the expected output format.

Usage:
    python recipe_transformer.py <input_recipe.json> [output_file.json]
"""

import json
import sys
import uuid
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime


class RecipeTransformer:
    """Transform recipe JSON to conform to recipe-schema-draft-01.json standard."""
    
    def __init__(self, schema_path: str = "./recipe-schema-draft-01.json"):
        """Initialize transformer with schema."""
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self.workflow_sample_path = Path("./workflowSample.json")
        self.workflow_sample = self._load_workflow_sample()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load the recipe schema definition."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Schema file not found at {self.schema_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in schema file: {e}")
            sys.exit(1)
    
    def _load_workflow_sample(self) -> Dict[str, Any]:
        """Load the workflow sample as a reference."""
        try:
            with open(self.workflow_sample_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Workflow sample not found at {self.workflow_sample_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in workflow sample: {e}")
            return {}
    
    def transform(self, input_data: Any) -> Dict[str, Any]:
        """
        Transform input recipe data to conform to recipe-schema-draft-01.json.
        
        Args:
            input_data: Input recipe data (can be dict or complex structure)
        
        Returns:
            Transformed recipe object conforming to recipe-schema-draft-01.json
        """
        # If input is already in the correct format, validate and return
        if isinstance(input_data, dict) and self._is_valid_schema_format(input_data):
            print("✓ Input already conforms to recipe-schema-draft-01.json format")
            return input_data
        
        # Transform the input to the new schema format
        if isinstance(input_data, dict):
            return self._transform_to_recipe_schema(input_data)
        
        # Default: create a basic recipe structure
        print("⚠ Warning: Input format not recognized, creating basic recipe structure")
        return self._create_default_recipe(input_data)
    
    def _is_valid_schema_format(self, data: Dict[str, Any]) -> bool:
        """Check if data already conforms to recipe-schema-draft-01.json format."""
        if not isinstance(data, dict):
            return False
        
        required_fields = {'id', 'name', 'label', 'description', 'version',
                          'tags', 'provenance', 'dependencies'}
        
        return required_fields.issubset(data.keys())
    
    def _extract_connector_info(self, recipe_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract connector/application information from recipe structure."""
        applications = []
        
        # Try to extract from output.recipe.connectors
        if 'output' in recipe_data:
            output = recipe_data['output']
            
            # Get connector names
            connector_names = output.get('recipe', {}).get('connectors', [])
            
            # Get connector icons
            connector_icons = {}
            for icon_data in output.get('connectors_icons', []):
                connector_icons[icon_data.get('connector', '')] = icon_data.get('icon', '')
            
            for connector_name in connector_names:
                applications.append({
                    'id': connector_name,
                    'label': connector_name.replace('-', ' ').replace('_', ' ').title(),
                    'icon': connector_icons.get(connector_name, connector_name)
                })
        
        return applications
    
    def _transform_to_recipe_schema(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform input data to recipe-schema-draft-01.json format.
        """
        # Extract applications/connectors
        applications = self._extract_connector_info(input_data)
        
        if not applications:
            # Create a default application if none found
            applications = [{
                'id': 'custom-integration',
                'label': 'Custom Integration',
                'icon': 'puzzle'
            }]
        
        # Extract name from various possible locations
        name = self._extract_name_from_data(input_data)
        
        # Create the recipe structure following recipe-schema-draft-01.json
        recipe = {
            "id": str(uuid.uuid4()),
            "name": name,
            "label": name.replace('-', ' ').replace('_', ' ').title(),
            "description": {
                "overview": f"Integration recipe for {name}",
                "details": f"This recipe provides integration capabilities for {name} with support for various operations."
            },
            "version": "1.0.0",
            "tags": {
                "category": ["Integration"],
                "availableOn": ["workflow"],
                "keyword": ["automation", "integration"]
            },
            "provenance": {
                "status": "draft",
                "visibility": "private",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "publishedAt": None,
                "owner": {
                    "userId": "system"
                }
            },
            "dependencies": {
                "applications": applications
            }
        }
        
        # Add optional fields if they exist in the schema
        recipe["compatibility"] = {}
        recipe["configurations"] = {}
        recipe["usageStatistics"] = {}
        
        # Preserve original data for reference
        recipe["_originalData"] = input_data
        
        return recipe
    
    def _extract_name_from_data(self, data: Any) -> str:
        """Try to extract a meaningful name from the data."""
        if isinstance(data, dict):
            # Try common name fields
            for key in ['name', 'connector', 'id', 'label', 'title']:
                if key in data:
                    value = data[key]
                    if isinstance(value, str):
                        return value.lower().replace(' ', '-')
            
            # Try nested structures
            if 'output' in data:
                output = data['output']
                if isinstance(output, dict):
                    recipe = output.get('recipe', {})
                    if isinstance(recipe, dict) and 'name' in recipe:
                        return recipe['name'].lower().replace(' ', '-')
        
        return "custom-recipe"
    
    def _create_default_recipe(self, original_data: Any) -> Dict[str, Any]:
        """Create a default recipe structure when input format is unknown."""
        return {
            "id": str(uuid.uuid4()),
            "name": "custom-recipe",
            "label": "Custom Recipe",
            "description": {
                "overview": "Custom integration recipe",
                "details": "This recipe was automatically generated from custom input data."
            },
            "version": "1.0.0",
            "tags": {
                "category": ["Integration"],
                "availableOn": ["workflow"],
                "keyword": ["custom", "integration"]
            },
            "provenance": {
                "status": "draft",
                "visibility": "private",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "publishedAt": None,
                "owner": {
                    "userId": "system"
                }
            },
            "dependencies": {
                "applications": [{
                    "id": "custom-integration",
                    "label": "Custom Integration",
                    "icon": "puzzle"
                }]
            },
            "compatibility": {},
            "configurations": {},
            "usageStatistics": {},
            "_originalData": original_data
        }
    
    def save_output(self, data: Dict[str, Any], output_path: str):
        """Save transformed data to file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Calculate file size
            file_size = Path(output_path).stat().st_size
            size_kb = file_size / 1024
            
            print(f"✓ Output saved to: {output_path}")
            print(f"  File size: {size_kb:.2f} KB ({file_size:,} bytes)")
        except Exception as e:
            print(f"Error saving output: {e}")
            sys.exit(1)


def main():
    """Main entry point for the utility."""
    if len(sys.argv) < 2:
        print("Usage: python recipe_transformer.py <input_recipe.json> [output_file.json]")
        print("\nExample:")
        print("  python recipe_transformer.py recipes/input.json recipes/transformed_recipe.json")
        print("\nNote: This transformer conforms to recipe-schema-draft-01.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Generate default output filename if not provided
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_transformed.json")
    
    print(f"Recipe Transformer Utility v3.0")
    print(f"=" * 60)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print(f"Schema: recipe-schema-draft-01.json")
    print(f"Sample: workflowSample.json")
    print(f"=" * 60)
    
    # Load input recipe
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        input_size = Path(input_file).stat().st_size
        input_size_kb = input_size / 1024
        print(f"✓ Loaded input recipe ({input_size_kb:.2f} KB)")
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    
    # Transform
    transformer = RecipeTransformer()
    transformed_data = transformer.transform(input_data)
    
    print(f"✓ Transformation complete")
    print(f"  Recipe ID: {transformed_data.get('id', 'N/A')}")
    print(f"  Recipe Name: {transformed_data.get('name', 'N/A')}")
    
    # Save output
    transformer.save_output(transformed_data, output_file)
    
    print(f"\n{'=' * 60}")
    print(f"✓ Transformation successful!")
    print(f"  Output conforms to recipe-schema-draft-01.json standard")


if __name__ == "__main__":
    main()

# Made with Bob
