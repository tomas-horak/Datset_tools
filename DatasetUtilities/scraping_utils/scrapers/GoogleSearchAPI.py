import requests

from DatasetUtilities.scraping_utils.scrapers.AbstractScraper import AbstractScraper


class GoogleSearchAPI(AbstractScraper):

    @staticmethod
    def scrape_images(query, api_key=None, count=100):
        """
          Google Custom Search API

          Parameters:
              api_key: dict of API key and Search engine ID
              query (str): Search query string.
              count (int): Number of results to fetch

          Returns:
              list: list of URLs
          """

        api_key, search_id = api_key
        base_url = "https://www.googleapis.com/customsearch/v1"
        num_results_per_page = 10  # Maximum allowed by API
        all_results = []

        for start in range(1, min(count, 100) + 1, num_results_per_page):
            params = {
                "key": api_key,
                "cx": search_id,
                "q": query,
                "lr": "lang_cs",
                "start": start,
                "num": num_results_per_page
            }
            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()  # Raise HTTPError for bad responses
                data = response.json()
                items = data.get("items", [])
                all_results.extend(items)

                # Break if fewer results than requested are returned (end of results)
                if len(items) < num_results_per_page:
                    break
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                break

        return all_results

