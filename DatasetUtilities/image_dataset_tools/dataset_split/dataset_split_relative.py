import logging
import os
import random
import shutil


class ImagesFromFolderDataset:

    def __init__(self, input_folder_path, output_test_path, output_train_path = None, test_split = 0.2):
        self.input = input_folder_path
        self.test_output = output_test_path
        self.train_output = output_train_path
        self.test_split = test_split

    def handle_folders(self):
        self.create_target_folder(self.test_output)
        self.create_class_folders(self.test_output)

        if self.train_output:
            self.create_target_folder(self.train_output)
            self.create_class_folders(self.train_output)

    def create_target_folder(self, path):
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            logging.error(f"could not create target dir, cause {e}")

    def create_class_folders(self, folder_path):
        folders = os.listdir(self.input)
        for folder in folders:
            path = os.path.join(folder_path, folder)
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                logging.error(f"could not create target class dir, cause {e}")

    def extract_from_input_dataset(self):
        folders = os.listdir(self.input)
        for folder in folders:
            file_list = os.listdir(os.path.join(self.input, folder))
            sample_size = int(len(file_list) * self.test_split)
            test_samples = random.sample(file_list, sample_size)

            for sample in test_samples:
                input_path = os.path.join(self.input, folder, sample)
                output_path = os.path.join(self.test_output, folder, sample)
                try:
                    shutil.move(input_path, output_path)
                except Exception as e:
                    logging.error(f"could not move file, cause {e}")

    def copy_from_input_dataset(self):
        folders = os.listdir(self.input)
        for folder in folders:
            file_list = os.listdir(os.path.join(self.input, folder))

            # Determine sample sizes
            sample_size = int(len(file_list) * self.test_split)  # 20% for test
            test_samples = random.sample(file_list, sample_size)
            train_samples = list(set(file_list) - set(test_samples))

            # Copy test samples
            for sample in test_samples:
                input_path = os.path.join(self.input, folder, sample)
                output_path = os.path.join(self.test_output, folder, sample)
                try:
                    shutil.copy2(input_path, output_path)
                except Exception as e:
                    logging.error(f"Could not copy test file {sample}, cause: {e}")

            # Copy train samples
            for sample in train_samples:
                input_path = os.path.join(self.input, folder, sample)
                output_path = os.path.join(self.train_output, folder, sample)
                try:
                    shutil.copy2(input_path, output_path)
                except Exception as e:
                    logging.error(f"Could not copy train file {sample}, cause: {e}")

    def process(self):
        self.handle_folders()
        if self.train_output:
            self.copy_from_input_dataset()
        else:
            self.extract_from_input_dataset()



