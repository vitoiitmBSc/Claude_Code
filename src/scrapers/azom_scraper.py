"""
AZoM scraper for material property data.

AZoM (www.azom.com) is a materials science and engineering database.
"""

from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraper


class AZoMScraper(BaseScraper):
    """
    Scraper for AZoM material property database.

    AZoM provides material information including:
    - Metals and alloys
    - Polymers
    - Ceramics
    - Composites
    - Detailed articles and datasheets
    """

    BASE_URL = "https://www.azom.com"
    SEARCH_URL = f"{BASE_URL}/search.aspx"

    def __init__(self, rate_limit: float = 2.0, **kwargs):
        """
        Initialize AZoM scraper.

        Args:
            rate_limit: Minimum seconds between requests (default: 2.0)
            **kwargs: Additional arguments passed to BaseScraper
        """
        super().__init__(rate_limit=rate_limit, **kwargs)

    def get_database_name(self) -> str:
        """Get the database name."""
        return "AZoM"

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search AZoM for materials matching the query.

        Args:
            query: Search query (e.g., "titanium alloy", "PEEK polymer")
            filters: Optional filters

        Returns:
            List of dictionaries containing material information
        """
        params = {
            'q': query,
            'ContentType': 'Materials'  # Focus on materials, not articles
        }

        if filters:
            # Add any additional filters
            params.update(filters)

        html = self.fetch_url(self.SEARCH_URL, params=params)
        if not html:
            self.logger.warning(f"No results for query: {query}")
            return []

        return self._parse_search_results(html)

    def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        """
        Parse AZoM search results.

        Args:
            html: HTML content from search page

        Returns:
            List of material results
        """
        soup = BeautifulSoup(html, 'html.parser')
        results = []

        # AZoM typically shows results in article/material cards
        # Look for links to material property pages
        material_links = soup.find_all('a', href=re.compile(r'properties\.aspx|article\.aspx'))

        for link in material_links:
            material_name = link.get_text(strip=True)
            material_url = link.get('href', '')

            # Skip if empty
            if not material_name or not material_url:
                continue

            # Make absolute URL
            if material_url.startswith('/'):
                material_url = f"{self.BASE_URL}{material_url}"
            elif not material_url.startswith('http'):
                material_url = f"{self.BASE_URL}/{material_url}"

            # Extract additional context
            parent = link.find_parent('div', class_=re.compile(r'search|result|card'))
            description = ""
            category = ""

            if parent:
                desc_elem = parent.find('p') or parent.find('div', class_=re.compile(r'desc|summary'))
                if desc_elem:
                    description = desc_elem.get_text(strip=True)

                # Try to extract category
                cat_elem = parent.find(class_=re.compile(r'category|type'))
                if cat_elem:
                    category = cat_elem.get_text(strip=True)

            results.append({
                'name': material_name,
                'url': material_url,
                'category': category,
                'description': description,
                'source': 'AZoM'
            })

        # Remove duplicates
        seen_urls = set()
        unique_results = []
        for result in results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)

        self.logger.info(f"Found {len(unique_results)} unique materials")
        return unique_results[:20]  # Limit to top 20 results

    def get_material_properties(
        self,
        material_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed properties for a material from AZoM.

        Args:
            material_id: Material URL or ID from search results

        Returns:
            Dictionary containing material properties
        """
        # If material_id is not a full URL, construct it
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
        Parse an AZoM material properties page.

        Args:
            html: HTML content of the material page
            url: URL of the material page

        Returns:
            Dictionary with extracted material properties
        """
        soup = BeautifulSoup(html, 'html.parser')

        material_data = {
            'source': 'AZoM',
            'url': url,
            'scraped_at': str(self.last_request_time),
            'name': '',
            'physical_properties': {},
            'mechanical_properties': {},
            'thermal_properties': {},
            'electrical_properties': {},
            'chemical_composition': {},
            'applications': [],
            'notes': [],
            'key_properties': []
        }

        # Extract material name
        title = soup.find('h1') or soup.find('title')
        if title:
            material_data['name'] = title.get_text(strip=True).replace(' Properties', '')

        # AZoM often has a "Key Properties" section
        key_props = soup.find(text=re.compile(r'Key Properties', re.I))
        if key_props:
            props_section = key_props.find_parent(['div', 'section'])
            if props_section:
                props_list = props_section.find_all('li')
                material_data['key_properties'] = [
                    li.get_text(strip=True) for li in props_list
                ]

        # Extract properties from tables
        tables = soup.find_all('table')
        for table in tables:
            self._extract_properties_from_table(table, material_data)

        # Look for applications section
        app_section = soup.find(text=re.compile(r'Application', re.I))
        if app_section:
            app_content = app_section.find_parent(['div', 'section'])
            if app_content:
                app_items = app_content.find_all(['li', 'p'])
                material_data['applications'] = [
                    item.get_text(strip=True) for item in app_items if item.get_text(strip=True)
                ]

        # Extract composition if available
        comp_section = soup.find(text=re.compile(r'Composition|Chemical', re.I))
        if comp_section:
            comp_table = comp_section.find_parent('table') or comp_section.find_next('table')
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

                # Skip empty or header rows
                if not property_value or property_value in ['-', 'N/A', 'Property', 'Value']:
                    continue

                # Categorize property
                property_lower = property_name.lower()

                if any(keyword in property_lower for keyword in [
                    'density', 'melting', 'boiling', 'specific gravity', 'molecular'
                ]):
                    material_data['physical_properties'][property_name] = property_value

                elif any(keyword in property_lower for keyword in [
                    'tensile', 'yield', 'elongation', 'hardness', 'modulus',
                    'strength', 'impact', 'fatigue', 'elastic', "young's"
                ]):
                    material_data['mechanical_properties'][property_name] = property_value

                elif any(keyword in property_lower for keyword in [
                    'thermal', 'conductivity', 'expansion', 'specific heat',
                    'heat capacity', 'temperature'
                ]):
                    material_data['thermal_properties'][property_name] = property_value

                elif any(keyword in property_lower for keyword in [
                    'electrical', 'resistivity', 'dielectric', 'conductivity'
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

                # Skip header rows
                if element.lower() in ['element', 'component'] or not percentage:
                    continue

                composition[element] = percentage

        return composition

    def search_by_property(
        self,
        property_name: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for materials by specific property criteria.

        Args:
            property_name: Name of property (e.g., "tensile strength", "density")
            min_value: Minimum value for the property
            max_value: Maximum value for the property

        Returns:
            List of materials matching the criteria
        """
        # Build a search query based on the property
        query = property_name

        if min_value is not None:
            query += f" {min_value}"
        if max_value is not None:
            query += f" {max_value}"

        self.logger.info(f"Searching by property: {query}")
        return self.search(query)
