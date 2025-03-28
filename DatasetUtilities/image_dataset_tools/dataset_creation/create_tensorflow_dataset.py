import tensorflow as tf

class TensorflowDatasetFromDirectory:

    def __init__(self, input_dataset_path, output_dataset_path, image_size, batch_size = None):
        self.input = input_dataset_path
        self.output = output_dataset_path
        self.image_size = image_size
        self.batch_size = batch_size

    def create_dataset(self):
        dataset = tf.keras.utils.image_dataset_from_directory(
            self.input,
            image_size = (self.image_size, self.image_size),
            batch_size= self.batch_size
        )
        dataset.save(self.output)
