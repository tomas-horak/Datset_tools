import logging
import os

from pathlib import Path

from DatasetUtilities.image_dataset_tools.dataset_creation.convert_images_to_jpg import \
    NormaliseFileTypeAndNameInDataset
from DatasetUtilities.image_dataset_tools.dataset_creation.create_tensorflow_dataset import \
    TensorflowDatasetFromDirectory
from DatasetUtilities.image_dataset_tools.dataset_creation.folders_to_dataset import ImageFoldersToDataset
from DatasetUtilities.image_dataset_tools.dataset_creation.resizer import ImageResizer
from DatasetUtilities.image_dataset_tools.dataset_split.dataset_split_absolute import ImagesFromFolderDatasetAbsolute
from DatasetUtilities.image_dataset_tools.dataset_split.dataset_split_relative import ImagesFromFolderDataset
from DatasetUtilities.image_dataset_tools.dataset_decomposition.decomposer import Decomposer
from DatasetUtilities.image_dataset_tools.dataset_distribution_tool import show_distribution_from_csv


class DatasetTools:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def decompose_dataset(path_to_dataset, output_dir, one_hot = False):
        """
        This utility is used for converting a single file with images and corresponding mapping in csv to a corresponding
        folder structure with images

        :param path_to_dataset: folder where dataset is saved
        :param path_to_csv: path to csv file with labels and ids
        :param csv_column_names: tuple, containing names of columns in csv file. First value corresponds to names
        of images, second value corresponds to name of column with target classes. eg: (filename, class)
        :param output_dir: path to where files with images should be created, if it does not exist, it will be created
        :param one_hot: If True, the CSV is expected to be one-hot encoded

        :return:
        """

        if not os.path.exists(path_to_dataset):
            raise ValueError(f"Input directory {path_to_dataset} does not exist.")

        try:
            decomposer = Decomposer(path_to_dataset, output_dir, one_hot=one_hot)
            decomposer.process()
            DatasetTools.logger.info("Decomposition completed.")
        except Exception as e:
            DatasetTools.logger.error(f"Error decomposing dataset: {e}")

    @staticmethod
    def create_dataset_from_folders(path_to_directory, output_path, dataset_type):
        """
        This utility is used for creating dataset from directory of folders.

        :param path_to_directory: path to folder with folders corresponding to classes
        :param output_path: directory, where dataset should be created
        :param dataset_type:
        """
        if not os.path.exists(path_to_directory):
            raise ValueError(f"Input directory {path_to_directory} does not exist.")

        dataset_creator = ImageFoldersToDataset(path_to_folder_with_folders= path_to_directory, output_path= output_path, dataset_type=dataset_type)
        dataset_creator.process()

    @staticmethod
    def show_distribution_from_csv(csv_path):
        show_distribution_from_csv(csv_path)

    @staticmethod
    def resize_images(input_directory, output_directory, dimension, dataset_type):
        resizer = ImageResizer(input_directory, output_directory, dimension, dataset_type)
        resizer.process()

    @staticmethod
    def labels_to_numbers(csv_file_path, output_file, output_docs):

        import pandas as pd
        df = pd.read_csv(csv_file_path, delimiter=';')
        print(df.columns)

        categories = sorted(df['categories'].unique())

        category_to_number = {category: index for index, category in enumerate(categories)}

        # Convert categories to numerical labels
        df['numerical_label'] = df['categories'].map(category_to_number)
        df_output = df[['filename', 'numerical_label']]

        # Save the Dypsis Lutescens houseplant CSV with the new numerical labels
        df_output.to_csv(output_file, index=False)

        # Prepare the explanation of the label mapping
        explanation = "\n".join(
            [f"Label {index} = class {category}" for category, index in category_to_number.items()])

        # Save the explanation to the Dypsis Lutescens houseplant document
        with open(output_docs, 'w') as doc_file:
            doc_file.write(explanation)

    @staticmethod
    def split_dataset_relative(input_folder_path, output_test_path, output_train_path=None, data_split=0.2):
        extractor = ImagesFromFolderDataset(input_folder_path, output_test_path, output_train_path, data_split)
        extractor.process()

    @staticmethod
    def split_dataset_absolute(input_folder_path, output_test_path, output_train_path=None, num_val = 100, num_test = 50):
        extractor = ImagesFromFolderDatasetAbsolute(input_folder_path, output_test_path, output_train_path, num_val, num_test)
        extractor.process()

    @staticmethod
    def create_tensorflow_dataset(input_folder_path, output_path, image_size, batch_size):
        dataset_creator = TensorflowDatasetFromDirectory(input_folder_path, output_path, image_size, batch_size)
        dataset_creator.create_dataset()

    @staticmethod
    def create_hdf5_dataset(tf_dataset, hdf5_path):
        print("TODO")

    @staticmethod
    def normalise_images(path_to_dataset, output_path):
        convertor = NormaliseFileTypeAndNameInDataset(path_to_dataset, output_path)
        convertor.process()













