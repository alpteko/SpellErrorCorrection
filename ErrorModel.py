import re
from EditDistance import update_confusion_matrix
del_confusion_matrix = {}
ins_confusion_matrix = {}
trans_confusion_matrix = {}
sub_confusion_matrix = {}


def likelihood(correct,wrong):
    return 1


def learn_error_model(error_corpus):
    initialize_confusion_matrix()
    error_list = []
    with open(error_corpus) as f:
        for line in f:
            error_list.append(re.split(": |,",line.replace("\n",'')))
    error_dict = {}
    for values in error_list:
        key = values[0]
        key = key.strip().lower()
        if key.isalpha() is False:
            continue
        error_dict[key] = []
        for word in values[1:]:
            word = word.strip().lower()
            reg = re.compile("(.*)\*(\d+)")
            result = reg.match(word)
            if result is None:
                if word.isalpha() is False:
                    continue
                error_dict[key].append(word)
            else:
                if result.group(1).isalpha() is False:
                    continue
                for i in range(1,int(result.group(2))):
                    error_dict[key].append(result.group(1))
    for key, values in error_dict.items():
        for word in values:
            update_confusion_matrix(key, word)
    print(del_confusion_matrix['m']['n'])
    print(ins_confusion_matrix['m']['n'])
    print(trans_confusion_matrix['i']['e'])
    print(sub_confusion_matrix['i']['e'])


def initialize_confusion_matrix():
    global del_confusion_matrix
    global ins_confusion_matrix
    global trans_confusion_matrix
    global sub_confusion_matrix
    del_confusion_matrix = create_dict()
    ins_confusion_matrix = create_dict()
    trans_confusion_matrix = create_dict()
    sub_confusion_matrix = create_dict()


def create_dict():
    alphabet = list(map(chr, range(97, 123)))
    alphabet.append(' ')
    dictionary = {}
    for i in alphabet:
        dictionary[i] = {}
        for j in alphabet:
            dictionary[i][j] = 0
    return dictionary



