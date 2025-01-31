from abc import ABC, abstractmethod
import logging


class AbstractScraper(ABC):
    """
    Base class for all scrapers. Provides a common interface and reusable utilities for scraping images.
    """

    @staticmethod
    @abstractmethod
    def scrape_images(query, api_key=None, count=100) -> list:
        """
        Abstract method to scrape images.
        :param query: Search query string
        :param api_key: API key for the service (if required)
        :param count: Number of images to retrieve
        :return: List of image URLs
        """
        pass

    @staticmethod
    def validate_response(response):
        """
        Validates the HTTP response.
        Logs an error for non-200 status codes instead of raising an exception.

        :param response: requests.Response object
        :return: True if valid, False otherwise
        """
        if response.status_code != 200:
            logging.error(
                f"Unexpected HTTP status code {response.status_code}: {response.text}"
            )
            return False
        return True

    @staticmethod
    def parse_json_response(response):
        """
        Safely parses the JSON response.
        Logs an error if JSON parsing fails.

        :param response: requests.Response object
        :return: Parsed JSON data or None
        """
        try:
            return response.json()
        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            return None
