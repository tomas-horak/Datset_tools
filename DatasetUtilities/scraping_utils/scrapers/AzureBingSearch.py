import requests

from DatasetUtilities.scraping_utils.scrapers.AbstractScraper import AbstractScraper


class AzureBingSearch(AbstractScraper):

    @staticmethod
    def scrape_images(query, api_key=None, count=100):
        """
        Searches Bing for image thumbnails and returns a list of thumbnail URLs.
        The key should be obtained through Azure.

        :param query: Search query
        :param api_key: Bing Search API key.
        :param count: Number of results to fetch (default is 10).
        :return: List of thumbnail URLs.
        """
        url = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        params = {"q": query, "count": count}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            print(data.get("value"))
            # Extract thumbnail URLs from the response
            thumbnail_urls = [img["thumbnailUrl"] for img in data.get("value", [])]
            return thumbnail_urls
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []

