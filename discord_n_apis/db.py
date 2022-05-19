# A Json based DB class which actively writes to filesystem
import json
import os


class DB:
    def __init__(self, path):
        self.path = path
        self.data = []
        self.load()
        self.lock = False

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump([], f)
                self.data = []
    def save(self):
        with open(self.path+'_backup', 'w') as f:
            json.dump(self.data, f)

        with open(self.path, 'w') as f:
            json.dump(self.data, f)
            
    def search(self, key, value):
        return list(filter(lambda x: x[key] == value if key in x else False, self.data))


