import logging
import pandas as pd
import numpy as np
import os
import shutil

#Třída, která slouží k dekompozici fotek z jedné složky do více složek podle tříd
class Decomposer:
#iniciallizace třídy, je zde definována cesta k datové sadě, kde se má vytvořit výstupní složka a zda je použito one hot kódování
    def __init__(self, dataset_path, output_directory, one_hot=False):
        self.dataset_path = dataset_path
        self.output_directory = output_directory
        self.one_hot = one_hot
        self.logger = logging.getLogger("Decomposer")
        self.dataframe = pd.DataFrame()

#metoda, která najde v souboru CSV s mapováním fotek a tříd
    def _find_csv_with_labels(self):
        for file in os.listdir(self.dataset_path):
            if file.endswith('.csv'):
                return os.path.join(self.dataset_path, file)
        return None

#metoda, která převede one hot kódování na jeden sloupec s názvem třídy
    def _one_hot_classes_csv_to_df(self):
        if self.dataframe.empty:
            self.logger.error("Failure to load csv dataframe")

        labels = self.dataframe.columns
        data_list = []
        for index, row in self.dataframe.iterrows():
            image_name = row[0]
            index_of_category = np.where(row[1:] == 1)[0][0]
            data_list.append({"filename": image_name, "class": labels[index_of_category + 1]})
        self.dataframe = pd.DataFrame(data_list)

#metoda, která vytvoří cílovou složku, pokud ještě neexistuje
    def _create_target_folder(self):
        os.makedirs(self.output_directory, exist_ok=True)


#metoda, která v cílové složce vytvoří složky pro jednotlivé třídy
    def _create_folders_for_categories(self):
        labels = self.dataframe["class"].unique()
        for label in labels:
            class_folder = os.path.join(self.output_directory, str(label))
            os.makedirs(class_folder, exist_ok=True)

#metoda, která slouží pro překopírování fotek podle mapování do nových složek
    def _copy_files(self):
        for _, item in self.dataframe.iterrows():
            filename = item['filename'].strip()
            category = item['class'].strip()
            source_path = os.path.join(self.dataset_path, filename)
            class_folder = os.path.join(self.output_directory, category)
            destination_path = os.path.join(class_folder, filename)

            if os.path.exists(source_path):
                try:
                    shutil.copy(source_path, destination_path)
                except Exception as e:
                    self.logger.error(f"could not copy image: {source_path} to file: {str(e)}")
            else:
                self.logger.warning(f"Warning: {filename} not found in {self.dataset_path}")

#metoda, která spouští celý proces
    def process(self):
        self._create_target_folder()
        csv_path = self._find_csv_with_labels()
        if csv_path:
            self.dataframe = pd.read_csv(csv_path)
        else:
            self.logger.error("No CSV file found.")
            return

        if self.one_hot:
            self.logger.info("One hot vectors converted")
            self._one_hot_classes_csv_to_df()

        self.logger.info("Creating category folders...")
        self._create_folders_for_categories()
        self.logger.info("Copying files into categorized folders...")
        self._copy_files()
