import os
from urllib.parse import quote


from DatasetUtilities.scraping_utils.scrapers.AzureBingSearch import AzureBingSearch
from DatasetUtilities.scraping_utils.scrapers.FlickrAPISearch import FlickrImageExtractor
from DatasetUtilities.scraping_utils.scrapers.GoogleSearchAPI import GoogleSearchAPI
from DatasetUtilities.scraping_utils.scrapers.PexelsScraper import PexelsImageSearch
from DatasetUtilities.scraping_utils.scrapers.PixabaySearchAPI import PixabayImageExtractor


class ScraperBuilder:
    def __init__(self, query, downloader, path_to_output):
        self.query = quote(query)
        self.pool_of_URLs = []
        self.scrapers = []
        self.downloader = downloader
        self.path_to_output = path_to_output

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
            print(scraper)
            api_key = params.get('api_key', None)
            count = params.get('count', 100)
            urls = scraper.scrape_images(self.query, api_key, count)
            self.pool_of_URLs.extend(urls)
        return self.pool_of_URLs

    def download_images(self):
        for url in self.pool_of_URLs:
            self.downloader.download_image(url, self.path_to_output)

    def create_target_directory(self):
        os.makedirs(self.path_to_output, exist_ok=True)

    def process(self):
        print("creating output directory")
        self.create_target_directory()
        print("searching")
        self.scrape()
        print("downloading")
        self.download_images()

