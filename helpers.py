from collections import defaultdict
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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


def count_file_lines(file_path):
    return sum(1 for line in open(file_path))


def word_cloud(count_dict, file_name, is_emoji=False):
    font_path = None
    if is_emoji:
        font_path = "./Symbola.ttf"
    wordcloud = WordCloud(font_path=font_path, width=800, height=800,
                      background_color='white',
                      min_font_size=10).generate_from_frequencies(count_dict)


    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig('./data/output_wordclouds/' + file_name + ".png")
    plt.close()


def make_histogram(data_dict):
    plt.xticks(rotation=90)
    plt.bar(data_dict.keys(), data_dict.values(), color='g')
    plt.tight_layout()
    plt.savefig('./data/output_perc_histogram.png')
    plt.close()
