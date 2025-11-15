"""
Export utilities for material property data.
"""

import json
import csv
from typing import Dict, List, Any
from pathlib import Path


def export_to_json(
    data: Dict[str, Any],
    output_file: str,
    indent: int = 2
) -> bool:
    """
    Export material data to JSON file.

    Args:
        data: Material property dictionary
        output_file: Path to output JSON file
        indent: JSON indentation (default: 2)

    Returns:
        True if successful, False otherwise
    """
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False


def export_to_csv(
    data: Dict[str, Any],
    output_file: str
) -> bool:
    """
    Export material data to CSV file.

    Args:
        data: Material property dictionary
        output_file: Path to output CSV file

    Returns:
        True if successful, False otherwise
    """
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Flatten the nested dictionary
        flat_data = _flatten_dict(data)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(['Property', 'Value'])

            # Write data
            for key, value in flat_data.items():
                writer.writerow([key, value])

        return True

    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False


def export_to_markdown(
    data: Dict[str, Any],
    output_file: str
) -> bool:
    """
    Export material data to Markdown file.

    Args:
        data: Material property dictionary
        output_file: Path to output Markdown file

    Returns:
        True if successful, False otherwise
    """
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            # Write title
            material_name = data.get('name', 'Unknown Material')
            f.write(f"# {material_name}\n\n")

            # Write source
            source = data.get('source', 'Unknown')
            url = data.get('url', '')
            f.write(f"**Source:** [{source}]({url})\n\n")

            # Write physical properties
            if data.get('physical_properties'):
                f.write("## Physical Properties\n\n")
                f.write("| Property | Value |\n")
                f.write("|----------|-------|\n")
                for prop, value in data['physical_properties'].items():
                    f.write(f"| {prop} | {value} |\n")
                f.write("\n")

            # Write mechanical properties
            if data.get('mechanical_properties'):
                f.write("## Mechanical Properties\n\n")
                f.write("| Property | Value |\n")
                f.write("|----------|-------|\n")
                for prop, value in data['mechanical_properties'].items():
                    f.write(f"| {prop} | {value} |\n")
                f.write("\n")

            # Write thermal properties
            if data.get('thermal_properties'):
                f.write("## Thermal Properties\n\n")
                f.write("| Property | Value |\n")
                f.write("|----------|-------|\n")
                for prop, value in data['thermal_properties'].items():
                    f.write(f"| {prop} | {value} |\n")
                f.write("\n")

            # Write electrical properties
            if data.get('electrical_properties'):
                f.write("## Electrical Properties\n\n")
                f.write("| Property | Value |\n")
                f.write("|----------|-------|\n")
                for prop, value in data['electrical_properties'].items():
                    f.write(f"| {prop} | {value} |\n")
                f.write("\n")

            # Write chemical composition
            if data.get('chemical_composition'):
                f.write("## Chemical Composition\n\n")
                f.write("| Element | Percentage |\n")
                f.write("|---------|------------|\n")
                for element, percentage in data['chemical_composition'].items():
                    f.write(f"| {element} | {percentage} |\n")
                f.write("\n")

            # Write applications
            if data.get('applications'):
                f.write("## Applications\n\n")
                for app in data['applications']:
                    f.write(f"- {app}\n")
                f.write("\n")

            # Write key properties
            if data.get('key_properties'):
                f.write("## Key Properties\n\n")
                for prop in data['key_properties']:
                    f.write(f"- {prop}\n")
                f.write("\n")

        return True

    except Exception as e:
        print(f"Error exporting to Markdown: {e}")
        return False


def _flatten_dict(
    d: Dict[str, Any],
    parent_key: str = '',
    separator: str = '.'
) -> Dict[str, str]:
    """
    Flatten a nested dictionary.

    Args:
        d: Dictionary to flatten
        parent_key: Parent key for recursion
        separator: Separator for nested keys

    Returns:
        Flattened dictionary
    """
    items = []

    for k, v in d.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k

        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, separator).items())
        elif isinstance(v, list):
            # Convert list to comma-separated string
            items.append((new_key, ', '.join(map(str, v))))
        else:
            items.append((new_key, str(v)))

    return dict(items)


def export_search_results_to_csv(
    results: List[Dict[str, Any]],
    output_file: str
) -> bool:
    """
    Export search results to CSV file.

    Args:
        results: List of search result dictionaries
        output_file: Path to output CSV file

    Returns:
        True if successful, False otherwise
    """
    try:
        if not results:
            print("No results to export")
            return False

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get all unique keys from results
        all_keys = set()
        for result in results:
            all_keys.update(result.keys())

        fieldnames = sorted(all_keys)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        return True

    except Exception as e:
        print(f"Error exporting search results to CSV: {e}")
        return False
