#!/usr/bin/env python3
"""
Material Selector Web Application.

A Flask web application for finding and evaluating materials based on user requirements.
"""

import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scrapers import MatWebScraper, AZoMScraper
from material_evaluator import MaterialEvaluator

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Initialize scrapers and evaluator
scrapers = {
    'matweb': MatWebScraper(),
    'azom': AZoMScraper()
}
evaluator = MaterialEvaluator()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_materials():
    """Search for materials based on user requirements."""
    try:
        data = request.get_json()

        # Extract requirements
        application = data.get('application', '')
        material_type = data.get('material_type', '')
        characteristics = data.get('characteristics', [])
        properties = data.get('properties', {})

        # Build search query
        search_query = material_type if material_type else application
        if not search_query and characteristics:
            search_query = ' '.join(characteristics[:2])

        if not search_query:
            return jsonify({
                'success': False,
                'error': 'Please provide at least one search criterion'
            }), 400

        # Search materials
        all_results = []

        # Search MatWeb
        try:
            matweb_results = scrapers['matweb'].search(search_query)
            all_results.extend(matweb_results[:10])
        except Exception as e:
            print(f"MatWeb search error: {e}")

        # Search AZoM
        try:
            azom_results = scrapers['azom'].search(search_query)
            all_results.extend(azom_results[:10])
        except Exception as e:
            print(f"AZoM search error: {e}")

        if not all_results:
            return jsonify({
                'success': False,
                'error': 'No materials found matching your criteria'
            }), 404

        # Get detailed properties for top results (limit to avoid too many requests)
        detailed_materials = []
        for result in all_results[:15]:  # Limit to top 15
            try:
                scraper = None
                if 'matweb.com' in result['url']:
                    scraper = scrapers['matweb']
                elif 'azom.com' in result['url']:
                    scraper = scrapers['azom']

                if scraper:
                    properties_data = scraper.get_material_properties(result['url'])
                    if properties_data:
                        detailed_materials.append(properties_data)
            except Exception as e:
                print(f"Error fetching properties for {result['url']}: {e}")
                # Add basic info even if we can't get full properties
                detailed_materials.append(result)

        # If no detailed materials, use basic results
        if not detailed_materials:
            detailed_materials = all_results[:15]

        # Evaluate materials against requirements
        requirements = {
            'application': application,
            'material_type': material_type,
            'characteristics': characteristics,
            'properties': properties
        }

        evaluated_materials = evaluator.evaluate_materials(
            detailed_materials,
            requirements
        )

        # Format results for frontend
        formatted_results = []
        for material in evaluated_materials:
            formatted = {
                'name': material.get('name', 'Unknown'),
                'source': material.get('source', 'Unknown'),
                'url': material.get('url', '#'),
                'score': round(material.get('evaluation_score', 0), 1),
                'description': material.get('description', 'No description available')[:300],
                'category': material.get('category', ''),
                'match_details': material.get('match_details', {}),
                'properties': {
                    'mechanical': material.get('mechanical_properties', {}),
                    'physical': material.get('physical_properties', {}),
                    'thermal': material.get('thermal_properties', {}),
                    'electrical': material.get('electrical_properties', {})
                },
                'applications': material.get('applications', [])[:5],
                'key_properties': material.get('key_properties', [])[:5]
            }
            formatted_results.append(formatted)

        return jsonify({
            'success': True,
            'materials': formatted_results,
            'total_found': len(formatted_results)
        })

    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.teardown_appcontext
def cleanup(error=None):
    """Clean up scrapers on shutdown."""
    for scraper in scrapers.values():
        try:
            scraper.close()
        except:
            pass


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("Material Selector Web Application")
    print("=" * 80)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
