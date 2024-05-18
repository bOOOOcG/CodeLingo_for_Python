import json
import os
from datetime import datetime

class SaveManager:
    def __init__(self, save_file='save_data.json'):
        self.save_file = save_file
        self.save_data = self.load_save_data()

    def load_save_data(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_progress(self, level, time_taken):
        self.save_data[level] = time_taken
        with open(self.save_file, 'w') as file:
            json.dump(self.save_data, file)

    def get_progress(self):
        return self.save_data
