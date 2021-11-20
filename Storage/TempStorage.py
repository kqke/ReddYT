import os
from tempfile import TemporaryDirectory

import BaseStorage


class TempStorage(BaseStorage):
    def __init__(self):
        super().__init__("")
        self.temp_dir = TemporaryDirectory()

    def __del__(self):
        self.temp_dir.cleanup()

    def get_storage_type(self):
        return "TempStorage"

    def read(self, file_name):
        file_name = self.get_file_name(file_name)
        with open(file_name, 'rb') as file:
            return file.read()

    def write(self, data, file_name=None):
        file_name = self.get_file_name(file_name)
        with open(file_name, 'wb') as file:
            file.write(data)
        super().write(file_name)

    def delete(self, file_name):
        file_name = self.get_file_name(file_name)
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            raise FileNotFoundError("File not found")

    def update(self, data, file_name):
        self.write(data, file_name)

    def get_file_name(self, file_name=None):
        if not file_name:
            return self.temp_dir.name + "/" + str(self.counter)
        return self.temp_dir.name + "/" + file_name

    def get_file_list(self):
        return self.file_list
