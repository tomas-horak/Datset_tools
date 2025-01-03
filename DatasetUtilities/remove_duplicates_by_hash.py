
import os
import shutil
from PIL import Image
import imagehash


class RemoveDuplicates:
    def __init__(self, folder1, folder2):
        self.folder1 = folder1
        self.folder2 = folder2
        self.first_file_hashes = []
        self.second_file_hashes = []
        self.first_file = sorted(os.listdir(folder1))
        self.second_file = sorted(os.listdir(folder2))

    def get_image_hash(self, image_path):
        img = Image.open(image_path)
        return imagehash.average_hash(img)

    def calculate_hashes(self):
        for item1 in self.first_file:
            hash_value = self.get_image_hash(os.path.join(self.folder1, item1))
            self.first_file_hashes.append(hash_value)

        for item2 in self.second_file:
            hash_value = self.get_image_hash(os.path.join(self.folder2, item2))
            self.second_file_hashes.append(hash_value)

    def deduplicate(self):
        os.makedirs("output", exist_ok=True)

        for index, second_hash in enumerate(self.second_file_hashes):

            if second_hash not in self.first_file_hashes:
                print(index, second_hash)
                src_path = os.path.join(self.folder2, self.second_file[index])
                shutil.copy(src_path, "./output")

    def process(self):
        self.calculate_hashes()
        self.deduplicate()


# Example usage
folder1 = './chlorophytum-comosum'
folder2 = './Chlorophytum comosum'

deduplicator = RemoveDuplicates(folder1, folder2)
deduplicator.run()

