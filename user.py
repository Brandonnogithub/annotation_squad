import os
from config import config
from utils.utils import load_json, dump_json, make_path


class User(object):
    def __init__(self, name=None):
        self.name = name

    def load_data(self):
        self.data_path = "data/annotated/" + self.name + ".json"
        make_path(self.data_path)

        if os.path.exists(self.data_path):
            self.ann_data = load_json(self.data_path)
        else:
            self.ann_data = []
        self.raw_data = load_json(config.processed_path)

        self.total_num = len(self.raw_data)
        self.annotated_num = len(self.ann_data)