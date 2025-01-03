import os

from DatasetUtilities.scraping_utils.scrapers.AzureBingSearch import bing_image_search
from DatasetUtilities.scraping_utils.scrapers.GoogleSearchAPI import google_custom_search_all
from DatasetUtilities.scraping_utils.image_downloader import download_image
from dotenv import load_dotenv

load_dotenv()
from urllib.parse import quote

# keys
flickr_api_key = os.environ.get("FLICKR_API_KEY")
pixabay_api_key = os.environ.get("PIXABAY_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")
google_search_key = os.environ.get("GOOGLE_SEARCH_ID")
bing_api_key = os.environ.get("BING_API_KEY")

# crossula ovata se nestáhla z API?? "crossula-ovata","dieffenbachia",  nedoběhlfa
# "kalanchoe", kalanchoe nedoběhla
# schafflera má jen 3??
# ZZko má taky málo
# flowers = ["spathiphyllum", "syngonium", "tradescantia", "verbena", "zamioculas", "iron cross begonia", "ctenanthe", "prayer plant", "calathea", "venus flytrap"]
plants = [
    "Codiaeum"
]


def process(query):
    output_folder = 'downloaded_images ' + query
    os.makedirs(output_folder, exist_ok=True)
    """
    extractor = FlickrImageExtractor()
    urls = extractor.get_urls(flickr_api_key, query)
    print(urls)
    for index, url in enumerate(urls):
        download_image(url, output_folder)
        time.sleep(1)
        print(f'flickr {index} / {len(urls)}')

    pixabay_extractor = PixabayImageExtractor()
    urls = pixabay_extractor.get_urls(pixabay_api_key, query)
    for index, url in enumerate(urls):
        download_image(url, output_folder)
        time.sleep(random.uniform(1, 5))
        print(f'pixabay {index} / {len(urls)}')

    """
    results_bing = bing_image_search(query, bing_api_key, count=150)

    print("Image URLs:")
    for url in results_bing:
        download_image(url, output_folder)
        print(url)

    results = google_custom_search_all(google_api_key, google_search_key, query)
    for result in results:
        image_url = result.get('pagemap', {}).get('cse_image', [{}])[0].get('src')
        print(image_url)
        download_image(image_url, output_folder)


for plant in plants:
    process(quote(plant))

""" results = google_custom_search_all(google_api_key, google_search_key, query)
    for result in results:
        image_url = result.get('pagemap', {}).get('cse_image', [{}])[0].get('src')
        print(image_url)
        download_image(image_url, output_folder)"""
