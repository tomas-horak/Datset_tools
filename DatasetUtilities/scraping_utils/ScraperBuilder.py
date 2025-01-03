from urllib.parse import quote

from DatasetUtilities.scraping_utils.scrapers.AzureBingSearch import AzureBingSearch
from DatasetUtilities.scraping_utils.scrapers.FlickrAPISearch import FlickrImageExtractor
from DatasetUtilities.scraping_utils.scrapers.GoogleSearchAPI import GoogleSearchAPI
from DatasetUtilities.scraping_utils.scrapers.PixabaySearchAPI import PixabayImageExtractor


class ScraperBuilder:
    def __init__(self, query):
        self.query = quote(query)
        self.pool_of_URLs = []
        self.scrapers = []

    def add_bing_scraper(self, params):
        self.scrapers.append((AzureBingSearch, params))
        return self

    def add_google_scraper(self, params):
        self.scrapers.append((GoogleSearchAPI, params))
        return self

    def add_flickr_scraper(self, params):
        self.scrapers.append((FlickrImageExtractor, params))
        return self

    def add_pixabay_scraper(self, params):
        self.scrapers.append((PixabayImageExtractor, params))
        return self

    def scrape(self, query):
        """
        Execute all added scrapers and aggregate results.
        """
        for scraper, params in self.scrapers:
            api_key = params.get('api_key', None)
            count = params.get('count', 100)
            self.pool_of_URLs.extend(scraper.scrape_images(query, api_key, count))
        return self.pool_of_URLs
