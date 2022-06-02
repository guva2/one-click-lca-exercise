import os

class FileWriter:
    #TODO: move output directory to config
    def __init__(self, root_dir='./out'):
        self.root_dir = root_dir

    def write_all(self, files):
        for file in files:
            self.write(file)

    def write(self, file):
        file_path = '/'.join([self.root_dir, file.dir_path, file.name])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(file.content)
