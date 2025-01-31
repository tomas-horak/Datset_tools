import shutil

from PIL import Image
import os


class ImageResizer:
    def __init__(self, dataset_directory, output_directory, dimension):
        self.dataset_directory = dataset_directory
        self.output_directory = output_directory
        self.dimension = dimension

    def process_directory(self):
        os.makedirs(self.output_directory, exist_ok=True)

        for filename in os.listdir(self.dataset_directory):
            input_path = os.path.join(self.dataset_directory, filename)
            output_path = os.path.join(self.output_directory, filename)

            # Check if the file is an image
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                shutil.copy(input_path, self.output_directory)
                print(f"Skipping non-image file: {filename}")
                continue

            try:
                self.make_image_resized_square(input_path, output_path)
            except Exception as e:
                print(f"Skipping {filename}: {e}")

    def make_image_resized_square(self, input_path, output_path):
        with Image.open(input_path) as img:
            width, height = img.size
            crop_box = None
            img = img.convert('RGB')

            if width != height:
                if width > height:
                    offset = (width - height) // 2
                    crop_box = (offset, 0, width - offset, height)

                else:
                    offset = (height - width) // 2
                    crop_box = (0, offset, width, height - offset)

            img = img.crop(crop_box)
            img.thumbnail((self.dimension, self.dimension))
            img.save(output_path)
