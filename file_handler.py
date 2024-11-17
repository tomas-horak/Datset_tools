import os
import shutil


class FileHandler:
    def __init__(self, input_folder, output_folder, dataset):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.dataset = dataset

    def create_target_folder(self):
        os.makedirs(self.output_folder, exist_ok=True)

    def create_folders_for_classes(self):
        labels = self.dataset["category"]
        for label in labels:
            class_folder = os.path.join(self.output_folder, label.strip())
            os.makedirs(class_folder, exist_ok=True)

    def copy_files(self):
        for _, item in self.dataset.iterrows():
            filename = item['filename'].strip()
            category = item['category'].strip()

            source_path = os.path.join(self.input_folder, filename)
            class_folder = os.path.join(self.output_folder, category)
            destination_path = os.path.join(class_folder, filename)

            if os.path.exists(source_path):
                shutil.copy(source_path, destination_path)
            else:
                print(f"Warning: {filename} not found in {self.input_folder}")
