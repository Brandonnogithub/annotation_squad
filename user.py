import os
from config import config
from utils.utils import load_json, dump_json, make_path


def trans_array(array):
    '''
    array: [0, 1,1, 0 ,3,3,...]
    '''
    print(array)
    res = []
    tmp_res = []
    for index, i in enumerate(array):
        if i != 0:
            if tmp_res:
                if i == array[tmp_res[0]]:
                    tmp_res.append(index)
                else:
                    res.append(tmp_res)
                    tmp_res = [index]
            else:
                tmp_res.append(index)
        else:
            if tmp_res:
                res.append(tmp_res)
                tmp_res = []
    return res


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
        self.position = self.annotated_num  # the page showing

    def next(self):
        '''
        get current data
        '''
        return self.raw_data[self.position] if self.position >= self.annotated_num else self.ann_data[self.position]

    def get_curr_docID(self):
        return self.position + 1

    def get_data(self, page_id):
        page_id -= 1
        if page_id < 0 or page_id >= self.total_num:
            raise ValueError("Page index out of range!")

        self.position = page_id
        if page_id >= self.annotated_num:
            return self.raw_data[page_id]
        else:
            return self.ann_data[page_id]

    # def last(self):
    #     self.position -= 1
    #     return self.ann_data[self.position]

    def update_ann(self, array):
        new_array = trans_array(array)
        data = self.raw_data[self.position]
        data["ann"] = new_array

        if self.position >= self.annotated_num:
            self.ann_data.append(data)
            self.annotated_num += 1
        else:
            self.ann_data[self.position] = data

    def save(self):
        dump_json(self.data_path, self.ann_data)

        
        
        