import os


from DatasetUtilities.DatasetTools import DatasetTools

from dotenv import load_dotenv
load_dotenv()

# keys to .env file
flickr_api_key = os.environ.get("FLICKR_API_KEY")
pixabay_api_key = os.environ.get("PIXABAY_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")
google_search_key = os.environ.get("GOOGLE_SEARCH_ID")
bing_api_key = os.environ.get("BING_API_KEY")



#DatasetTools.resize_images("/Users/tomashorak/PycharmProjects/ML_dataset_parser/flowers", "./resized", 224)

#DatasetTools.create_dataset_from_folders("/Users/tomashorak/PycharmProjects/ML_dataset_parser/resized", "./resized_dataset")

#DatasetTools.create_dataset_from_folders("/Users/tomashorak/PycharmProjects/ML_dataset_parser/flowers-small-25", "./flowers")

#DatasetTools.labels_to_numbers("/Users/tomashorak/PycharmProjects/ML_dataset_parser/classes.csv", "./encoded.csv", "./docs")

DatasetTools.decompose_dataset("/Users/tomashorak/PycharmProjects/ML_dataset_parser/resized", "/Users/tomashorak/PycharmProjects/ML_dataset_parser/encoded.csv", "./flowers_full_decomposed")