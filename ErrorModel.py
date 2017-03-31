import re
from EditDistance import update_confusion_matrix
del_confusion_matrix = {}
ins_confusion_matrix = {}
trans_confusion_matrix = {}
sub_confusion_matrix = {}


def likelihood(correct, wrong, c):
    if c == 0:
        return 1
    elif c == 1:
        return del_confusion_matrix[correct][wrong]
    elif c == 2:
        return ins_confusion_matrix[correct][wrong]
    elif c == 3:
        return trans_confusion_matrix[correct][wrong]
    elif c == 4:
        return sub_confusion_matrix[correct][wrong]
    else:
        print("Unexpected Class")


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
    #convert_confusion_to_likelihood("corpus.txt",error_corpus)
    print("Likelihood Matrix is generated.")



def convert_confusion_to_likelihood(corpus_name, error_file):
    global del_confusion_matrix
    global ins_confusion_matrix
    global trans_confusion_matrix
    global sub_confusion_matrix
    corpus = open(corpus_name).read()
    error = open(error_file).read()
    for key, entry in del_confusion_matrix.items():
        for inner_key in entry.keys():
            if inner_key == ' ':
                continue
            if key == ' ':
                count = len(re.findall(' '+inner_key, corpus)) + len(re.findall(' '+inner_key, error))
            else:
                count = len(re.findall(key+inner_key, corpus)) + len(re.findall(key+inner_key, error))
            del_confusion_matrix[key][inner_key] = (del_confusion_matrix[key][inner_key]+1)*10000;
            del_confusion_matrix[key][inner_key] /= (count*1.0 + 26.0);
    for key, entry in ins_confusion_matrix.items():
        for inner_key in entry.keys():
            if inner_key == ' ':
                continue
            if key == ' ':
                count = len(re.findall("\w+.", corpus)) + len(re.findall("\w+.", error))
            else:
                count = len(re.findall(key, corpus)) + len(re.findall(key, error))
            ins_confusion_matrix[key][inner_key] = (ins_confusion_matrix[key][inner_key] +1)*10000;
            ins_confusion_matrix[key][inner_key] /= (count*1.0 + 26.0);
    for key, entry in sub_confusion_matrix.items():
        for inner_key in entry.keys():
            if inner_key == ' ':
                continue
            count = len(re.findall(inner_key, corpus)) + len(re.findall(inner_key, error))
            sub_confusion_matrix[key][inner_key] = (sub_confusion_matrix[key][inner_key] +1)*10000;
            sub_confusion_matrix[key][inner_key] /= (count*1.0 + 26.0);
    for key, entry in trans_confusion_matrix.items():
        for inner_key in entry.keys():
            if inner_key == ' ' or key == ' ':
                continue
            count = len(re.findall(key+inner_key, corpus)) + len(re.findall(key+inner_key, error))
            trans_confusion_matrix[key][inner_key] = (trans_confusion_matrix[key][inner_key] +1)*10000;
            trans_confusion_matrix[key][inner_key] /= (count*1.0 + 26.0);


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



