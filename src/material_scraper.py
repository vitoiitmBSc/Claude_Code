#!/usr/bin/env python3
"""
Material Properties Web Scraper - Main CLI Tool.

A comprehensive tool for fetching material properties from professional databases
like MatWeb, AZoM, and others.

Usage:
    python material_scraper.py search "stainless steel 316"
    python material_scraper.py search "aluminum alloy" --source matweb
    python material_scraper.py get-properties <material_url> --export json
    python material_scraper.py search-application "high corrosion resistance"
"""

import argparse
import sys
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from scrapers import MatWebScraper, AZoMScraper
from utils.export import (
    export_to_json,
    export_to_csv,
    export_to_markdown,
    export_search_results_to_csv
)


class MaterialScraperCLI:
    """Main CLI class for material scraper."""

    def __init__(self):
        """Initialize the CLI."""
        self.scrapers = {
            'matweb': MatWebScraper(),
            'azom': AZoMScraper()
        }

    def search(
        self,
        query: str,
        source: Optional[str] = None,
        limit: int = 10,
        export_format: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for materials across databases.

        Args:
            query: Search query string
            source: Specific source to search (matweb, azom, or None for all)
            limit: Maximum number of results
            export_format: Export format (json, csv, markdown)
            output_file: Output file path

        Returns:
            List of search results
        """
        all_results = []

        # Determine which scrapers to use
        if source:
            source = source.lower()
            if source not in self.scrapers:
                print(f"Error: Unknown source '{source}'")
                print(f"Available sources: {', '.join(self.scrapers.keys())}")
                return []
            scrapers_to_use = {source: self.scrapers[source]}
        else:
            scrapers_to_use = self.scrapers

        # Search each database
        for source_name, scraper in scrapers_to_use.items():
            print(f"\n🔍 Searching {scraper.get_database_name()}...")

            try:
                results = scraper.search(query)
                print(f"   Found {len(results)} results")
                all_results.extend(results)

            except Exception as e:
                print(f"   Error searching {source_name}: {e}")

        # Limit results
        all_results = all_results[:limit]

        # Display results
        self._display_search_results(all_results)

        # Export if requested
        if export_format and output_file:
            self._export_search_results(all_results, export_format, output_file)

        return all_results

    def get_properties(
        self,
        material_url: str,
        export_format: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed properties for a specific material.

        Args:
            material_url: URL of the material
            export_format: Export format (json, csv, markdown)
            output_file: Output file path

        Returns:
            Material properties dictionary
        """
        # Determine which scraper to use based on URL
        scraper = None
        if 'matweb.com' in material_url:
            scraper = self.scrapers['matweb']
        elif 'azom.com' in material_url:
            scraper = self.scrapers['azom']
        else:
            print("Error: Could not determine database from URL")
            return None

        print(f"\n📊 Fetching properties from {scraper.get_database_name()}...")

        try:
            properties = scraper.get_material_properties(material_url)

            if properties:
                self._display_properties(properties)

                # Export if requested
                if export_format and output_file:
                    self._export_properties(properties, export_format, output_file)

                return properties
            else:
                print("   No properties found")
                return None

        except Exception as e:
            print(f"   Error fetching properties: {e}")
            return None

    def search_by_application(
        self,
        application: str,
        limit: int = 10,
        export_format: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for materials suitable for a specific application.

        Args:
            application: Application description
            limit: Maximum number of results
            export_format: Export format (json, csv, markdown)
            output_file: Output file path

        Returns:
            List of suitable materials
        """
        print(f"\n🎯 Searching for materials for application: {application}")

        all_results = []

        # Search MatWeb with application-specific query
        matweb = self.scrapers['matweb']
        try:
            results = matweb.search_by_application(application)
            all_results.extend(results)
            print(f"   MatWeb: Found {len(results)} results")
        except Exception as e:
            print(f"   MatWeb error: {e}")

        # Also search AZoM with general query
        azom = self.scrapers['azom']
        try:
            results = azom.search(application)
            all_results.extend(results)
            print(f"   AZoM: Found {len(results)} results")
        except Exception as e:
            print(f"   AZoM error: {e}")

        # Limit results
        all_results = all_results[:limit]

        # Display results
        self._display_search_results(all_results)

        # Export if requested
        if export_format and output_file:
            self._export_search_results(all_results, export_format, output_file)

        return all_results

    def _display_search_results(self, results: List[Dict[str, Any]]) -> None:
        """Display search results in a formatted way."""
        if not results:
            print("\n❌ No results found")
            return

        print(f"\n✅ Total Results: {len(results)}\n")
        print("=" * 80)

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.get('name', 'Unknown')}")
            print(f"   Source: {result.get('source', 'Unknown')}")

            if result.get('category'):
                print(f"   Category: {result['category']}")

            if result.get('description'):
                desc = result['description'][:200]
                if len(result['description']) > 200:
                    desc += "..."
                print(f"   Description: {desc}")

            print(f"   URL: {result.get('url', 'N/A')}")

        print("\n" + "=" * 80)

    def _display_properties(self, properties: Dict[str, Any]) -> None:
        """Display material properties in a formatted way."""
        print("\n" + "=" * 80)
        print(f"Material: {properties.get('name', 'Unknown')}")
        print(f"Source: {properties.get('source', 'Unknown')}")
        print("=" * 80)

        # Physical properties
        if properties.get('physical_properties'):
            print("\n📏 Physical Properties:")
            for prop, value in properties['physical_properties'].items():
                print(f"   • {prop}: {value}")

        # Mechanical properties
        if properties.get('mechanical_properties'):
            print("\n💪 Mechanical Properties:")
            for prop, value in properties['mechanical_properties'].items():
                print(f"   • {prop}: {value}")

        # Thermal properties
        if properties.get('thermal_properties'):
            print("\n🌡️  Thermal Properties:")
            for prop, value in properties['thermal_properties'].items():
                print(f"   • {prop}: {value}")

        # Electrical properties
        if properties.get('electrical_properties'):
            print("\n⚡ Electrical Properties:")
            for prop, value in properties['electrical_properties'].items():
                print(f"   • {prop}: {value}")

        # Chemical composition
        if properties.get('chemical_composition'):
            print("\n🧪 Chemical Composition:")
            for element, percentage in properties['chemical_composition'].items():
                print(f"   • {element}: {percentage}")

        # Applications
        if properties.get('applications'):
            print("\n🔧 Applications:")
            for app in properties['applications'][:5]:
                print(f"   • {app}")

        # Key properties
        if properties.get('key_properties'):
            print("\n⭐ Key Properties:")
            for prop in properties['key_properties'][:5]:
                print(f"   • {prop}")

        print("\n" + "=" * 80)

    def _export_search_results(
        self,
        results: List[Dict[str, Any]],
        format: str,
        output_file: str
    ) -> None:
        """Export search results to file."""
        format = format.lower()

        if format == 'json':
            success = export_to_json(results, output_file)
        elif format == 'csv':
            success = export_search_results_to_csv(results, output_file)
        else:
            print(f"Error: Unsupported export format '{format}'")
            return

        if success:
            print(f"\n💾 Results exported to {output_file}")
        else:
            print(f"\n❌ Failed to export results")

    def _export_properties(
        self,
        properties: Dict[str, Any],
        format: str,
        output_file: str
    ) -> None:
        """Export material properties to file."""
        format = format.lower()

        if format == 'json':
            success = export_to_json(properties, output_file)
        elif format == 'csv':
            success = export_to_csv(properties, output_file)
        elif format == 'markdown':
            success = export_to_markdown(properties, output_file)
        else:
            print(f"Error: Unsupported export format '{format}'")
            return

        if success:
            print(f"\n💾 Properties exported to {output_file}")
        else:
            print(f"\n❌ Failed to export properties")

    def cleanup(self) -> None:
        """Close all scraper sessions."""
        for scraper in self.scrapers.values():
            scraper.close()


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Material Properties Web Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Search for materials:
    %(prog)s search "stainless steel 316"
    %(prog)s search "aluminum alloy" --source matweb --limit 5

  Get detailed properties:
    %(prog)s get-properties "https://www.matweb.com/..." --export json --output steel.json

  Search by application:
    %(prog)s search-app "high corrosion resistance" --export csv --output results.csv
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for materials')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--source', choices=['matweb', 'azom'], help='Specific database to search')
    search_parser.add_argument('--limit', type=int, default=10, help='Maximum number of results (default: 10)')
    search_parser.add_argument('--export', choices=['json', 'csv'], help='Export format')
    search_parser.add_argument('--output', help='Output file path')

    # Get properties command
    props_parser = subparsers.add_parser('get-properties', help='Get detailed properties for a material')
    props_parser.add_argument('url', help='Material URL')
    props_parser.add_argument('--export', choices=['json', 'csv', 'markdown'], help='Export format')
    props_parser.add_argument('--output', help='Output file path')

    # Search by application command
    app_parser = subparsers.add_parser('search-app', help='Search for materials by application')
    app_parser.add_argument('application', help='Application description')
    app_parser.add_argument('--limit', type=int, default=10, help='Maximum number of results (default: 10)')
    app_parser.add_argument('--export', choices=['json', 'csv'], help='Export format')
    app_parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Create CLI instance
    cli = MaterialScraperCLI()

    try:
        if args.command == 'search':
            cli.search(
                args.query,
                source=args.source,
                limit=args.limit,
                export_format=args.export,
                output_file=args.output
            )

        elif args.command == 'get-properties':
            cli.get_properties(
                args.url,
                export_format=args.export,
                output_file=args.output
            )

        elif args.command == 'search-app':
            cli.search_by_application(
                args.application,
                limit=args.limit,
                export_format=args.export,
                output_file=args.output
            )

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        return 130

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    finally:
        cli.cleanup()

    return 0


if __name__ == '__main__':
    sys.exit(main())
