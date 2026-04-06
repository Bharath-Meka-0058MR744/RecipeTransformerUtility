#!/usr/bin/env python3
"""
Recipe Transformer Web Application
Flask backend for transforming recipe JSON schemas.
"""

import json
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Add parent directory to path to import RecipeTransformer
sys.path.insert(0, str(Path(__file__).parent.parent))
from recipe_transformer import RecipeTransformer

app = Flask(__name__)
CORS(app)

# Initialize transformer with schema from parent directory
SCHEMA_PATH = Path(__file__).parent.parent / "recipe-schema-draft-01.json"
transformer = RecipeTransformer(schema_path=str(SCHEMA_PATH))


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/transform', methods=['POST'])
def transform_recipe():
    """
    Transform recipe JSON to conform to recipe-schema-draft-01.json.
    
    Expects JSON payload with 'input' field containing the recipe data.
    Returns transformed schema or error message.
    """
    try:
        # Get input data from request
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'success': False,
                'error': 'No input data provided. Please provide JSON with "input" field.'
            }), 400
        
        input_data = data['input']
        
        # Parse input if it's a string
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid JSON format: {str(e)}'
                }), 400
        
        # Transform the data
        transformed_data = transformer.transform(input_data)
        
        return jsonify({
            'success': True,
            'output': transformed_data,
            'message': f'Successfully transformed recipe'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Transformation error: {str(e)}'
        }), 500


@app.route('/api/schema', methods=['GET'])
def get_schema():
    """Return the recipe-schema-draft-01.json for reference."""
    try:
        return jsonify({
            'success': True,
            'schema': transformer.schema
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error loading schema: {str(e)}'
        }), 500


@app.route('/api/validate', methods=['POST'])
def validate_schema():
    """
    Validate if input conforms to recipe-schema-draft-01.json format.
    
    Expects JSON payload with 'input' field.
    Returns validation result.
    """
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'success': False,
                'error': 'No input data provided'
            }), 400
        
        input_data = data['input']
        
        # Parse input if it's a string
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError as e:
                return jsonify({
                    'success': False,
                    'valid': False,
                    'error': f'Invalid JSON format: {str(e)}'
                }), 400
        
        # Check if it's a dict and validate format
        if isinstance(input_data, dict):
            is_valid = transformer._is_valid_schema_format(input_data)
            return jsonify({
                'success': True,
                'valid': is_valid,
                'message': 'Input conforms to recipe-schema-draft-01.json' if is_valid else 'Input does not conform to schema'
            })
        else:
            return jsonify({
                'success': True,
                'valid': False,
                'message': 'Input must be a recipe object (dictionary)'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Validation error: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Recipe Transformer Web Application")
    print("=" * 60)
    print(f"Schema loaded from: {SCHEMA_PATH}")
    print("Starting Flask server...")
    print("Access the application at: http://localhost:5001")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)

# Made with Bob
