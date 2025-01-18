from urllib.parse import quote
import requests
from DatasetUtilities.scraping_utils.scrapers.AbstractScraper import AbstractScraper


class GoogleSearchAPI(AbstractScraper):
    @staticmethod
    def scrape_images(query, api_key=None, count=100):
        """
        Google Custom Search API

        Parameters:
            api_key: tuple of API key and Search engine ID
            query (str): Search query string.
            count (int): Number of results to fetch

        Returns:
            list: list of image URLs
        """
        api_key, search_id = api_key
        base_url = "https://www.googleapis.com/customsearch/v1"
        num_results_per_page = 10  # Maximum allowed by API
        all_image_urls = []
        start = 1  # API uses a 1-based index for results

        while len(all_image_urls) < count:
            params = {
                "key": api_key,
                "cx": search_id,
                "q": query,
                "lr": "lang_cs",  # Adjust language if needed
                "start": start,
                "num": num_results_per_page,
                "searchType": "image",  # Ensures image search
            }
            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()  # Raise HTTPError for bad responses
                data = response.json()
                items = data.get("items", [])

                # Extract image URLs from 'link' or 'pagemap' (if available)
                for item in items:
                    if "link" in item:
                        all_image_urls.append(item["link"])
                    elif "pagemap" in item and "cse_image" in item["pagemap"]:
                        for image in item["pagemap"]["cse_image"]:
                            all_image_urls.append(image.get("src"))

                # Increment the start index for the next page
                start += num_results_per_page

                # Break if fewer results than requested are returned (end of results)
                if len(items) < num_results_per_page:
                    break

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                break

        # Trim the result to the requested count, if necessary
        return all_image_urls[:count]
