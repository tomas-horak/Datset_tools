import os
import shutil
import pandas as pd


class ImageFoldersToDataset:
    def __init__(self, path_to_folder_with_folders, output_path, dataset_type):
        self.input_folder_path = path_to_folder_with_folders
        self.output_path = output_path
        self.dataset_type = dataset_type

    def create_target_folder(self):
        try:
            os.makedirs(self.output_path, exist_ok=True)
        except Exception as e:
            raise OSError(f"Could not create folder at {self.output_path}. Reason: {e}")

    def convert_folders(self):
            folders = os.listdir(self.input_folder_path)
            filenames = []
            categories = []

            for folder in folders:
                file_list = os.listdir(os.path.join(self.input_folder_path, folder))
                for file in file_list:

                    source_path = os.path.join(self.input_folder_path, folder, file)
                    destination_path = os.path.join(self.output_path, file)
                    try:
                        shutil.copy(source_path, destination_path)
                    except:
                        print(f"image ${file} was not processed")
                        continue

                    filenames.append(file)
                    categories.append(folder)

            data = {"filename": filenames, "categories": categories}
            return data

    def create_one_hot_encoded(self, data):
        df = pd.DataFrame(data)
        """
        # get_dummies creates one hot encoded
        one_hot_encoded = pd.get_dummies(df, columns=["categories"])
        # Convert only the one-hot encoded columns to integers
        columns_to_convert = one_hot_encoded.columns.difference(["filename"])
        one_hot_encoded[columns_to_convert] = one_hot_encoded[columns_to_convert].astype(int)
        """
        output_file = "classes.csv"
        csv_path = os.path.join(self.output_path, output_file)
        df.to_csv(csv_path, index=False)

    def process(self):

        print("creating target folder")
        self.create_target_folder()
        print("converting data")
        data = self.convert_folders()
        print("converting classes csv")
        self.create_one_hot_encoded(data)






