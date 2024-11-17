import pandas as pd
import matplotlib.pyplot as plt

from decoder import OneHotShotDecoder
from file_handler import FileHandler

input_folder = './Plant Detection/train'
input_csv = input_folder + '/_classes.csv'
output_folder = './output_plant_detection_train'


def generate_folders():
    df = pd.read_csv(input_csv, )
    print(df.shape)
    decoder = OneHotShotDecoder()
    decoded_dataframe = decoder.decode(df)
    print(decoded_dataframe.shape)

    file_handler = FileHandler(input_folder, output_folder, decoded_dataframe)
    file_handler.create_target_folder()
    file_handler.create_folders_for_classes()
    file_handler.copy_files()


generate_folders()
def show_distribution():
    df = pd.read_csv(input_csv, )
    class_sums = df.iloc[:, 1:].sum()
    print(class_sums)
    plt.figure(figsize=(12, 6))
    class_sums.plot(kind='bar')
    plt.title("Class Distribution of Botanic buddy Dataset")
    plt.xlabel("Class", fontsize=12)
    plt.ylabel("Number of Samples")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

show_distribution()