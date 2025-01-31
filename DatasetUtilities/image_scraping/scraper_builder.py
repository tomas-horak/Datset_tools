import os
import time
from urllib.parse import quote

from DatasetUtilities.image_scraping.scrapers.azure_bing_search import AzureBingSearch
from DatasetUtilities.image_scraping.scrapers.flickr_api_search import FlickrImageExtractor
from DatasetUtilities.image_scraping.scrapers.google_search_api import GoogleSearchAPI
from DatasetUtilities.image_scraping.scrapers.pexels_api_search import PexelsImageSearch
from DatasetUtilities.image_scraping.scrapers.pixabay_api_search import PixabayImageExtractor


class ScraperBuilder:
    def __init__(self, query, downloader, path_to_output, download_delay_ms = 0.5):
        self.query = query
        self.pool_of_URLs = []
        self.scrapers = []
        self.downloader = downloader
        self.path_to_output = path_to_output
        self.delay = download_delay_ms

    def add_bing_scraper(self, params):
        self.scrapers.append((AzureBingSearch, params))
        return self

    def add_google_scraper(self, params):
        self.scrapers.append((GoogleSearchAPI, params))
        return self

    def add_pexels_scraper(self, params):
        self.scrapers.append((PexelsImageSearch, params))
        return self

    def add_flickr_scraper(self, params):
        self.scrapers.append((FlickrImageExtractor, params))
        return self

    def add_pixabay_scraper(self, params):
        self.scrapers.append((PixabayImageExtractor, params))
        return self

    def scrape(self):
        """
        Execute all added scrapers and aggregate results.
        """
        for scraper, params in self.scrapers:
            api_key = params.get('api_key', None)
            count = params.get('count', 100)
            urls = scraper.scrape_images(self.query, api_key, count)
            self.pool_of_URLs.extend(urls)
        return self.pool_of_URLs

    def download_images(self):
        number_of_urls = len(self.pool_of_URLs)

        for index, url in enumerate(self.pool_of_URLs, start=1):
            print(f"Downloading image {index} of {number_of_urls}: {url}")
            self.downloader.download_image(url, self.path_to_output)
            time.sleep(self.delay)

    def create_target_directory(self):
        os.makedirs(self.path_to_output, exist_ok=True)

    def process(self):
        print("creating output directory")
        self.create_target_directory()
        print("searching")
        self.scrape()
        print("downloading")
        self.download_images()

