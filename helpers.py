from collections import defaultdict
import json

import constants


def multi_dict(K, type):
    if K == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(K-1, type))


# returns the text file as a string
def read_file(file_path):
    with open(file_path) as f:
        return f.readlines()


def read_slang_json():
    f = open(constants.DATA_PATH + 'slang.txt')
    data = json.load(f)
    f.close()
    return data


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

