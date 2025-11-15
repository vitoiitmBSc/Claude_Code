"""
Base scraper class with common functionality for all material database scrapers.
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseScraper(ABC):
    """
    Abstract base class for material property scrapers.

    Provides common functionality like:
    - Rate limiting
    - Request handling with retries
    - Error handling
    - Session management
    """

    def __init__(
        self,
        rate_limit: float = 1.0,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize the base scraper.

        Args:
            rate_limit: Minimum seconds between requests (default: 1.0)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retry attempts (default: 3)
        """
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.max_retries = max_retries
        self.last_request_time = 0.0
        self.session = self._create_session()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry logic.

        Returns:
            Configured requests Session object
        """
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set a user agent to be respectful
        session.headers.update({
            'User-Agent': 'MaterialPropertiesScraper/1.0 (Educational/Research)'
        })

        return session

    def _rate_limit_wait(self) -> None:
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.rate_limit:
            wait_time = self.rate_limit - time_since_last_request
            self.logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)

        self.last_request_time = time.time()

    def fetch_url(self, url: str, params: Optional[Dict] = None) -> Optional[str]:
        """
        Fetch content from a URL with rate limiting and error handling.

        Args:
            url: The URL to fetch
            params: Optional query parameters

        Returns:
            HTML content as string, or None if request failed
        """
        self._rate_limit_wait()

        try:
            self.logger.info(f"Fetching: {url}")
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.text

        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout while fetching {url}")
            return None

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for {url}")
            return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            return None

    @abstractmethod
    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for materials matching the query.

        Args:
            query: Search query (e.g., "stainless steel", "aluminum alloy")
            filters: Optional filters (e.g., application, environment)

        Returns:
            List of material results with basic information
        """
        pass

    @abstractmethod
    def get_material_properties(
        self,
        material_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed properties for a specific material.

        Args:
            material_id: Unique identifier for the material

        Returns:
            Dictionary containing material properties, or None if not found
        """
        pass

    @abstractmethod
    def get_database_name(self) -> str:
        """
        Get the name of the database this scraper targets.

        Returns:
            Database name as string
        """
        pass

    def close(self) -> None:
        """Close the session and cleanup resources."""
        if self.session:
            self.session.close()
            self.logger.info("Session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
