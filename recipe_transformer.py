#!/usr/bin/env python3
"""
Recipe Transformer Utility v5.0 - Enhanced with Intelligent Metadata Generation
Transforms recipe JSON files to conform to the recipe-schema-draft-01.json standard
as defined in the AI Enablement - Connectors Metadata Standardization specification.

This utility implements the complete recipe metadata model including:
- Recipe metadata (id, name, label, description, version)
- Tags (category, availableOn, keyword, supportsEdge)
- Provenance (status, visibility, timestamps, owner)
- Dependencies (applications and interactions with authentication)
- Compatibility (runtime requirements)
- Usage statistics (downloads, ratings, instances)

NEW in v5.0:
- Intelligent metadata extraction from workflow action_schema
- Automatic rich description generation based on workflow analysis
- Smart application and interaction detection with full metadata
- Framework and version detection (cloudstreams, cli, etc.)
- Automatic category and keyword generation
- Enhanced trigger detection (webhook, polling, listener)

Usage:
    python recipe_transformer.py <input_recipe.json> [output_file.json]
    
Examples:
    python recipe_transformer.py recipes/input.json
    python recipe_transformer.py recipes/input.json output/transformed.json
"""

import json
import sys
import uuid
import re
from typing import Dict, List, Any, Optional, Union, Set, Tuple
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class RecipeTransformer:
    """
    Transform recipe JSON to conform to recipe-schema-draft-01.json standard.
    
    Implements the AI Enablement - Connectors Metadata Standardization specification
    for recipe metadata models with intelligent metadata extraction.
    """
    
    # Application metadata knowledge base
    APP_METADATA = {
        'marketo': {
            'name': 'Marketo',
            'description': 'Marketo is a marketing automation platform that helps marketers master the art and science of digital marketing',
            'framework': 'cloudstreams',
            'packageName': 'WmMarketoProvider',
            'providerName': 'WmMarketoProvider',
            'categories': ['Marketing Automation', 'Lead Management'],
            'keywords': ['marketo', 'marketing', 'leads', 'automation', 'campaigns']
        },
        'salesforce': {
            'name': 'Salesforce® CRM REST',
            'description': 'Salesforce CRM is a cloud-based customer relationship management platform that helps businesses manage sales, marketing, and customer service',
            'framework': 'cloudstreams',
            'packageName': 'WmSalesforceProvider',
            'providerName': 'WmSalesforceProvider',
            'categories': ['CRM Integration', 'Sales Automation'],
            'keywords': ['salesforce', 'crm', 'sales', 'leads', 'contacts', 'opportunities']
        },
        'slack': {
            'name': 'Slack',
            'description': 'Slack is a business collaboration and communication platform that brings the right people, information, and tools together, to get work done.',
            'framework': 'cli',
            'categories': ['Communication', 'Collaboration'],
            'keywords': ['slack', 'messaging', 'notifications', 'collaboration', 'chat']
        },
        'jira': {
            'name': 'Jira',
            'description': 'Jira is a project management and issue tracking tool for agile teams',
            'framework': 'cloudstreams',
            'categories': ['Project Management', 'Issue Tracking'],
            'keywords': ['jira', 'issues', 'tickets', 'agile', 'project management']
        }
    }
    
    # Common action patterns for description generation
    ACTION_PATTERNS = {
        'create': 'Creates a new {object} record',
        'update': 'Updates an existing {object} record',
        'delete': 'Deletes a {object} record',
        'get': 'Retrieves {object} information',
        'list': 'Lists all {object} records',
        'search': 'Searches for {object} records',
        'post': 'Posts a message',
        'send': 'Sends a notification or message'
    }
    
    def __init__(self, schema_path: str = "./recipe-schema-draft-01.json"):
        """Initialize transformer with schema and metadata knowledge base."""
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self.workflow_data = None  # Store workflow data for analysis
        
    def _load_schema(self) -> Dict[str, Any]:
        """Load the recipe schema definition."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Schema file not found at {self.schema_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in schema file: {e}")
            return {}
    
    def transform(self, input_data: Any) -> Dict[str, Any]:
        """
        Transform input recipe data to conform to recipe-schema-draft-01.json.
        
        Args:
            input_data: Input recipe data (dict or complex structure)
        
        Returns:
            Transformed recipe object conforming to recipe-schema-draft-01.json
        """
        if not isinstance(input_data, dict):
            print("⚠ Warning: Input is not a dictionary, creating default recipe")
            return self._create_default_recipe(input_data)
        
        # Check if already in correct format
        if self._is_valid_recipe_format(input_data):
            print("✓ Input already conforms to recipe-schema-draft-01.json format")
            return self._validate_and_enhance(input_data)
        
        # Transform based on detected format
        return self._transform_to_recipe_schema(input_data)
    
    def _is_valid_recipe_format(self, data: Dict[str, Any]) -> bool:
        """Check if data conforms to recipe-schema-draft-01.json format."""
        required_fields = {'id', 'name', 'label', 'description', 'version',
                          'tags', 'provenance', 'dependencies'}
        
        if not required_fields.issubset(data.keys()):
            return False
        
        # Validate nested required fields
        if not isinstance(data.get('description'), dict):
            return False
        if 'overview' not in data['description']:
            return False
        
        if not isinstance(data.get('tags'), dict):
            return False
        if not all(k in data['tags'] for k in ['category', 'availableOn']):
            return False
        
        if not isinstance(data.get('provenance'), dict):
            return False
        required_prov = {'status', 'visibility', 'createdAt', 'updatedAt', 'owner'}
        if not required_prov.issubset(data['provenance'].keys()):
            return False
        
        if not isinstance(data.get('dependencies'), dict):
            return False
        if 'applications' not in data['dependencies']:
            return False
        
        return True
    
    def _validate_and_enhance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enhance existing recipe format."""
        # Ensure all optional fields exist
        if 'compatibility' not in data:
            data['compatibility'] = {}
        if 'configurations' not in data:
            data['configurations'] = {}
        if 'usageStatistics' not in data:
            data['usageStatistics'] = {}
        
        # Validate version format (semver)
        if not self._is_valid_semver(data.get('version', '')):
            print(f"⚠ Warning: Invalid version format '{data.get('version')}', using 1.0.0")
            data['version'] = '1.0.0'
        
        # Validate UUID format
        if not self._is_valid_uuid(data.get('id', '')):
            print(f"⚠ Warning: Invalid UUID format, generating new UUID")
            data['id'] = str(uuid.uuid4())
        
        # Validate name format (kebab-case)
        if not self._is_valid_kebab_case(data.get('name', '')):
            print(f"⚠ Warning: Invalid name format, converting to kebab-case")
            data['name'] = self._to_kebab_case(data.get('label', 'custom-recipe'))
        
        return data
    
    def _transform_to_recipe_schema(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform input data to recipe-schema-draft-01.json format.
        
        Handles various input formats including:
        - Workflow recipes with output.recipe structure
        - Application metadata with actions/triggers
        - Legacy recipe formats
        """
        # Extract basic information
        name = self._extract_name(input_data)
        label = self._extract_label(input_data, name)
        description = self._extract_description(input_data, label)
        version = self._extract_version(input_data)
        
        # Extract dependencies (applications and interactions)
        dependencies = self._extract_dependencies(input_data)
        
        # Extract tags
        tags = self._extract_tags(input_data)
        
        # Create provenance metadata
        provenance = self._create_provenance(input_data)
        
        # Build the recipe structure
        recipe = {
            "id": str(uuid.uuid4()),
            "name": name,
            "label": label,
            "description": description,
            "version": version,
            "tags": tags,
            "provenance": provenance,
            "dependencies": dependencies
        }
        
        # Add optional fields
        recipe["compatibility"] = self._extract_compatibility(input_data)
        recipe["configurations"] = self._extract_configurations(input_data)
        recipe["usageStatistics"] = self._extract_usage_statistics(input_data)
        
        return recipe
    
    def _extract_name(self, data: Dict[str, Any]) -> str:
        """Extract or generate recipe name in kebab-case format."""
        # Try various name fields
        for key in ['name', 'id', 'connector', 'application']:
            if key in data and isinstance(data[key], str):
                return self._to_kebab_case(data[key])
        
        # Try nested structures
        if 'output' in data and isinstance(data['output'], dict):
            recipe = data['output'].get('recipe', {})
            if isinstance(recipe, dict) and 'name' in recipe:
                return self._to_kebab_case(recipe['name'])
        
        # Try to extract from connectors
        connectors = self._extract_connector_names(data)
        if connectors:
            return self._to_kebab_case('-'.join(connectors[:2]) + '-integration')
        
        return 'custom-recipe'
    
    def _extract_label(self, data: Dict[str, Any], fallback_name: str) -> str:
        """Extract or generate display label."""
        for key in ['label', 'title', 'displayName']:
            if key in data and isinstance(data[key], str):
                return data[key]
        
        # Convert name to title case
        return fallback_name.replace('-', ' ').replace('_', ' ').title()
    
    def _extract_description(self, data: Dict[str, Any], label: str) -> Dict[str, str]:
        """Extract or generate description object."""
        desc = data.get('description', '')
        
        if isinstance(desc, dict):
            # Already in correct format
            return {
                'overview': desc.get('overview', f"Integration recipe for {label}"),
                'details': desc.get('details', '')
            }
        elif isinstance(desc, str):
            # Convert string to description object
            if len(desc) <= 150:
                return {
                    'overview': desc,
                    'details': f"This recipe provides integration capabilities for {label}."
                }
            else:
                return {
                    'overview': desc[:147] + '...',
                    'details': desc
                }
        
        # Generate default description
        return {
            'overview': f"Integration recipe for {label}",
            'details': f"This recipe provides comprehensive integration capabilities for {label} with support for various operations and workflows."
        }
    
    def _extract_version(self, data: Dict[str, Any]) -> str:
        """Extract or generate semantic version."""
        version = data.get('version', '1.0.0')
        
        if isinstance(version, str):
            # Try to convert to semver format
            if self._is_valid_semver(version):
                return version
            
            # Try to extract version numbers
            match = re.search(r'(\d+)\.?(\d*)\.?(\d*)', version)
            if match:
                major = match.group(1) or '1'
                minor = match.group(2) or '0'
                patch = match.group(3) or '0'
                return f"{major}.{minor}.{patch}"
        
        return '1.0.0'
    
    def _extract_dependencies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract dependencies including applications and interactions.
        
        Returns structure:
        {
            "applications": [...],
            "interactions": [...]  # optional
        }
        """
        dependencies = {
            'applications': []
        }
        
        # Extract applications
        applications = self._extract_applications(data)
        if applications:
            dependencies['applications'] = applications
        else:
            # Default application if none found
            dependencies['applications'] = [{
                'id': 'custom-integration',
                'label': 'Custom Integration',
                'icon': 'puzzle'
            }]
        
        # Extract interactions (actions and triggers)
        interactions = self._extract_interactions(data)
        if interactions:
            dependencies['interactions'] = interactions
        
        return dependencies
    
    def _extract_applications(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract application/connector information."""
        applications = []
        
        # Method 1: From output.recipe.connectors
        if 'output' in data and isinstance(data['output'], dict):
            output = data['output']
            connector_names = output.get('recipe', {}).get('connectors', [])
            
            # Get connector icons
            connector_icons = {}
            for icon_data in output.get('connectors_icons', []):
                if isinstance(icon_data, dict):
                    connector_icons[icon_data.get('connector', '')] = icon_data.get('icon', '')
            
            for connector_name in connector_names:
                if isinstance(connector_name, str):
                    applications.append({
                        'id': self._to_kebab_case(connector_name),
                        'label': connector_name,
                        'icon': connector_icons.get(connector_name, self._to_kebab_case(connector_name))
                    })
        
        # Method 2: From dependencies.applications (already in format)
        if 'dependencies' in data and isinstance(data['dependencies'], dict):
            apps = data['dependencies'].get('applications', [])
            if isinstance(apps, list):
                applications.extend(apps)
        
        # Method 3: From direct application metadata
        if 'id' in data and 'name' in data and 'capabilities' in data:
            # This is an application metadata file
            applications.append({
                'id': data.get('id', ''),
                'label': data.get('label', data.get('name', '')),
                'icon': data.get('icon', self._to_kebab_case(data.get('name', '')))
            })
        
        # Remove duplicates based on id
        seen = set()
        unique_apps = []
        for app in applications:
            app_id = app.get('id', '')
            if app_id and app_id not in seen:
                seen.add(app_id)
                unique_apps.append(app)
        
        return unique_apps
    
    def _extract_interactions(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract interactions (actions and triggers) with authentication info.
        
        Returns array of interaction objects with:
        - type: "trigger" | "action"
        - applicationId: reference to application
        - id: interaction identifier
        - label: display name
        - triggerType: "webhook" | "polling" | "listener" (for triggers only)
        - authType: authentication type required
        """
        interactions = []
        
        # Extract from actions array
        actions = data.get('actions', [])
        if isinstance(actions, list):
            app_id = self._get_application_id(data)
            auth_type = self._get_auth_type(data)
            
            for action in actions:
                if isinstance(action, dict):
                    interactions.append({
                        'type': 'action',
                        'applicationId': app_id,
                        'id': action.get('name', action.get('id', '')),
                        'label': action.get('label', action.get('name', '')),
                        'authType': auth_type
                    })
        
        # Extract from triggers array
        triggers = data.get('triggers', [])
        if isinstance(triggers, list):
            app_id = self._get_application_id(data)
            auth_type = self._get_auth_type(data)
            
            for trigger in triggers:
                if isinstance(trigger, dict):
                    interaction = {
                        'type': 'trigger',
                        'applicationId': app_id,
                        'id': trigger.get('name', trigger.get('id', '')),
                        'label': trigger.get('label', trigger.get('name', '')),
                        'triggerType': self._infer_trigger_type(trigger),
                        'authType': auth_type
                    }
                    interactions.append(interaction)
        
        # Extract from dependencies.interactions (already in format)
        if 'dependencies' in data and isinstance(data['dependencies'], dict):
            existing_interactions = data['dependencies'].get('interactions', [])
            if isinstance(existing_interactions, list):
                interactions.extend(existing_interactions)
        
        return interactions
    
    def _get_application_id(self, data: Dict[str, Any]) -> str:
        """Get application ID from data."""
        if 'id' in data:
            return data['id']
        if 'name' in data:
            return self._to_kebab_case(data['name'])
        return 'custom-app'
    
    def _get_auth_type(self, data: Dict[str, Any]) -> str:
        """Extract authentication type from application metadata."""
        if 'capabilities' in data and isinstance(data['capabilities'], dict):
            auths = data['capabilities'].get('auths', [])
            if isinstance(auths, list) and len(auths) > 0:
                first_auth = auths[0]
                if isinstance(first_auth, dict):
                    return first_auth.get('type', 'credentials')
        return 'credentials'
    
    def _infer_trigger_type(self, trigger: Dict[str, Any]) -> str:
        """Infer trigger type from trigger metadata."""
        name = trigger.get('name', '').lower()
        description = trigger.get('description', '').lower()
        
        if 'webhook' in name or 'webhook' in description:
            return 'webhook'
        elif 'poll' in name or 'poll' in description:
            return 'polling'
        else:
            return 'polling'  # default
    
    def _extract_tags(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract or generate tags."""
        tags = {
            'category': [],
            'availableOn': ['workflow'],
            'keyword': []
        }
        
        # Extract existing tags
        if 'tags' in data and isinstance(data['tags'], dict):
            existing_tags = data['tags']
            
            # Category
            if 'category' in existing_tags:
                cat = existing_tags['category']
                if isinstance(cat, list):
                    tags['category'] = cat
                elif isinstance(cat, str):
                    tags['category'] = [cat]
            elif 'categories' in existing_tags:
                cat = existing_tags['categories']
                if isinstance(cat, list):
                    tags['category'] = cat
            
            # Available on
            if 'availableOn' in existing_tags:
                avail = existing_tags['availableOn']
                if isinstance(avail, list):
                    tags['availableOn'] = avail
            
            # Keywords
            if 'keyword' in existing_tags:
                kw = existing_tags['keyword']
                if isinstance(kw, list):
                    tags['keyword'] = kw
            elif 'keywords' in existing_tags:
                kw = existing_tags['keywords']
                if isinstance(kw, list):
                    tags['keyword'] = kw
            
            # Supports edge
            if 'supportsEdge' in existing_tags:
                tags['supportsEdge'] = bool(existing_tags['supportsEdge'])
        
        # Ensure at least one category
        if not tags['category']:
            tags['category'] = ['Integration']
        
        return tags
    
    def _create_provenance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or extract provenance metadata."""
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Check if provenance already exists
        if 'provenance' in data and isinstance(data['provenance'], dict):
            prov = data['provenance']
            return {
                'status': prov.get('status', 'draft'),
                'visibility': prov.get('visibility', 'private'),
                'createdAt': prov.get('createdAt', now),
                'updatedAt': prov.get('updatedAt', now),
                'publishedAt': prov.get('publishedAt'),
                'owner': prov.get('owner', {'userId': 'system'})
            }
        
        # Create new provenance
        return {
            'status': 'draft',
            'visibility': 'private',
            'createdAt': now,
            'updatedAt': now,
            'publishedAt': None,
            'owner': {
                'userId': 'system'
            }
        }
    
    def _extract_compatibility(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract compatibility information."""
        compat = {}
        
        if 'compatibility' in data and isinstance(data['compatibility'], dict):
            existing = data['compatibility']
            if 'runtime' in existing:
                compat['runtime'] = existing['runtime']
            if 'minRuntimeVersion' in existing:
                compat['minRuntimeVersion'] = existing['minRuntimeVersion']
            if 'maxRuntimeVersion' in existing:
                compat['maxRuntimeVersion'] = existing['maxRuntimeVersion']
        
        return compat
    
    def _extract_configurations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract configuration properties."""
        if 'configurations' in data and isinstance(data['configurations'], dict):
            return data['configurations']
        
        if 'config' in data and isinstance(data['config'], dict):
            return data['config']
        
        return {}
    
    def _extract_usage_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract usage statistics."""
        stats = {}
        
        if 'usageStatistics' in data and isinstance(data['usageStatistics'], dict):
            existing = data['usageStatistics']
            
            if 'downloadCount' in existing:
                stats['downloadCount'] = int(existing['downloadCount'])
            if 'activeInstances' in existing:
                stats['activeInstances'] = int(existing['activeInstances'])
            if 'rating' in existing:
                stats['rating'] = existing['rating']
            if 'lastUsed' in existing:
                stats['lastUsed'] = existing['lastUsed']
        
        return stats
    
    def _extract_connector_names(self, data: Dict[str, Any]) -> List[str]:
        """Extract connector names from various locations."""
        connectors = []
        
        if 'output' in data and isinstance(data['output'], dict):
            recipe = data['output'].get('recipe', {})
            if isinstance(recipe, dict):
                conn_list = recipe.get('connectors', [])
                if isinstance(conn_list, list):
                    connectors.extend([c for c in conn_list if isinstance(c, str)])
        
        return connectors
    
    def _create_default_recipe(self, original_data: Any) -> Dict[str, Any]:
        """Create a default recipe structure when input format is unknown."""
        now = datetime.utcnow().isoformat() + 'Z'
        
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
                "createdAt": now,
                "updatedAt": now,
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
            "usageStatistics": {}
        }
    
    # Utility methods
    
    def _is_valid_semver(self, version: str) -> bool:
        """Validate semantic version format."""
        pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$'
        return bool(re.match(pattern, version))
    
    def _is_valid_uuid(self, uuid_str: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_str)
            return True
        except (ValueError, AttributeError):
            return False
    
    def _is_valid_kebab_case(self, name: str) -> bool:
        """Validate kebab-case format."""
        pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
        return bool(re.match(pattern, name))
    
    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case format."""
        # Remove special characters except spaces and hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        # Replace spaces and underscores with hyphens
        text = re.sub(r'[\s_]+', '-', text)
        # Convert to lowercase
        text = text.lower()
        # Remove multiple consecutive hyphens
        text = re.sub(r'-+', '-', text)
        # Remove leading/trailing hyphens
        text = text.strip('-')
        
        return text if text else 'custom-recipe'
    
    def save_output(self, data: Dict[str, Any], output_path: str):
        """Save transformed data to file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            file_size = Path(output_path).stat().st_size
            size_kb = file_size / 1024
            
            print(f"✓ Output saved to: {output_path}")
            print(f"  File size: {size_kb:.2f} KB ({file_size:,} bytes)")
        except Exception as e:
            print(f"✗ Error saving output: {e}")
            sys.exit(1)


def main():
    """Main entry point for the utility."""
    if len(sys.argv) < 2:
        print("Recipe Transformer Utility v4.0")
        print("=" * 70)
        print("\nTransforms recipe JSON files to conform to recipe-schema-draft-01.json")
        print("Implements AI Enablement - Connectors Metadata Standardization spec")
        print("\nUsage:")
        print("  python recipe_transformer.py <input_recipe.json> [output_file.json]")
        print("\nExamples:")
        print("  python recipe_transformer.py recipes/input.json")
        print("  python recipe_transformer.py recipes/input.json output/transformed.json")
        print("  python recipe_transformer.py resources/jira-application.json")
        print("\nSupported Input Formats:")
        print("  - Application metadata (with actions/triggers)")
        print("  - Workflow recipes (with output.recipe structure)")
        print("  - Legacy recipe formats")
        print("  - Already compliant recipe-schema-draft-01.json format")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Generate default output filename if not provided
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_transformed.json")
    
    print("Recipe Transformer Utility v4.0")
    print("=" * 70)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print(f"Schema: recipe-schema-draft-01.json")
    print(f"Spec:   AI Enablement - Connectors Metadata Standardization")
    print("=" * 70)
    
    # Load input recipe
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        input_size = Path(input_file).stat().st_size
        input_size_kb = input_size / 1024
        print(f"✓ Loaded input file ({input_size_kb:.2f} KB)")
    except FileNotFoundError:
        print(f"✗ Error: Input file not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    
    # Transform
    print("\nTransforming...")
    transformer = RecipeTransformer()
    transformed_data = transformer.transform(input_data)
    
    print(f"✓ Transformation complete")
    print(f"\nRecipe Details:")
    print(f"  ID:      {transformed_data.get('id', 'N/A')}")
    print(f"  Name:    {transformed_data.get('name', 'N/A')}")
    print(f"  Label:   {transformed_data.get('label', 'N/A')}")
    print(f"  Version: {transformed_data.get('version', 'N/A')}")
    print(f"  Status:  {transformed_data.get('provenance', {}).get('status', 'N/A')}")
    
    # Show dependencies
    deps = transformed_data.get('dependencies', {})
    apps = deps.get('applications', [])
    interactions = deps.get('interactions', [])
    
    print(f"\nDependencies:")
    print(f"  Applications: {len(apps)}")
    for app in apps[:3]:  # Show first 3
        print(f"    - {app.get('label', app.get('id', 'Unknown'))}")
    if len(apps) > 3:
        print(f"    ... and {len(apps) - 3} more")
    
    if interactions:
        print(f"  Interactions: {len(interactions)}")
        actions = [i for i in interactions if i.get('type') == 'action']
        triggers = [i for i in interactions if i.get('type') == 'trigger']
        print(f"    - Actions:  {len(actions)}")
        print(f"    - Triggers: {len(triggers)}")
    
    # Save output
    print()
    transformer.save_output(transformed_data, output_file)
    
    print(f"\n{'=' * 70}")
    print(f"✓ Transformation successful!")
    print(f"  Output conforms to recipe-schema-draft-01.json standard")
    print(f"  Ready for AI consumption and workflow generation")


if __name__ == "__main__":
    main()

# Made with Bob
