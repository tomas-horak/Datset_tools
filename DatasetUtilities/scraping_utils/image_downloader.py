import os
import requests
import hashlib
from urllib.parse import urlparse, unquote


def download_image(url, folder):
    # Vytvoření složky, pokud neexistuje
    os.makedirs(folder, exist_ok=True)

    try:
        # Stažení obrázku z URL
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = create_filename_from_url(url)
            file_path = os.path.join(folder, f"{filename}.jpg")

            # Uložení obrázku
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"Downloaded: {file_path}")
            return file_path
        else:
            # Chybová hláška, pokud status není 200
            error_msg = f"Failed to download {url} (Status Code: {response.status_code})"
            print(error_msg)
            return error_msg
    except Exception as e:
        # Zachycení výjimek a vypsání chyby
        error_msg = f"Error downloading {url}: {e}"
        print(error_msg)
        return error_msg


import os
from urllib.parse import urlparse


def create_filename_from_url(url):
    decoded_url = unquote(url)
    url_hash = hashlib.md5(decoded_url.encode()).hexdigest()

    return url_hash

