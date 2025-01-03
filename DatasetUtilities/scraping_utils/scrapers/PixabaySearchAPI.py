import requests

from DatasetUtilities.scraping_utils.scrapers.AbstractScraper import AbstractScraper


class PixabayImageExtractor(AbstractScraper):
    """
    https://pixabay.com/api/docs/
    """
    # maybe add page parameter

    @staticmethod
    def scrape_images(query, api_key=None, count=100):
        params = {
            'key': api_key,
            'q': query,
            'image_type': 'photo',
            'per_page': count
        }
        api_endpoint = 'https://pixabay.com/api/'
        response = requests.get(api_endpoint, params=params)
        data = response.json()
        if response.status_code == 200:
            if data is None:
                return []
            hits = data.get('hits', [])
            urls = []
            for hit in hits:
                urls.append(hit['webformatURL'])
            return urls
        else:
            return []
