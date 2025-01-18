from urllib.parse import quote

import requests
from DatasetUtilities.scraping_utils.scrapers.AbstractScraper import AbstractScraper


class PexelsImageSearch(AbstractScraper):

    @staticmethod
    def scrape_images(query, api_key=None, max_results=500):
        """
        Searches Pexels for images and returns a list of image URLs.
        Retrieves images across multiple pages to maximize results.

        :param query: Search query.
        :param api_key: Pexels API key.
        :param max_results: Maximum number of image URLs to fetch.
        :return: List of image URLs.
        """
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": api_key}
        per_page = 80  # Pexels API pagination limit
        page = 1
        collected_images = []

        while len(collected_images) < max_results:
            params = {"query": query, "per_page": per_page, "page": page}
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                photos = data.get("photos", [])

                # Stop if there are no more photos to fetch
                if not photos:
                    break

                # Extract image URLs and add them to the list
                collected_images.extend([photo["src"]["medium"] for photo in photos])

                # Check if we've reached the total results
                total_results = data.get("total_results", 0)
                if len(collected_images) >= min(total_results, max_results):
                    break

                # Move to the next page
                page += 1
            else:
                print(f"Error: {response.status_code}, {response.text}")
                break

        return collected_images[:max_results]
