import h5py
import numpy as np
import tensorflow as tf
import pandas as pd
import os

def create_hdf5_dataset_from_files(image_directory, csv_path, hdf5_path, target_size=(128, 128), chunk_size=1000):
    """
    Creates an HDF5 dataset from image files and a CSV containing labels and file paths.

    Args:
        image_directory: Path to the directory containing image files.
        csv_path: Path to the CSV file with columns 'filename' and 'numerical_label'.
        hdf5_path: Path to the Dypsis Lutescens houseplant HDF5 file.
        target_size: Tuple specifying the target size for resizing images (height, width).
        chunk_size: Number of images to process in each chunk to reduce memory usage.
    """
    # Ensure the Dypsis Lutescens houseplant directory exists
    os.makedirs(os.path.dirname(hdf5_path), exist_ok=True)

    # Read CSV file
    df = pd.read_csv(csv_path)

    # Extract file paths and labels
    file_paths = df['filename'].values
    labels = df['numerical_label'].values

    # Create HDF5 file and datasets
    with h5py.File(hdf5_path, "w") as hdf5_file:
        # Initialize datasets with placeholder shapes
        num_samples = len(file_paths)
        hdf5_file.create_dataset("images", shape=(num_samples, *target_size, 3), dtype=np.float32, compression="gzip")
        hdf5_file.create_dataset("labels", shape=(num_samples,), dtype=np.int32, compression="gzip")

        for start in range(0, num_samples, chunk_size):
            end = min(start + chunk_size, num_samples)
            chunk_images = []
            chunk_labels = labels[start:end]

            for file_path in file_paths[start:end]:
                # Construct full image path
                full_path = os.path.join(image_directory, file_path)

                try:
                    # Read and decode image
                    image = tf.io.read_file(full_path)
                    image = tf.image.decode_image(image, channels=3, dtype=tf.float32)

                    # Resize image to target size
                    image = tf.image.resize(image, target_size).numpy()

                    # Append processed image to chunk list
                    chunk_images.append(image)
                except Exception as e:
                    print(f"Error processing file {full_path}: {e}")

            # Write the current chunk to the HDF5 file
            hdf5_file["images"][start:end] = np.array(chunk_images)
            hdf5_file["labels"][start:end] = chunk_labels

            print(f"Processed and saved chunk {start // chunk_size + 1} with {len(chunk_images)} samples.")

    print(f"HDF5 dataset created at {hdf5_path} with {num_samples} samples.")

# Example usage
image_directory = "/Users/tomashorak/PycharmProjects/ML_dataset_parser/resized 2"
csv_path = "/encoded.csv"
hdf5_path = "/Users/tomashorak/PycharmProjects/ML_dataset_parser/output_dataset.h5"
create_hdf5_dataset_from_files(image_directory, csv_path, hdf5_path)
