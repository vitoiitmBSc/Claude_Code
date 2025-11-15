#!/usr/bin/env python3
"""
Example usage of the Material Properties Web Scraper.

This file demonstrates various ways to use the scraper programmatically.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scrapers import MatWebScraper, AZoMScraper
from utils.export import export_to_json, export_to_markdown


def example_1_basic_search():
    """Example 1: Basic material search."""
    print("\n" + "=" * 80)
    print("Example 1: Basic Material Search")
    print("=" * 80)

    with MatWebScraper() as scraper:
        # Search for stainless steel
        results = scraper.search("stainless steel 316")

        print(f"\nFound {len(results)} materials:")
        for i, result in enumerate(results[:5], 1):
            print(f"\n{i}. {result['name']}")
            print(f"   URL: {result['url']}")


def example_2_get_properties():
    """Example 2: Get detailed material properties."""
    print("\n" + "=" * 80)
    print("Example 2: Get Detailed Material Properties")
    print("=" * 80)

    with MatWebScraper() as scraper:
        # First search for a material
        results = scraper.search("aluminum 6061")

        if results:
            # Get properties for the first result
            material_url = results[0]['url']
            print(f"\nFetching properties from: {material_url}")

            properties = scraper.get_material_properties(material_url)

            if properties:
                print(f"\nMaterial: {properties['name']}")

                if properties['mechanical_properties']:
                    print("\nMechanical Properties:")
                    for prop, value in list(properties['mechanical_properties'].items())[:5]:
                        print(f"  • {prop}: {value}")


def example_3_search_by_application():
    """Example 3: Search for materials by application."""
    print("\n" + "=" * 80)
    print("Example 3: Search by Application")
    print("=" * 80)

    with MatWebScraper() as scraper:
        # Search for corrosion-resistant materials
        print("\nSearching for corrosion-resistant materials...")
        results = scraper.search_by_application("high corrosion resistance")

        print(f"\nFound {len(results)} materials:")
        for i, result in enumerate(results[:5], 1):
            print(f"\n{i}. {result['name']}")
            print(f"   Source: {result['source']}")


def example_4_multiple_databases():
    """Example 4: Search across multiple databases."""
    print("\n" + "=" * 80)
    print("Example 4: Search Multiple Databases")
    print("=" * 80)

    query = "titanium alloy"
    all_results = []

    # Search MatWeb
    print(f"\nSearching MatWeb for '{query}'...")
    with MatWebScraper() as scraper:
        results = scraper.search(query)
        print(f"Found {len(results)} results")
        all_results.extend(results)

    # Search AZoM
    print(f"\nSearching AZoM for '{query}'...")
    with AZoMScraper() as scraper:
        results = scraper.search(query)
        print(f"Found {len(results)} results")
        all_results.extend(results)

    print(f"\nTotal results from all databases: {len(all_results)}")


def example_5_export_data():
    """Example 5: Export material data to files."""
    print("\n" + "=" * 80)
    print("Example 5: Export Material Data")
    print("=" * 80)

    with MatWebScraper() as scraper:
        # Search and get properties
        results = scraper.search("copper")

        if results:
            material_url = results[0]['url']
            properties = scraper.get_material_properties(material_url)

            if properties:
                # Create output directory
                output_dir = Path(__file__).parent.parent / 'output'
                output_dir.mkdir(exist_ok=True)

                # Export to JSON
                json_file = output_dir / 'copper_properties.json'
                export_to_json(properties, str(json_file))
                print(f"\n✓ Exported to JSON: {json_file}")

                # Export to Markdown
                md_file = output_dir / 'copper_properties.md'
                export_to_markdown(properties, str(md_file))
                print(f"✓ Exported to Markdown: {md_file}")


def example_6_filtering_results():
    """Example 6: Filter and process search results."""
    print("\n" + "=" * 80)
    print("Example 6: Filter Search Results")
    print("=" * 80)

    with MatWebScraper() as scraper:
        # Search for steel
        results = scraper.search("steel")

        # Filter for stainless steel
        stainless_results = [
            r for r in results
            if 'stainless' in r['name'].lower()
        ]

        print(f"\nTotal steel results: {len(results)}")
        print(f"Stainless steel results: {len(stainless_results)}")

        print("\nStainless steel materials found:")
        for i, result in enumerate(stainless_results[:5], 1):
            print(f"{i}. {result['name']}")


def example_7_error_handling():
    """Example 7: Proper error handling."""
    print("\n" + "=" * 80)
    print("Example 7: Error Handling")
    print("=" * 80)

    with MatWebScraper() as scraper:
        try:
            # Try to search with an empty query
            results = scraper.search("")

            if not results:
                print("\nNo results found for empty query (as expected)")

            # Try to get properties with invalid URL
            properties = scraper.get_material_properties("invalid_url")

            if not properties:
                print("No properties found for invalid URL (as expected)")

        except Exception as e:
            print(f"\nError occurred: {e}")


def example_8_custom_rate_limiting():
    """Example 8: Custom rate limiting."""
    print("\n" + "=" * 80)
    print("Example 8: Custom Rate Limiting")
    print("=" * 80)

    # Create scraper with custom rate limit (3 seconds between requests)
    with MatWebScraper(rate_limit=3.0) as scraper:
        print("\nSearching with 3-second rate limit...")

        results = scraper.search("bronze")
        print(f"Found {len(results)} results")

        # The scraper will automatically wait 3 seconds before the next request
        if results:
            material_url = results[0]['url']
            print(f"\nFetching properties (will wait 3 seconds)...")
            properties = scraper.get_material_properties(material_url)

            if properties:
                print(f"Got properties for: {properties['name']}")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("Material Properties Web Scraper - Usage Examples")
    print("=" * 80)

    examples = [
        ("Basic Search", example_1_basic_search),
        ("Get Properties", example_2_get_properties),
        ("Search by Application", example_3_search_by_application),
        ("Multiple Databases", example_4_multiple_databases),
        ("Export Data", example_5_export_data),
        ("Filtering Results", example_6_filtering_results),
        ("Error Handling", example_7_error_handling),
        ("Custom Rate Limiting", example_8_custom_rate_limiting),
    ]

    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")

    print("\nRunning Example 1 (Basic Search)...")
    print("To run other examples, modify this script or call them directly.")

    # Run the first example
    example_1_basic_search()

    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
