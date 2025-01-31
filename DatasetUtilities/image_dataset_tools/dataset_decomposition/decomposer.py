import pandas as pd
import numpy as np
import os
import shutil

from keras.src.legacy.preprocessing.text import one_hot


class Decomposer:
    df_with_image_names_and_labels = pd.DataFrame()

    def __init__(self, dataset_path, labels_csv_path, output_directory, csv_names, one_hot, logger):
        self.dataset_path = dataset_path
        self.labels_csv_path = labels_csv_path
        self.output_directory = output_directory
        self.dataframe = pd.read_csv(self.labels_csv_path)
        self.filename_column, self.classes_column = csv_names
        self.one_hot = one_hot
        self.logger = logger

    def classes_csv_to_df(self):
        labels = self.dataframe.columns
        data_list = []
        for index, row in self.dataframe.iterrows():
            transposed = pd.DataFrame(row).transpose().to_numpy()
            image_name = transposed[0][0]
            index_of_category = np.where(transposed[0] == 1)[0][0]
            data_list.append({self.filename_column: image_name, self.classes_column: labels[index_of_category]})
        self.df_with_image_names_and_labels = pd.DataFrame(data_list)

    def create_target_folder(self):
        os.makedirs(self.output_directory, exist_ok=True)

    def create_folders_for_categories(self):
        def create_folders_from_list(labels):
            for label in labels:
                class_folder = os.path.join(self.output_directory, str(label))
                os.makedirs(class_folder, exist_ok=True)

        if self.one_hot:
            labels = self.df_with_image_names_and_labels[self.classes_column].unique()
            create_folders_from_list(labels)

        else:
            category_column = self.classes_column
            labels = self.dataframe[category_column].unique()
            create_folders_from_list(labels)


    def copy_files(self):

        if one_hot:
            df = self.df_with_image_names_and_labels
        else:
            df = self.dataframe

        for _, item in df:
            filename = self.filename_column
            classes = self.classes_column


            filename = item[filename].strip()
            category = item[classes]

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
        self.create_target_folder()
        if self.one_hot:
            self.logger.info("One hot vectors converted")
            self.classes_csv_to_df()

        self.logger.info("Creating category folders...")
        self.create_folders_for_categories()
        print("Copying files into categorized folders...")
        self.logger.info("Copying files into categorized folders...")
        self.copy_files()

