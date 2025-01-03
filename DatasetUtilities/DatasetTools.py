from DatasetUtilities.tools_utils.dataset_distribution_tool import show_distribution_from_csv
from DatasetUtilities.tools_utils.decomposer import Decomposer
from DatasetUtilities.tools_utils.folders_to_dataset import ImageFoldersToDataset
from DatasetUtilities.tools_utils.resizer import ImageResizer


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

    @staticmethod
    def remove_duplicates_in_folder_by_hash():
        print("todo")

    @staticmethod
    def resize_images(input_directory, output_directory, dimension):
        resizer = ImageResizer(input_directory, output_directory, dimension)
        resizer.process_directory()

    @staticmethod
    def labels_to_numbers(csv_file_path, output_file, output_docs):
        import pandas as pd
        # Read the CSV file
        df = pd.read_csv(csv_file_path, delimiter=';')
        print(df.columns)

        categories = sorted(df['categories'].unique())

        # Map categories to numbers
        category_to_number = {category: index for index, category in enumerate(categories)}

        # Convert categories to numerical labels
        df['numerical_label'] = df['categories'].map(category_to_number)
        df_output = df[['filename', 'numerical_label']]

        # Save the output CSV with the new numerical labels
        df_output.to_csv(output_file, index=False)

        # Prepare the explanation of the label mapping
        explanation = "\n".join(
            [f"Label {index} = class {category}" for category, index in category_to_number.items()])

        # Save the explanation to the output document
        with open(output_docs, 'w') as doc_file:
            doc_file.write(explanation)

        print("Conversion completed successfully!")







