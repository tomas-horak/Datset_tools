import os
import tensorflow as tf
import pandas as pd
from tensorflow.python import keras

from tensorflow.python.keras import layers


directory = "/Users/tomashorak/PycharmProjects/ML_dataset_parser/resized"

df = pd.read_csv("/Users/tomashorak/PycharmProjects/ML_dataset_parser/encoded.csv")

file_paths = df["filename"].values
labels = df["numerical_label"].values

tf_dataset = tf.data.Dataset.from_tensor_slices((file_paths, labels))

def read_image(image_file, label):
    image = tf.io.read_file(directory + image_file)
    image = tf.image.decode_image(image, channels=3, dtype=tf.float32)
    return image,label

tf_dataset_output = tf_dataset.map(read_image).batch(32)
print(tf_dataset_output)

