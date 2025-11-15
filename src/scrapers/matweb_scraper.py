"""
MatWeb scraper for material property data.

MatWeb (www.matweb.com) is a comprehensive material property database.
"""

from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraper


class MatWebScraper(BaseScraper):
    """
    Scraper for MatWeb material property database.

    MatWeb provides comprehensive material property data including:
    - Metals and alloys
    - Polymers and plastics
    - Ceramics and glasses
    - Composites
    - Semiconductors
    """

    BASE_URL = "https://www.matweb.com"
    SEARCH_URL = f"{BASE_URL}/search/QuickText.aspx"

    def __init__(self, rate_limit: float = 2.0, **kwargs):
        """
        Initialize MatWeb scraper.

        Args:
            rate_limit: Minimum seconds between requests (default: 2.0)
            **kwargs: Additional arguments passed to BaseScraper
        """
        super().__init__(rate_limit=rate_limit, **kwargs)

    def get_database_name(self) -> str:
        """Get the database name."""
        return "MatWeb"

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search MatWeb for materials matching the query.

        Args:
            query: Search query (e.g., "stainless steel 316", "aluminum 6061")
            filters: Optional filters (currently limited by MatWeb's interface)

        Returns:
            List of dictionaries containing:
                - name: Material name
                - url: Link to detailed material page
                - category: Material category
                - description: Brief description (if available)
        """
        params = {
            'txtText': query
        }

        html = self.fetch_url(self.SEARCH_URL, params=params)
        if not html:
            self.logger.warning(f"No results for query: {query}")
            return []

        return self._parse_search_results(html)

    def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        """
        Parse MatWeb search results.

        Args:
            html: HTML content from search page

        Returns:
            List of material results
        """
        soup = BeautifulSoup(html, 'html.parser')
        results = []

        # MatWeb shows results in a table or list format
        # Look for material links (they typically contain "DataSheet.aspx")
        links = soup.find_all('a', href=re.compile(r'DataSheet\.aspx'))

        for link in links:
            material_name = link.get_text(strip=True)
            material_url = link.get('href', '')

            # Make absolute URL
            if material_url.startswith('/'):
                material_url = f"{self.BASE_URL}{material_url}"
            elif not material_url.startswith('http'):
                material_url = f"{self.BASE_URL}/{material_url}"

            # Extract additional context from the parent elements
            parent = link.find_parent('tr') or link.find_parent('div')
            description = ""
            category = ""

            if parent:
                text = parent.get_text(strip=True)
                # Clean up the description
                description = text.replace(material_name, '').strip()

            if material_name and material_url:
                results.append({
                    'name': material_name,
                    'url': material_url,
                    'category': category,
                    'description': description,
                    'source': 'MatWeb'
                })

        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for result in results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)

        self.logger.info(f"Found {len(unique_results)} unique materials")
        return unique_results

    def get_material_properties(
        self,
        material_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed properties for a material from MatWeb.

        Args:
            material_id: Material URL or ID from search results

        Returns:
            Dictionary containing material properties including:
                - name: Material name
                - physical_properties: Density, melting point, etc.
                - mechanical_properties: Tensile strength, hardness, etc.
                - thermal_properties: Thermal conductivity, specific heat, etc.
                - electrical_properties: Resistivity, etc.
                - chemical_composition: Element percentages
                - applications: Common uses
        """
        # If material_id is not a full URL, treat it as part of URL
        if not material_id.startswith('http'):
            url = f"{self.BASE_URL}/{material_id}"
        else:
            url = material_id

        html = self.fetch_url(url)
        if not html:
            return None

        return self._parse_material_page(html, url)

    def _parse_material_page(
        self,
        html: str,
        url: str
    ) -> Dict[str, Any]:
        """
        Parse a MatWeb material datasheet page.

        Args:
            html: HTML content of the material page
            url: URL of the material page

        Returns:
            Dictionary with extracted material properties
        """
        soup = BeautifulSoup(html, 'html.parser')

        material_data = {
            'source': 'MatWeb',
            'url': url,
            'scraped_at': str(self.last_request_time),
            'name': '',
            'physical_properties': {},
            'mechanical_properties': {},
            'thermal_properties': {},
            'electrical_properties': {},
            'chemical_composition': {},
            'applications': [],
            'notes': []
        }

        # Extract material name (usually in h1 or title)
        title = soup.find('h1') or soup.find('title')
        if title:
            material_data['name'] = title.get_text(strip=True)

        # MatWeb uses tables for property data
        tables = soup.find_all('table')

        for table in tables:
            self._extract_properties_from_table(table, material_data)

        # Look for composition data (often in specific sections)
        comp_section = soup.find(text=re.compile(r'Composition', re.I))
        if comp_section:
            comp_table = comp_section.find_parent('table')
            if comp_table:
                material_data['chemical_composition'] = self._extract_composition(comp_table)

        return material_data

    def _extract_properties_from_table(
        self,
        table,
        material_data: Dict[str, Any]
    ) -> None:
        """
        Extract property data from a table.

        Args:
            table: BeautifulSoup table element
            material_data: Dictionary to populate with properties
        """
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                property_name = cells[0].get_text(strip=True)
                property_value = cells[1].get_text(strip=True)

                # Skip empty values
                if not property_value or property_value == '-':
                    continue

                # Categorize property based on name
                property_lower = property_name.lower()

                if any(keyword in property_lower for keyword in [
                    'density', 'melting', 'boiling', 'specific gravity'
                ]):
                    material_data['physical_properties'][property_name] = property_value

                elif any(keyword in property_lower for keyword in [
                    'tensile', 'yield', 'elongation', 'hardness', 'modulus',
                    'strength', 'impact', 'fatigue'
                ]):
                    material_data['mechanical_properties'][property_name] = property_value

                elif any(keyword in property_lower for keyword in [
                    'thermal', 'conductivity', 'expansion', 'specific heat',
                    'heat capacity'
                ]):
                    material_data['thermal_properties'][property_name] = property_value

                elif any(keyword in property_lower for keyword in [
                    'electrical', 'resistivity', 'conductivity'
                ]):
                    material_data['electrical_properties'][property_name] = property_value

    def _extract_composition(self, table) -> Dict[str, str]:
        """
        Extract chemical composition from a table.

        Args:
            table: BeautifulSoup table element

        Returns:
            Dictionary mapping elements to percentages
        """
        composition = {}
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                element = cells[0].get_text(strip=True)
                percentage = cells[1].get_text(strip=True)

                if element and percentage:
                    composition[element] = percentage

        return composition

    def search_by_application(
        self,
        application: str
    ) -> List[Dict[str, Any]]:
        """
        Search for materials suitable for a specific application.

        Args:
            application: Application description (e.g., "high corrosion resistance",
                        "high temperature", "aerospace")

        Returns:
            List of suitable materials
        """
        # Map common applications to search queries
        application_keywords = {
            'corrosion': 'stainless steel corrosion resistant',
            'high temperature': 'high temperature alloy superalloy',
            'aerospace': 'aerospace aluminum titanium',
            'marine': 'marine grade stainless steel',
            'cryogenic': 'cryogenic low temperature',
            'wear resistant': 'wear resistant hardened steel',
            'lightweight': 'aluminum titanium composite'
        }

        # Find best matching query
        query = application.lower()
        for key, search_query in application_keywords.items():
            if key in query:
                query = search_query
                break

        self.logger.info(f"Searching for application: {application} -> query: {query}")
        return self.search(query)
