from DatasetTools.dataset_distribution_tool import show_distribution_from_csv
from DatasetTools.decomposer import Decomposer
from DatasetTools.folders_to_dataset import ImageFoldersToDataset


class DatasetTools:

    @staticmethod
    def decompose_dataset(dataset_path, csv_path, output_dir):
        """
        This utility is used for converting a single file with images and corresponding mapping in csv to a corresponding
        folder structure with images

        :param dataset_path: folder where dataset is saved
        :param csv_path: path to csv file with labels and ids
        :param output_dir: path to where files with images should be created
        :return:
        """

        decomposer = Decomposer(dataset_path=dataset_path, labels_csv_path=csv_path, output_directory=output_dir)
        decomposer.process()

    @staticmethod
    def create_dataset_from_folders(folders_directory, output_path):
        dataset_creator = ImageFoldersToDataset(path_to_folder_with_folders= folders_directory, output_path= output_path)
        dataset_creator.process()

    @staticmethod
    def show_distribution_from_csv(csv_path):
        show_distribution_from_csv(csv_path)



