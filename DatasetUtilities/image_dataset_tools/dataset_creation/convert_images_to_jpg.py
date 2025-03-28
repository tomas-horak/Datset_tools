import logging
import shutil

from PIL import Image
import os


class NormaliseFileTypeAndNameInDataset:
    def __init__(self, input_folder_path, output_folder_path):
        self.input_directory = input_folder_path
        self.output_directory = output_folder_path
        self.folder_name_mapping = {}

    def create_target_folder(self):
        try:
            os.makedirs(self.output_directory, exist_ok=True)
        except Exception as e:
            logging.error(f"could not create target dir, cause {e}")

    def create_class_folders(self):
        folders = os.listdir(self.input_directory)
        for folder in folders:
            normalized_name = folder.lower().replace(" ", "-")
            self.folder_name_mapping[folder] = normalized_name
            path = os.path.join(self.output_directory, folder)
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                logging.error(f"could not create target class dir, cause {e}")

    def convert(self):
        folders = os.listdir(self.input_directory)
        for folder in folders:
            folder_path = os.path.join(self.input_directory, folder)
            if not os.path.isdir(folder_path):
                logging.warning(f"{folder_path} is not a folder")
                continue
            folder_name_lowercase = folder.lower()
            normalised_folder_name = folder_name_lowercase.replace(" ", "-")

            file_list = os.listdir(os.path.join(self.input_directory, folder))
            for i, file in enumerate(file_list):
                filename_before = os.path.join(self.input_directory, folder, file)
                if os.path.isdir(filename_before):
                    logging.warning(f"{folder_path} is not a image file")
                    continue

                filename_after = normalised_folder_name + "-" + str(i)
                image_output_path = os.path.join(self.output_directory, folder, filename_after)

                image = Image.open(filename_before)
                rgb_im = image.convert("RGB")
                rgb_im.save(f"{image_output_path}.jpg")

    def rename_class_folders(self):
        for original_name, normalized_name in self.folder_name_mapping.items():
            original_path = os.path.join(self.output_directory, original_name)
            normalized_path = os.path.join(self.output_directory, normalized_name)

            if os.path.exists(original_path) and original_name != normalized_name:
                try:
                    os.rename(original_path, normalized_path)
                    logging.info(f"Renamed folder {original_name} -> {normalized_name}")
                except Exception as e:
                    logging.error(f"Could not rename {original_name} -> {normalized_name}: {e}")

    def process(self):
        logging.info("Creating target folder")
        self.create_target_folder()
        logging.info("Creating class folders")
        self.create_class_folders()
        logging.info("Converting files")
        self.convert()
        logging.info("Renaming class folders")
        self.rename_class_folders()
        logging.info("Done")




