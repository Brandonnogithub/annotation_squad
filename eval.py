import numpy as np
from collections import Counter
from utils.utils import load_json


def find_ann_num(data):
    count = 0
    for item in data:
        if "ann" in item and item["ann"]:
            count += 1

    return count


def get_token_list(doc_list, index_list):
    res = []
    for term in index_list:
        tmp = []
        for i in term:
            tmp.append(doc_list[i])
        res.append(tmp)
    return res


def get_single_f1_score(gt_words, pred_words):
    """ Given single grond truth answer position and predicted answer position, return f1 score of them

    Args:
        gt_chunk (tuple): ('ANS', 100, 104)
        pred_chunk (tuple): ('ANS', 102, 106)
        word_id (list of word ids of this document): [1,100,2,4,1,3,4,....]
        id2words (dictionary)

        gt_words (list): ['Shanghai', 'Jiao', 'Tong', 'University']
        pred_words (list): ['Jiao', 'Tong', 'University']

    Return:
        f1 score of gt_chunk and pred_chunk

    """
    common = Counter(gt_words) & Counter(pred_words)
    num_same = sum(common.values())

    num_gt_tokens = len(gt_words)
    num_pred_tokens = len(pred_words)

    precision = 1.0 * num_same / num_pred_tokens if num_pred_tokens > 0 else 0
    recall = 1.0 * num_same / num_gt_tokens if num_gt_tokens > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision > 0 and recall > 0 else 0

    return f1


def get_f1_matrix(gt_chunks, pred_chunks):
    num_gt = len(gt_chunks)
    num_pred = len(pred_chunks)

    f1_matrix = np.zeros(shape=(num_gt, num_pred))

    for j, gt_chunk in enumerate(gt_chunks):
        for i, pred_chunk in enumerate(pred_chunks):
            f1_matrix[j, i] = get_single_f1_score(gt_chunk, pred_chunk)

    return f1_matrix


def fuzzy_match(a, b):
    count = 0
    for i in a:
        for j in b:
            if i == j:
                count += 1
    th = 0.5
    if count / len(b) >= 0.5:
        return True
    else:
        return False 


def get_em(a, b):
    count = 0
    for i in a:
        for j in b:
            # if i == j:
            #     count += 1
            if fuzzy_match(i, j):
                count += 1
                break
    return count


def eval(path1, path2):
    data1 = load_json(path1)
    data2 = load_json(path2)

    count1 = find_ann_num(data1)
    count2 = find_ann_num(data2)
    count_all = min(count1, count2)

    data1 = data1[:count_all]
    data2 = data2[:count_all]

    count = 0
    f_all = 0

    c_e = 0
    c_g = 0
    c_p = 0
    for gt_data, pred_data in zip(data1, data2):
        assert gt_data["context_tokens"] == pred_data["context_tokens"]
        doc_list = gt_data["context_tokens"].split(" ")

        gt_ann = gt_data["ann"]
        pred_ann = pred_data["ann"]

        gt_tokens = get_token_list(doc_list, gt_ann)
        pred_tokens = get_token_list(doc_list, pred_ann)

        f1_matrix = get_f1_matrix(gt_tokens, pred_tokens)

        if len(pred_tokens) != 0:
            p = np.average(np.max(f1_matrix, axis=0))
            r = np.average(np.max(f1_matrix, axis=1))
            f = 2 * p * r / (p + r) if p > 0 and r > 0 else 0

            f_all += f
            count += 1

        c_e += get_em(gt_tokens, pred_tokens)
        c_g += len(gt_tokens)
        c_p += len(pred_tokens)

    print(c_e / c_g)
    print(c_e / c_p)

    print(f_all / count)


if __name__ == "__main__":
    path1 = "data/annotated/bran.json"
    path2 = "data/annotated/liuyunfei.json"
    eval(path1, path2)

