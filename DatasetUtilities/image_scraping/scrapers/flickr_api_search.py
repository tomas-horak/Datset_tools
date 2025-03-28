from urllib.parse import unquote

import requests
import logging

from DatasetUtilities.image_scraping.scrapers.abstract_scraper import AbstractScraper


class FlickrImageExtractor(AbstractScraper):
    """
    https://www.flickr.com/services/api/flickr.photos.search.html
    """

    def scrape_images(self, query, api_key=None, count=100):
        """
        :param query: search query
        :param api_key: Flickr API key
        :param count: number of results, max 500
        :return: list of found URLs
        """

        api_endpoint = 'https://api.flickr.com/services/rest/'
        request_params = {
            'method': 'flickr.photos.search',
            'api_key': api_key,
            'text': query,
            'format': 'json',
            'nojsoncallback': 1,
            'per_page': count,
        }

        try:
            response = requests.get(api_endpoint, params=request_params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        except requests.exceptions.RequestException as e:
            # Catch network-related errors (timeouts, DNS errors, etc.)
            logging.error(f"Network error while calling Flickr API: {e}")
            return []

        data = self.parse_json_response(response)

        #data = AbstractScraper.parse_json_response(response)

        if data is None or 'photos' not in data or 'photo' not in data['photos']:
            logging.warning("Flickr response is empty or malformed")
            return []

        photos = data['photos']['photo']
        if not photos:
            logging.info(f"No photos found for query: {query}")
            return []

        urls = []
        for photo in photos:
            try:
                # Extract necessary information from the photo data
                server_id = photo['server']
                photo_id = photo['id']
                secret = photo['secret']
                size = 'z'  # Using 'z' size for medium resolution

                # Construct the image URL
                url = f"https://live.staticflickr.com/{server_id}/{photo_id}_{secret}_{size}.jpg"
                urls.append(url)

            except KeyError as e:
                # Handle missing expected keys in the response data
                logging.warning(f"Missing expected data in Flickr response: {e}")
                continue

        return urls
