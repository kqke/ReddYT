class BaseStorage:

    def __init__(self, prefix):
        self.prefix = prefix
        self.file_list = []
        self.counter = 0

    def read(self, file_name):
        raise NotImplementedError("Subclass must implement abstract method")

    def write(self, data, file_name):
        self.file_list.append(file_name)
        self.counter += 1

    def delete(self, file_name):
        raise NotImplementedError("Subclass must implement abstract method")

    def update(self, data, file_name):
        raise NotImplementedError("Subclass must implement abstract method")

