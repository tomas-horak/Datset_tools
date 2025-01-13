import tensorflow as tf

# Create a dataset from the folder structure
dataset = tf.keras.utils.image_dataset_from_directory(
    "/Users/tomashorak/PycharmProjects/ML_dataset_parser/flowers_full_decomposed",
    image_size = (224,224),
    batch_size= None
)

# Save the dataset
dataset.save("./td_dataset_224")

# Load and verify
loaded_dataset = tf.data.Dataset.load("./td_dataset_224")
for element in loaded_dataset:
    print(element)  # Print elements to verify
