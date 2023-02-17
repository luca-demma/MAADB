from collections import defaultdict


def multi_dict(K, type):
    if K == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(K-1, type))


# returns the text file as a string
def read_file(file_path):
    with open(file_path) as f:
        return f.readlines()
