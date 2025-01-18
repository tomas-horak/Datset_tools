import logging
from urllib.parse import unquote

import requests
from DatasetUtilities.scraping_utils.scrapers.AbstractScraper import AbstractScraper


class PixabayImageExtractor(AbstractScraper):
    """
    Pixabay API Scraper with Pagination Support
    Documentation: https://pixabay.com/api/docs/
    """

    @staticmethod
    def scrape_images(query, api_key=None, count=100):
        if not api_key:
            logging.error("Pixabay API key is missing.")
            return []

        # Constants
        API_ENDPOINT = 'https://pixabay.com/api/'
        collected_images = []
        page = 1  # Start with the first page
        query = unquote(query)
        formatted_query = query.strip().replace(" ", "+") #!!! different than URL formatting

        while len(collected_images) < count:

            params = {
                'key': api_key,
                'q': formatted_query,
                'image_type': 'photo',
                'page': page,
            }

            try:
                response = requests.get(API_ENDPOINT, params=params)

                # Validate the response
                if not AbstractScraper.validate_response(response):
                    break

                data = AbstractScraper.parse_json_response(response)
                if not data or 'hits' not in data:
                    logging.warning("No hits found in Pixabay response.")
                    break

                # Extract URLs and update the collected list
                hits = data['hits']
                collected_images.extend(
                    hit.get('webformatURL') for hit in hits if 'webformatURL' in hit
                )

                page += 1  # Increment the page number

            except Exception as e:
                logging.error(f"Error while fetching images from Pixabay: {e}")
                break

        return collected_images[:count]  # Return only the requested number of URLs
