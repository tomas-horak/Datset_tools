import requests

from DatasetUtilities.scraping_utils.scrapers.AbstractScraper import AbstractScraper


class FlickrImageExtractor(AbstractScraper):
    """
    https://www.flickr.com/services/api/flickr.photos.search.html
    """

    @staticmethod
    def scrape_images(query, api_key=None, count=100):
        """
        :param query: search query
        :param api_key: Flickr api key
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

        response = requests.get(api_endpoint, params=request_params)
        data = response.json()

        if data is None:
            print("Flickr response is empty")
            return []

        photos = data.get('photos', {}).get('photo', [])
        urls = []
        for photo in photos:
            server_id = photo['server']
            photo_id = photo['id']
            secret = photo['secret']
            size = 'z'
            url = f"https://live.staticflickr.com/{server_id}/{photo_id}_{secret}_{size}.jpg"
            urls.append(url)
        return urls

