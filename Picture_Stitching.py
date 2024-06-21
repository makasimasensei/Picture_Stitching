import os
import re

from PIL import Image
from tqdm import tqdm


class Picture_Stitching:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.h_offset = 0
        self.max_width, self.max_height = 0, 0
        self.doc = os.listdir(folder_path)

    def __call__(self, *args, **kwargs):
        for filename in self.doc:
            image = Image.open(os.path.join(self.folder_path, filename))
            local_width, local_height = image.size
            self.max_width = max(self.max_width, local_width)
            self.max_height += local_height

        new_image = Image.new("RGB", (self.max_width, self.max_height))

        numbers = re.findall(r'\d+', self.folder_path)
        print('开始合成第{}章'.format(numbers[0]))
        bar = tqdm(total=len(os.listdir(self.folder_path)))
        for filename in self.doc:
            image = Image.open(os.path.join(self.folder_path, filename))
            _, local_height = image.size
            new_image.paste(image, (0, self.h_offset))
            self.h_offset += local_height
            bar.update(1)
        bar.close()

        new_image.save("Chapter{}.png".format(numbers[0]))


if __name__ == '__main__':
    contents = os.listdir('./')
    folders = [content for content in contents if content[:3] == 'doc']
    pictures = [content for content in contents if content[-3:] == 'png']

    folders_numbers, pictures_numbers = [], []

    for folder in folders:
        folders_numbers.append(re.findall(r'\d+', folder)[0])
    for picture in pictures:
        pictures_numbers.append(re.findall(r'\d+', picture)[0])

    not_in_pictures_numbers = [number for number in folders_numbers if number not in pictures_numbers]

    for i in not_in_pictures_numbers:
        folder = 'doc' + i
        pc = Picture_Stitching(os.path.join('./', folder))
        pc()
