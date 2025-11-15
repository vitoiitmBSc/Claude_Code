"""
Parsing utilities for material property data.
"""

import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup, Tag


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.

    Args:
        text: Raw text string

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters but keep units
    text = text.strip()

    return text


def parse_property_table(
    table: Tag,
    header_row: int = 0
) -> List[Dict[str, str]]:
    """
    Parse a property table into a list of dictionaries.

    Args:
        table: BeautifulSoup table element
        header_row: Index of the header row (default: 0)

    Returns:
        List of dictionaries with property data
    """
    rows = table.find_all('tr')
    if not rows:
        return []

    # Extract headers
    headers = []
    if header_row < len(rows):
        header_cells = rows[header_row].find_all(['th', 'td'])
        headers = [clean_text(cell.get_text()) for cell in header_cells]

    # If no headers found, use generic names
    if not headers:
        # Determine number of columns from first data row
        first_row = rows[0] if rows else None
        if first_row:
            num_cols = len(first_row.find_all(['th', 'td']))
            headers = [f'Column_{i}' for i in range(num_cols)]

    # Extract data rows
    data = []
    start_row = header_row + 1 if headers else 0

    for row in rows[start_row:]:
        cells = row.find_all(['td', 'th'])
        if len(cells) == len(headers):
            row_data = {}
            for i, cell in enumerate(cells):
                row_data[headers[i]] = clean_text(cell.get_text())
            data.append(row_data)

    return data


def extract_numeric_value(text: str) -> Optional[float]:
    """
    Extract numeric value from text, ignoring units.

    Args:
        text: Text containing numeric value (e.g., "100 MPa", "2.5 g/cm³")

    Returns:
        Numeric value as float, or None if not found
    """
    if not text:
        return None

    # Remove commas from numbers
    text = text.replace(',', '')

    # Look for numeric patterns (including scientific notation)
    pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    match = re.search(pattern, text)

    if match:
        try:
            return float(match.group())
        except ValueError:
            return None

    return None


def extract_unit(text: str) -> Optional[str]:
    """
    Extract unit from text.

    Args:
        text: Text containing value and unit (e.g., "100 MPa")

    Returns:
        Unit string, or None if not found
    """
    if not text:
        return None

    # Remove the numeric part
    numeric_pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    unit = re.sub(numeric_pattern, '', text).strip()

    # Common unit patterns
    if unit:
        return unit

    return None


def parse_range(text: str) -> Dict[str, Optional[float]]:
    """
    Parse a range value (e.g., "10 - 20 MPa").

    Args:
        text: Text containing range

    Returns:
        Dictionary with 'min', 'max', and 'unit' keys
    """
    result = {
        'min': None,
        'max': None,
        'unit': None
    }

    if not text:
        return result

    # Look for range pattern
    range_pattern = r'([-+]?\d*\.?\d+)\s*[-–to]+\s*([-+]?\d*\.?\d+)'
    match = re.search(range_pattern, text, re.IGNORECASE)

    if match:
        try:
            result['min'] = float(match.group(1))
            result['max'] = float(match.group(2))
            # Extract unit
            result['unit'] = extract_unit(text)
        except ValueError:
            pass
    else:
        # Single value
        result['min'] = extract_numeric_value(text)
        result['max'] = result['min']
        result['unit'] = extract_unit(text)

    return result


def categorize_property(property_name: str) -> str:
    """
    Categorize a property based on its name.

    Args:
        property_name: Name of the property

    Returns:
        Category string ('physical', 'mechanical', 'thermal', 'electrical', 'other')
    """
    property_lower = property_name.lower()

    physical_keywords = [
        'density', 'melting', 'boiling', 'specific gravity',
        'molecular', 'mass', 'weight'
    ]

    mechanical_keywords = [
        'tensile', 'yield', 'elongation', 'hardness', 'modulus',
        'strength', 'impact', 'fatigue', 'elastic', "young's",
        'compression', 'shear', 'toughness'
    ]

    thermal_keywords = [
        'thermal', 'conductivity', 'expansion', 'specific heat',
        'heat capacity', 'temperature', 'coefficient'
    ]

    electrical_keywords = [
        'electrical', 'resistivity', 'dielectric', 'conductivity',
        'resistance', 'permittivity'
    ]

    if any(kw in property_lower for kw in physical_keywords):
        return 'physical'
    elif any(kw in property_lower for kw in mechanical_keywords):
        return 'mechanical'
    elif any(kw in property_lower for kw in thermal_keywords):
        return 'thermal'
    elif any(kw in property_lower for kw in electrical_keywords):
        return 'electrical'
    else:
        return 'other'


def normalize_property_name(property_name: str) -> str:
    """
    Normalize property name for consistency.

    Args:
        property_name: Original property name

    Returns:
        Normalized property name
    """
    # Clean text
    normalized = clean_text(property_name)

    # Convert to title case
    normalized = normalized.title()

    # Common abbreviations to uppercase
    abbreviations = ['MPa', 'GPa', 'HRC', 'HRB', 'HV', 'CTE', 'UTS']
    for abbr in abbreviations:
        normalized = re.sub(
            r'\b' + abbr + r'\b',
            abbr,
            normalized,
            flags=re.IGNORECASE
        )

    return normalized
