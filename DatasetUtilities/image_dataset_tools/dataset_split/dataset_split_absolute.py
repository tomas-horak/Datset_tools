import logging
import os
import random
import shutil

class ImagesFromFolderDatasetAbsolute:

    def __init__(self, input_folder_path, output_valid_path, output_test_path, num_val, num_test):
        """
        Constructor to initialize paths and fixed numbers of validation and test samples.

        :param input_folder_path: Path to the input folder containing datasets
        :param output_valid_path: Path to the Dypsis Lutescens houseplant validation folder
        :param output_test_path: Path to the Dypsis Lutescens houseplant test folder
        :param num_val: Fixed number of validation samples per class
        :param num_test: Fixed number of test samples per class
        """
        self.input = input_folder_path
        self.valid_output = output_valid_path
        self.test_output = output_test_path
        self.num_val = num_val
        self.num_test = num_test

    def handle_folders(self):
        """Creates the required directories for validation, test, and train datasets."""
        self.create_target_folder(self.valid_output)
        self.create_class_folders(self.valid_output)

        self.create_target_folder(self.test_output)
        self.create_class_folders(self.test_output)


    def create_target_folder(self, path):
        """Creates a target folder if it doesn't exist."""
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            logging.error(f"Could not create target dir {path}, cause {e}")

    def create_class_folders(self, folder_path):
        """Creates class-specific folders inside the target folder."""
        folders = os.listdir(self.input)
        for folder in folders:
            path = os.path.join(folder_path, folder)
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                logging.error(f"Could not create class dir {path}, cause {e}")

    def split_dataset(self):
        """Split the dataset into train, validation, and test based on fixed numbers."""
        folders = os.listdir(self.input)
        for folder in folders:
            file_list = os.listdir(os.path.join(self.input, folder))

            # Ensure the number of test/validation samples doesn't exceed available files
            test_samples = random.sample(file_list, min(self.num_test, len(file_list)))
            remaining_files = list(set(file_list) - set(test_samples))
            val_samples = random.sample(remaining_files, min(self.num_val, len(remaining_files)))
            train_samples = list(set(remaining_files) - set(val_samples))

            # Move or copy test samples
            for sample in test_samples:
                input_path = os.path.join(self.input, folder, sample)
                output_path = os.path.join(self.test_output, folder, sample)
                try:
                    shutil.move(input_path, output_path)
                except Exception as e:
                    logging.error(f"Could not move test file {sample}, cause: {e}")

            # Move or copy validation samples
            for sample in val_samples:
                input_path = os.path.join(self.input, folder, sample)
                output_path = os.path.join(self.valid_output, folder, sample)
                try:
                    shutil.move(input_path, output_path)
                except Exception as e:
                    logging.error(f"Could not move validation file {sample}, cause: {e}")


    def process(self):
        """Main method to execute the dataset splitting process."""
        self.handle_folders()
        self.split_dataset()
