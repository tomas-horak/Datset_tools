import pandas as pd
import numpy as np
import os
import shutil


class Decomposer():
    df_with_image_names_and_labels = pd.DataFrame()

    def __init__(self, dataset_path, labels_csv_path, output_directory):
        self.dataset_path = dataset_path
        self.labels_csv_path = labels_csv_path
        self.output_directory = output_directory
        self.dataframe = pd.read_csv(self.labels_csv_path)


    def classes_csv_to_df(self):
        labels = self.dataframe.columns
        data_list = []
        print("skipped")

        #for index, row in self.dataframe.iterrows():

            #transposed = pd.DataFrame(row).transpose().to_numpy()
            #image_name = transposed[0][0]
            #print(image_name)
            #print(np.where(transposed[0] == 1))
            #index_of_category = np.where(transposed[0] == 1)[0][0]
            #data_list.append({"filename": image_name, "category": labels[index_of_category]})
        #self.df_with_image_names_and_labels = pd.DataFrame(data_list)

    def create_target_folder(self):
        os.makedirs(self.output_directory, exist_ok=True)

    def create_folders_for_categories(self):
        print(self.dataframe.columns)
        labels = self.dataframe["category"].unique()
        for label in labels:
            class_folder = os.path.join(self.output_directory, str(label))
            os.makedirs(class_folder, exist_ok=True)

    def copy_files(self):
        print("copying")
        for _, item in self.dataframe.iterrows():
            filename = item['filename'].strip()
            category = item['category']

            source_path = os.path.join(self.dataset_path, filename)
            class_folder = os.path.join(self.output_directory, str(category))
            destination_path = os.path.join(class_folder, filename)

            if os.path.exists(source_path):
                try:
                    shutil.copy(source_path, destination_path)
                except:
                    print(f"could not copy image: ${source_path} to file")
            else:
                print(f"Warning: {filename} not found in {self.dataset_path}")

    def process(self):
        print("Processing labels CSV...")
        self.classes_csv_to_df()
        print("Creating category folders...")
        self.create_folders_for_categories()
        print("Copying files into categorized folders...")
        self.copy_files()
        print("Decomposition complete.")

