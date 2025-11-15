#!/usr/bin/env python3
"""
Material Evaluator - Evaluates and ranks materials based on user requirements.

This module evaluates materials against user-specified requirements and
provides a scoring/ranking system to help select the best material.
"""

from typing import List, Dict, Any, Optional
import re


class MaterialEvaluator:
    """Evaluates materials based on user requirements."""

    def __init__(self):
        """Initialize the evaluator."""
        pass

    def evaluate_materials(
        self,
        materials: List[Dict[str, Any]],
        requirements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Evaluate and rank materials based on requirements.

        Args:
            materials: List of materials with properties
            requirements: Dictionary of user requirements

        Returns:
            List of materials with scores, sorted by best match
        """
        evaluated = []

        for material in materials:
            score = self._calculate_score(material, requirements)
            material_copy = material.copy()
            material_copy['evaluation_score'] = score
            material_copy['match_details'] = self._get_match_details(material, requirements)
            evaluated.append(material_copy)

        # Sort by score (highest first)
        evaluated.sort(key=lambda x: x['evaluation_score'], reverse=True)

        return evaluated

    def _calculate_score(
        self,
        material: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> float:
        """
        Calculate a score for how well a material matches requirements.

        Args:
            material: Material data
            requirements: User requirements

        Returns:
            Score from 0-100
        """
        total_score = 0.0
        total_weight = 0.0

        # Application match (weight: 30)
        if requirements.get('application'):
            app_score = self._score_application_match(
                material,
                requirements['application']
            )
            total_score += app_score * 30
            total_weight += 30

        # Property requirements (weight: 40)
        if requirements.get('properties'):
            prop_score = self._score_property_requirements(
                material,
                requirements['properties']
            )
            total_score += prop_score * 40
            total_weight += 40

        # Material type/category match (weight: 15)
        if requirements.get('material_type'):
            type_score = self._score_material_type(
                material,
                requirements['material_type']
            )
            total_score += type_score * 15
            total_weight += 15

        # Key properties/characteristics match (weight: 15)
        if requirements.get('characteristics'):
            char_score = self._score_characteristics(
                material,
                requirements['characteristics']
            )
            total_score += char_score * 15
            total_weight += 15

        # Normalize score to 0-100
        if total_weight > 0:
            return (total_score / total_weight) * 100
        else:
            return 0.0

    def _score_application_match(
        self,
        material: Dict[str, Any],
        required_application: str
    ) -> float:
        """Score how well material matches the application."""
        if not required_application:
            return 0.5

        required_lower = required_application.lower()
        score = 0.0

        # Check in applications list
        if material.get('applications'):
            for app in material['applications']:
                if self._text_similarity(required_lower, app.lower()) > 0.5:
                    score = max(score, 1.0)
                elif any(word in app.lower() for word in required_lower.split()):
                    score = max(score, 0.7)

        # Check in description
        if material.get('description'):
            desc = material['description'].lower()
            if required_lower in desc:
                score = max(score, 0.8)
            elif any(word in desc for word in required_lower.split() if len(word) > 3):
                score = max(score, 0.5)

        # Check in key properties
        if material.get('key_properties'):
            for prop in material['key_properties']:
                if self._text_similarity(required_lower, prop.lower()) > 0.5:
                    score = max(score, 0.9)

        return score

    def _score_property_requirements(
        self,
        material: Dict[str, Any],
        property_requirements: Dict[str, Any]
    ) -> float:
        """Score how well material meets specific property requirements."""
        if not property_requirements:
            return 0.5

        scores = []

        for prop_name, req_value in property_requirements.items():
            # Search for the property in all property categories
            material_value = self._find_property_value(material, prop_name)

            if material_value:
                prop_score = self._compare_property_values(
                    material_value,
                    req_value,
                    prop_name
                )
                scores.append(prop_score)

        if scores:
            return sum(scores) / len(scores)
        else:
            # No properties found, but that doesn't mean it's a bad match
            return 0.3

    def _find_property_value(
        self,
        material: Dict[str, Any],
        property_name: str
    ) -> Optional[str]:
        """Find a property value in the material data."""
        prop_lower = property_name.lower()

        # Check all property categories
        for category in ['physical_properties', 'mechanical_properties',
                        'thermal_properties', 'electrical_properties']:
            if material.get(category):
                for key, value in material[category].items():
                    if prop_lower in key.lower():
                        return value

        return None

    def _compare_property_values(
        self,
        material_value: str,
        required_value: Any,
        property_name: str
    ) -> float:
        """Compare a material's property value with required value."""
        try:
            # Extract numeric value from material property string
            material_num = self._extract_number(material_value)

            if material_num is None:
                # If we can't extract a number, check for text match
                if str(required_value).lower() in material_value.lower():
                    return 1.0
                else:
                    return 0.3

            # Handle different requirement formats
            if isinstance(required_value, dict):
                # Range requirements like {"min": 100, "max": 200}
                min_val = required_value.get('min')
                max_val = required_value.get('max')

                if min_val is not None and max_val is not None:
                    if min_val <= material_num <= max_val:
                        return 1.0
                    else:
                        # Partial credit based on how close
                        range_size = max_val - min_val
                        if material_num < min_val:
                            diff = min_val - material_num
                        else:
                            diff = material_num - max_val
                        return max(0.0, 1.0 - (diff / range_size))

                elif min_val is not None:
                    # Minimum requirement
                    if material_num >= min_val:
                        return 1.0
                    else:
                        return max(0.0, material_num / min_val)

                elif max_val is not None:
                    # Maximum requirement
                    if material_num <= max_val:
                        return 1.0
                    else:
                        return max(0.0, max_val / material_num)

            else:
                # Direct value comparison
                required_num = float(required_value)
                # Close match = high score
                diff_ratio = abs(material_num - required_num) / required_num
                return max(0.0, 1.0 - diff_ratio)

        except (ValueError, TypeError):
            # Fallback to text comparison
            if str(required_value).lower() in str(material_value).lower():
                return 1.0
            else:
                return 0.3

        return 0.5

    def _extract_number(self, text: str) -> Optional[float]:
        """Extract the first number from a text string."""
        # Remove commas from numbers
        text = text.replace(',', '')

        # Find numbers (including decimals and scientific notation)
        match = re.search(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', text)

        if match:
            return float(match.group())

        return None

    def _score_material_type(
        self,
        material: Dict[str, Any],
        required_type: str
    ) -> float:
        """Score how well material type matches requirement."""
        if not required_type:
            return 0.5

        required_lower = required_type.lower()

        # Check name
        if material.get('name'):
            name = material['name'].lower()
            if required_lower in name:
                return 1.0
            elif any(word in name for word in required_lower.split()):
                return 0.7

        # Check category
        if material.get('category'):
            category = material['category'].lower()
            if required_lower in category:
                return 1.0
            elif any(word in category for word in required_lower.split()):
                return 0.7

        return 0.3

    def _score_characteristics(
        self,
        material: Dict[str, Any],
        required_characteristics: List[str]
    ) -> float:
        """Score how well material matches required characteristics."""
        if not required_characteristics:
            return 0.5

        scores = []

        for characteristic in required_characteristics:
            char_lower = characteristic.lower()
            score = 0.0

            # Check in key properties
            if material.get('key_properties'):
                for prop in material['key_properties']:
                    if char_lower in prop.lower():
                        score = max(score, 1.0)

            # Check in description
            if material.get('description'):
                desc = material['description'].lower()
                if char_lower in desc:
                    score = max(score, 0.8)

            # Check in applications
            if material.get('applications'):
                for app in material['applications']:
                    if char_lower in app.lower():
                        score = max(score, 0.7)

            scores.append(score)

        if scores:
            return sum(scores) / len(scores)
        else:
            return 0.5

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity (word overlap)."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _get_match_details(
        self,
        material: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> Dict[str, str]:
        """Get details about why a material matches requirements."""
        details = {}

        if requirements.get('application'):
            if material.get('applications'):
                matching_apps = [
                    app for app in material['applications']
                    if any(word in app.lower()
                          for word in requirements['application'].lower().split())
                ]
                if matching_apps:
                    details['matching_applications'] = ', '.join(matching_apps[:3])

        if requirements.get('characteristics'):
            if material.get('key_properties'):
                matching_props = []
                for char in requirements['characteristics']:
                    for prop in material['key_properties']:
                        if char.lower() in prop.lower():
                            matching_props.append(prop)
                if matching_props:
                    details['matching_characteristics'] = ', '.join(matching_props[:3])

        return details
