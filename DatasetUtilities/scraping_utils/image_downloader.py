import os
import requests
import hashlib
from urllib.parse import urlparse, unquote


class ImageDownloader:

    @staticmethod
    def download_image(url, folder):
        """
        Downloads an image from the given URL and saves it to the specified folder.

        :param url: URL of the image to download.
        :return: File path of the downloaded image or an error message.
        """
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                filename = create_filename_from_url(url)
                file_path = os.path.join(folder, f"{filename}.jpg")

                # Save the image
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                return file_path
            else:
                error_msg = f"Failed to download {url} (Status Code: {response.status_code})"
                return error_msg
        except Exception as e:
            error_msg = f"URL exception{url}: {e}"
            print(error_msg)
            return error_msg

def create_filename_from_url(url):
    """
    Generates a unique filename for the image based on its URL.
    :param url: URL of the image.
    :return: A unique hash-based filename.
    """
    decoded_url = unquote(url)
    url_hash = hashlib.md5(decoded_url.encode()).hexdigest()
    return url_hash
