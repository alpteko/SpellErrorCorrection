import re
from collections import Counter

prior_probability_table = {}
####  Language Model #######
# This part is for creating a language model


def prior_probability(word):
    try:
        return prior_probability_table[word]
    except:
        return False


def learn_language_model(corpus_name):
    global prior_probability_table
    corpus = open(corpus_name).read()
    all_words = tokenize(corpus)
    dictionary = Counter(all_words)
    total_count = len(all_words) * 1.0
    for key in dictionary:
        dictionary[key] *= 10000
        dictionary[key] /= total_count
    prior_probability_table = dictionary


def tokenize(corpus):
    all_words = re.findall(r'\w+', corpus.lower())
    return all_words

