import os
import json
import time
import pickle


def load_json(path):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


def dump_json(path, data):
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def dump_pickle(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def make_path(f):
    d = os.path.dirname(f)
    if d and not os.path.exists(d):
        os.makedirs(d)
    return f


class ResultLogger(object):
    '''
    a class for logging the result
    '''
    def __init__(self, path, *args, **kwargs):
        if 'time' not in kwargs:
            kwargs['time'] = time.time()
        self.f_log = open(make_path(path), 'w', encoding="utf8")
        self.f_log.write(json.dumps(kwargs)+'\n')

    def log(self, **kwargs):
        if 'time' not in kwargs:
            kwargs['time'] = time.time()
        self.f_log.write(json.dumps(kwargs)+'\n')
        self.f_log.flush()

    def close(self):
        self.f_log.close()