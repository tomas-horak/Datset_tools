import requests

from DatasetUtilities.image_scraping.scrapers.abstract_scraper import AbstractScraper


class AzureBingSearch(AbstractScraper):
    @staticmethod
    def scrape_images(query, api_key=None, count=100):
        """
        Searches Bing for image thumbnails and returns a list of thumbnail URLs.
        The key should be obtained through Azure.

        :param query: Search query
        :param api_key: Bing Search API key.
        :param count: Number of results to fetch (default is 100).
        :return: List of thumbnail URLs.
        """
        url = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        max_per_request = 150  # Bing API allows up to 150 results per request
        thumbnail_urls = []
        offset = 0

        while len(thumbnail_urls) < count:
            params = {
                "q": query,
                "count": min(max_per_request, count - len(thumbnail_urls)),
                "offset": offset,
            }
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                images = data.get("value", [])

                # Extract thumbnail URLs
                for img in images:
                    if "thumbnailUrl" in img:
                        thumbnail_urls.append(img["thumbnailUrl"])

                # Break if fewer results than requested are returned (end of results)
                if len(images) < params["count"]:
                    break

                # Update offset for the next page
                offset += params["count"]

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                break

        # Trim the result to the requested count, if necessary
        return thumbnail_urls[:count]
