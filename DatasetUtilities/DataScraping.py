import os
from dotenv import load_dotenv

from DatasetUtilities.image_scraping.image_downloader import ImageDownloader
from DatasetUtilities.image_scraping.scraper_builder import ScraperBuilder


class DataScraper:

    def __init__(self, query, images_per_source, output_folder="./output", use_scrapers=None):
        """
        Initializes the DataScraper instance.

        :param query: The search query for images (e.g., "schefflera")
        :param output_folder: Folder to save the downloaded images
        :param use_scrapers: Dictionary of scrapers to enable (optional)
        """
        self.query = query
        self.output_folder = output_folder
        self.downloader = ImageDownloader()
        self.images_per_source = images_per_source


        # Load API keys from .env file
        if not load_dotenv():
            raise Exception("no .env file found")

        # Load the API keys for each scraper (they may or may not be present)
        self.flickr_api_key = os.environ.get("FLICKR_API_KEY")
        self.pixabay_api_key = os.environ.get("PIXABAY_API_KEY")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        self.google_search_ID = os.environ.get("GOOGLE_SEARCH_ID")
        self.bing_api_key = os.environ.get("BING_API_KEY")
        self.pexels_api_key = os.environ.get("PEXELS_API_KEY")

        # Configuration to select which scrapers to use
        self.use_scrapers = use_scrapers or {}

    def add_scrapers(self, builder):
        """
        Dynamically add scrapers based on available API keys and user selection.
        :param builder: ScraperBuilder instance.
        :return: Updated builder with the selected scrapers.
        """
        if self.use_scrapers.get('pexels', False) and self.pexels_api_key:
            builder.add_pexels_scraper({"api_key": self.pexels_api_key, "count": self.images_per_source})

        if self.use_scrapers.get('flickr', False) and self.flickr_api_key:
            builder.add_flickr_scraper({"api_key": self.flickr_api_key, "count": self.images_per_source})

        if self.use_scrapers.get('pixabay', False) and self.pixabay_api_key:
            builder.add_pixabay_scraper({"api_key": self.pixabay_api_key, "count": self.images_per_source})

        if self.use_scrapers.get('google', False) and self.google_api_key:
            builder.add_google_scraper({"api_key": (self.google_api_key, self.google_search_ID), "count": self.images_per_source})

        if self.use_scrapers.get('bing', False) and self.bing_api_key:
            builder.add_bing_scraper({"api_key": self.bing_api_key, "count": self.images_per_source})

        return builder

    def scrape(self):
        """
        Orchestrates the entire scraping and downloading process.
        """
        # Initialize the ScraperBuilder
        builder = ScraperBuilder(self.query, self.downloader, self.output_folder)

        # Add scrapers dynamically to the builder
        builder = self.add_scrapers(builder)

        # Start the scraping and downloading process
        builder.process()

        print(f"Scraping and downloading for query '{self.query}' completed successfully!")
