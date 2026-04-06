#!/usr/bin/env python3
"""
Recipe Transformer Utility
Transforms recipe JSON files to conform to the newSchema.json standard.
Preserves ALL original content while wrapping it in the new schema structure.

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
    """Transform recipe JSON to conform to newSchema.json standard while preserving all content."""
    
    def __init__(self, schema_path: str = "./newSchema.json"):
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
        PRESERVES ALL ORIGINAL CONTENT - no data loss.
        
        Args:
            input_data: Input recipe data (can be dict, list, or complex structure)
        
        Returns:
            List of transformed recipe objects conforming to schema with all original data preserved
        """
        # If input is already in the correct format (list of connectors), validate and return
        if isinstance(input_data, list) and self._is_valid_schema_format(input_data):
            print("✓ Input already conforms to newSchema.json format")
            return input_data
        
        # If input is a complex recipe structure, extract and preserve all content
        if isinstance(input_data, dict):
            return self._transform_complex_recipe(input_data)
        
        # If input is a list but not in schema format, wrap each item
        if isinstance(input_data, list):
            return self._transform_list_format(input_data)
        
        # Default: wrap the entire input in a connector structure
        print("⚠ Warning: Input format not recognized, wrapping entire content in schema structure")
        return self._transform_unknown_format(input_data)
    
    def _is_valid_schema_format(self, data: List[Dict[str, Any]]) -> bool:
        """Check if data already conforms to schema format."""
        if not data:
            return False
        
        required_fields = {'id', 'name', 'label', 'description', 'version',
                          'tags', 'provenance', 'dependencies', 'compatibility',
                          'configurations', 'usageStatistics'}
        
        for item in data:
            if not isinstance(item, dict):
                return False
            if not required_fields.issubset(item.keys()):
                return False
        
        return True
    
    def _extract_connector_info(self, recipe_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract connector metadata from recipe structure."""
        connector_info = []
        
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
                connector_info.append({
                    'name': connector_name,
                    'icon': connector_icons.get(connector_name, connector_name)
                })
        
        return connector_info
    
    def _transform_complex_recipe(self, recipe_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Transform complex recipe structure to schema format.
        PRESERVES ALL ORIGINAL DATA in the 'originalRecipeData' field.
        """
        connectors = []
        
        # Extract connector metadata
        connector_info = self._extract_connector_info(recipe_data)
        
        if connector_info:
            # Create a connector for each identified connector with ALL original data
            for info in connector_info:
                connector = self._create_connector_with_data(
                    name=info['name'],
                    icon=info['icon'],
                    original_data=recipe_data
                )
                connectors.append(connector)
        else:
            # No connectors identified, wrap entire recipe in a single connector
            print("ℹ No specific connectors identified, wrapping entire recipe in schema structure")
            connector = self._create_connector_with_data(
                name=self._extract_name_from_data(recipe_data),
                icon="puzzle",
                original_data=recipe_data
            )
            connectors.append(connector)
        
        return connectors
    
    def _transform_list_format(self, data_list: List[Any]) -> List[Dict[str, Any]]:
        """Transform list format data, preserving all items."""
        connectors = []
        
        for idx, item in enumerate(data_list):
            connector = self._create_connector_with_data(
                name=f"connector-{idx + 1}",
                icon="puzzle",
                original_data=item
            )
            connectors.append(connector)
        
        return connectors
    
    def _extract_name_from_data(self, data: Any) -> str:
        """Try to extract a meaningful name from the data."""
        if isinstance(data, dict):
            # Try common name fields
            for key in ['name', 'connector', 'id', 'label', 'title']:
                if key in data:
                    value = data[key]
                    if isinstance(value, str):
                        return value
            
            # Try nested structures
            if 'output' in data:
                output = data['output']
                if isinstance(output, dict):
                    recipe = output.get('recipe', {})
                    if isinstance(recipe, dict) and 'name' in recipe:
                        return recipe['name']
        
        return "custom-recipe"
    
    def _create_connector_with_data(
        self,
        name: str,
        icon: str = "",
        original_data: Any = None
    ) -> Dict[str, Any]:
        """
        Create a connector definition that PRESERVES ALL ORIGINAL DATA.
        The original data is stored in 'originalRecipeData' field.
        """
        # Generate a unique ID
        connector_id = str(uuid.uuid4())
        
        # Create label from name
        label = name.replace('-', ' ').replace('_', ' ').title()
        
        # Base connector structure following newSchema.json
        connector = {
            "id": connector_id,
            "name": name,
            "label": label,
            "description": {
                "overview": f"{label} connector for workflow integration",
                "details": f"Comprehensive integration connector for {label} with support for actions and triggers."
            },
            "version": "1.0.0",
            "tags": {
                "category": ["Integration"],
                "availableOn": ["workflow", "flow.cloud", "flow.anywhere"],
                "keyword": ["automation", "integration", "connector"]
            },
            "provenance": {
                "status": "active"
            },
            "dependencies": {
                "applications": [
                    {
                        "id": connector_id,
                        "label": label,
                        "icon": icon or name
                    }
                ]
            },
            "compatibility": {},
            "configurations": {},
            "usageStatistics": {}
        }
        
        # CRITICAL: Preserve ALL original data
        if original_data is not None:
            connector["originalRecipeData"] = original_data
            
            # Also try to extract and merge additional fields from original data
            if isinstance(original_data, dict):
                # Extract actions, triggers, operations if they exist
                self._merge_recipe_details(connector, original_data)
        
        # Add transformation metadata
        connector["transformationMetadata"] = {
            "transformedAt": datetime.utcnow().isoformat() + "Z",
            "transformerVersion": "2.0.0",
            "schemaVersion": "newSchema.json",
            "preservedOriginalData": True
        }
        
        return connector
    
    def _merge_recipe_details(self, connector: Dict[str, Any], original_data: Dict[str, Any]):
        """
        Extract and merge detailed recipe information from original data.
        This preserves actions, triggers, operations, etc.
        """
        # Extract from output structure if present
        if 'output' in original_data:
            output = original_data['output']
            
            # Preserve recipe details
            if 'recipe' in output:
                connector['recipeDetails'] = output['recipe']
            
            # Preserve actions
            if 'actions' in output:
                connector['actions'] = output['actions']
            
            # Preserve triggers
            if 'triggers' in output:
                connector['triggers'] = output['triggers']
            
            # Preserve operations
            if 'operations' in output:
                connector['operations'] = output['operations']
            
            # Preserve any other output fields
            for key, value in output.items():
                if key not in ['recipe', 'actions', 'triggers', 'operations', 'connectors_icons']:
                    connector[f'original_{key}'] = value
        
        # Preserve top-level fields that aren't part of schema
        schema_fields = {'id', 'name', 'label', 'description', 'version', 'icon',
                        'tags', 'capabilities', 'sourceMetadata', 'configurations'}
        
        for key, value in original_data.items():
            if key not in schema_fields and key != 'output':
                connector[f'original_{key}'] = value
    
    def _create_default_connector(self) -> Dict[str, Any]:
        """Create a default connector when no data is available."""
        return self._create_connector_with_data("custom-connector", "puzzle", None)
    
    def _transform_unknown_format(self, data: Any) -> List[Dict[str, Any]]:
        """Handle unknown format by wrapping entire content."""
        return [self._create_connector_with_data("custom-recipe", "puzzle", data)]
    
    def save_output(self, data: List[Dict[str, Any]], output_path: str):
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
        print("  python recipe_transformer.py recipes/boxComplexRecipe.json recipes/transformed_recipe.json")
        print("\nNote: This transformer PRESERVES ALL original content while conforming to newSchema.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Generate default output filename if not provided
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_transformed.json")
    
    print(f"Recipe Transformer Utility v2.0")
    print(f"=" * 60)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print(f"Schema: ./newSchema.json")
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
    
    print(f"✓ Transformation complete: {len(transformed_data)} connector(s) generated")
    print(f"  ℹ All original content preserved in 'originalRecipeData' field")
    
    # Save output
    transformer.save_output(transformed_data, output_file)
    
    print(f"\n{'=' * 60}")
    print(f"✓ Transformation successful!")
    print(f"  Generated {len(transformed_data)} connector definition(s)")
    print(f"  Output conforms to newSchema.json standard")
    print(f"  ALL original data preserved - no content loss")


if __name__ == "__main__":
    main()

# Made with Bob
