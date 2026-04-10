#!/usr/bin/env python3
"""
Apply Recipe Mapping Utility
Applies a custom mapping configuration to transform a recipe to match specific requirements.

Usage:
    python apply_recipe_mapping.py <input_recipe.json> <mapping.json> [output_file.json]
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_json(file_path: str) -> dict:
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: dict, file_path: str):
    """Save JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def extract_flow_id(input_data: dict) -> str:
    """Extract flow UID from input data."""
    try:
        return input_data['output']['recipe']['flow']['uid']
    except (KeyError, TypeError):
        return ''


def apply_mapping(input_data: dict, mapping: dict) -> dict:
    """Apply mapping configuration to input data."""
    
    # Use flow UID as recipe ID if available
    flow_id = extract_flow_id(input_data)
    recipe_id = flow_id if flow_id else mapping.get('id', 'custom-recipe-id')
    
    # Build the transformed recipe
    recipe = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "id": recipe_id,
        "name": mapping.get('name', 'custom-recipe'),
        "label": mapping.get('label', 'Custom Recipe'),
        "description": mapping.get('description', {
            "overview": "Custom recipe",
            "details": "Custom recipe details"
        }),
        "version": "1.0.0",
        "tags": mapping.get('tags', {
            "category": ["Integration"],
            "availableOn": ["workflow"],
            "keyword": []
        }),
        "provenance": {
            "status": mapping.get('provenance', {}).get('status', 'published'),
            "visibility": mapping.get('provenance', {}).get('visibility', 'public'),
            "createdAt": mapping.get('provenance', {}).get('createdAt', datetime.utcnow().isoformat() + 'Z'),
            "updatedAt": mapping.get('provenance', {}).get('updatedAt', datetime.utcnow().isoformat() + 'Z'),
            "publishedAt": mapping.get('provenance', {}).get('publishedAt', datetime.utcnow().isoformat() + 'Z'),
            "owner": mapping.get('provenance', {}).get('owner', {"userId": "IBM"})
        },
        "dependencies": {
            "applications": [],
            "interactions": []
        },
        "compatibility": mapping.get('compatibility', {}),
        "configurations": mapping.get('configurations', {}),
        "usageStatistics": mapping.get('usageStatistics', {})
    }
    
    # Apply application mappings
    app_mappings = mapping.get('applicationMappings', {})
    for app_name, app_config in app_mappings.items():
        recipe['dependencies']['applications'].append(app_config)
    
    # Apply interaction mappings
    interaction_mappings = mapping.get('interactionMappings', {})
    for interaction_name, interaction_config in interaction_mappings.items():
        recipe['dependencies']['interactions'].append(interaction_config)
    
    return recipe


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Apply Recipe Mapping Utility")
        print("=" * 70)
        print("\nApplies a custom mapping configuration to transform a recipe")
        print("\nUsage:")
        print("  python apply_recipe_mapping.py <input_recipe.json> <mapping.json> [output_file.json]")
        print("\nExample:")
        print("  python apply_recipe_mapping.py input.json mapping.json output.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    mapping_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Generate default output filename if not provided
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_mapped.json")
    
    print("Apply Recipe Mapping Utility")
    print("=" * 70)
    print(f"Input:   {input_file}")
    print(f"Mapping: {mapping_file}")
    print(f"Output:  {output_file}")
    print("=" * 70)
    
    # Load files
    try:
        print("✓ Loading input recipe...")
        input_data = load_json(input_file)
        input_size = Path(input_file).stat().st_size / 1024
        print(f"  Size: {input_size:.2f} KB")
        
        print("✓ Loading mapping configuration...")
        mapping = load_json(mapping_file)
        
    except FileNotFoundError as e:
        print(f"✗ Error: File not found: {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON: {e}")
        sys.exit(1)
    
    # Apply mapping
    print("\n✓ Applying mapping...")
    transformed = apply_mapping(input_data, mapping)
    
    # Display results
    print(f"\nTransformed Recipe:")
    print(f"  ID:      {transformed.get('id')}")
    print(f"  Name:    {transformed.get('name')}")
    print(f"  Label:   {transformed.get('label')}")
    print(f"  Status:  {transformed.get('provenance', {}).get('status')}")
    
    deps = transformed.get('dependencies', {})
    apps = deps.get('applications', [])
    interactions = deps.get('interactions', [])
    
    print(f"\nDependencies:")
    print(f"  Applications: {len(apps)}")
    for app in apps:
        print(f"    - {app.get('label')} ({app.get('framework', 'N/A')})")
    
    if interactions:
        print(f"  Interactions: {len(interactions)}")
        actions = [i for i in interactions if i.get('type') == 'action']
        triggers = [i for i in interactions if i.get('type') == 'trigger']
        print(f"    - Actions:  {len(actions)}")
        print(f"    - Triggers: {len(triggers)}")
    
    # Save output
    print(f"\n✓ Saving output...")
    save_json(transformed, output_file)
    output_size = Path(output_file).stat().st_size / 1024
    print(f"  Size: {output_size:.2f} KB")
    
    print(f"\n{'=' * 70}")
    print(f"✓ Mapping applied successfully!")
    print(f"  Output saved to: {output_file}")


if __name__ == "__main__":
    main()

# Made with Bob
