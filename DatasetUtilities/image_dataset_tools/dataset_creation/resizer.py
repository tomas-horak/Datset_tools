import logging
import shutil

from PIL import Image
import os


class ImageResizer:
    def __init__(self, input_directory, output_directory = None, dimension = 128, dataset_type = "mono_dataset"):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.dimension = dimension
        self.type = dataset_type

        if not self.output_directory:
            self.output_directory = self.input_directory

    def __create_target_folder(self):
        try:
            os.makedirs(self.output_directory, exist_ok=True)
        except Exception as e:
            logging.error(f"could not create target dir, cause {e}")

    def __create_class_folders(self):
        folders = os.listdir(self.input_directory)
        for folder in folders:
            path = os.path.join(self.output_directory, folder)
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                logging.error(f"could not create target class dir, cause {e}")

    def __process_directory(self):
        folders = os.listdir(self.input_directory)
        if not folders:
            logging.error("No files found.")
            return
        if self.type == "folders_dataset":
            for folder in folders:
                input_folder_path = os.path.join(self.input_directory, folder)
                output_folder_path = os.path.join(self.output_directory, folder)
                self.__process_folder(input_folder_path, output_folder_path)

        elif self.type == "mono_dataset":
            self.__process_folder(self.input_directory, self.output_directory)

    def __process_folder(self, input_folder, output_folder):

        for filename in os.listdir(input_folder):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                logging.warning(f"Skipping non-image file: {filename}")
                continue

            try:
                self.__make_image_resized_square(input_image_path, output_image_path)
            except Exception as e:
                logging.warning(f"Could not resize: {filename}, reason: {e}")

    def __make_image_resized_square(self, input_path, output_path):
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

    def process(self):
        self.__create_target_folder()
        self.__create_class_folders()
        self.__process_directory()



