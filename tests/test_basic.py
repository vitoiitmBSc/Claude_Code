#!/usr/bin/env python3
"""
Basic tests for the material scraper.

These tests verify that the code is syntactically correct and
basic functionality works without making actual network requests.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scrapers import MatWebScraper, AZoMScraper
from utils.parser import clean_text, extract_numeric_value, categorize_property
from utils.export import _flatten_dict


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from scrapers import MatWebScraper, AZoMScraper, BaseScraper
        from utils.parser import clean_text, parse_property_table
        from utils.export import export_to_json, export_to_csv
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_scraper_initialization():
    """Test that scrapers can be initialized."""
    print("\nTesting scraper initialization...")

    try:
        matweb = MatWebScraper()
        assert matweb.get_database_name() == "MatWeb"
        matweb.close()

        azom = AZoMScraper()
        assert azom.get_database_name() == "AZoM"
        azom.close()

        print("✓ Scrapers initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False


def test_context_manager():
    """Test that scrapers work with context manager."""
    print("\nTesting context manager...")

    try:
        with MatWebScraper() as scraper:
            assert scraper is not None
            assert scraper.get_database_name() == "MatWeb"

        with AZoMScraper() as scraper:
            assert scraper is not None
            assert scraper.get_database_name() == "AZoM"

        print("✓ Context manager works correctly")
        return True
    except Exception as e:
        print(f"✗ Context manager failed: {e}")
        return False


def test_parser_utilities():
    """Test parsing utility functions."""
    print("\nTesting parser utilities...")

    try:
        # Test clean_text
        assert clean_text("  hello   world  ") == "hello world"
        assert clean_text("") == ""

        # Test extract_numeric_value
        assert extract_numeric_value("100 MPa") == 100.0
        assert extract_numeric_value("2.5 g/cm³") == 2.5
        assert extract_numeric_value("1.5e3") == 1500.0

        # Test categorize_property
        assert categorize_property("Density") == "physical"
        assert categorize_property("Tensile Strength") == "mechanical"
        assert categorize_property("Thermal Conductivity") == "thermal"
        assert categorize_property("Electrical Resistivity") == "electrical"

        print("✓ Parser utilities work correctly")
        return True
    except Exception as e:
        print(f"✗ Parser utilities failed: {e}")
        return False


def test_export_utilities():
    """Test export utility functions."""
    print("\nTesting export utilities...")

    try:
        # Test flatten_dict
        nested = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3
            },
            'e': [4, 5, 6]
        }

        flat = _flatten_dict(nested)
        assert 'a' in flat
        assert 'b.c' in flat
        assert 'b.d' in flat
        assert 'e' in flat

        print("✓ Export utilities work correctly")
        return True
    except Exception as e:
        print(f"✗ Export utilities failed: {e}")
        return False


def test_rate_limiting():
    """Test rate limiting configuration."""
    print("\nTesting rate limiting...")

    try:
        # Create scraper with custom rate limit
        scraper = MatWebScraper(rate_limit=0.5)
        assert scraper.rate_limit == 0.5

        scraper2 = AZoMScraper(rate_limit=2.0)
        assert scraper2.rate_limit == 2.0

        scraper.close()
        scraper2.close()

        print("✓ Rate limiting configured correctly")
        return True
    except Exception as e:
        print(f"✗ Rate limiting test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("Material Scraper - Basic Tests")
    print("=" * 80)

    tests = [
        test_imports,
        test_scraper_initialization,
        test_context_manager,
        test_parser_utilities,
        test_export_utilities,
        test_rate_limiting,
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "=" * 80)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 80 + "\n")

    return all(results)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
