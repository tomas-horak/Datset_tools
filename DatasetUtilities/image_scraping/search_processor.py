

import os

from dotenv import load_dotenv

from DatasetUtilities.image_scraping.image_downloader import ImageDownloader
from DatasetUtilities.image_scraping.scraper_builder import ScraperBuilder

if not load_dotenv():
    raise Exception("no .env file found")


# keys to .env file
flickr_api_key = os.environ.get("FLICKR_API_KEY")
pixabay_api_key = os.environ.get("PIXABAY_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")
google_search_key = os.environ.get("GOOGLE_SEARCH_ID")
bing_api_key = os.environ.get("BING_API_KEY")
pexels_api_key = os.environ.get("PEXELS_API_KEY")

downloader = ImageDownloader()

builder = ScraperBuilder("schefflera", downloader, "./Dypsis Lutescens houseplant")

builder.add_pexels_scraper({"api_key": pexels_api_key, "count": 1})

builder.process()


