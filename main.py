import sys
from LanguageModel import learn_language_model, prior_probability,tokenize
from ErrorModel import learn_error_model, likelihood
from SpellCorrect import predict
full = 1
print("Learning Language Model is started.")
learn_language_model('corpus.txt')
print("Learning Noisy Channel Model is started.")
if full:
    learn_error_model('spell-errors.txt')
file = open("prediction.txt",'w')
prediction_list = []
misspelled_file = sys.argv[1]
all_misspelled = tokenize(open(misspelled_file).read())
for word in all_misspelled:
    prediction = predict(word, 1)
    prediction_list.append(prediction)
    file.write(prediction)
    file.write("\n")
###############################################
###############################################
########## This part for testing the our corpus.
######## Make this variable false for ignore test
# TEST = FALSE
TEST = True
############
###########
##########
if TEST:
    correct_file = "test-words-correct.txt"
    all_correct = tokenize(open(correct_file).read())
    index = 0
    acc = 0
    valid_word_count = 0
    p_acc = 0
    print("Prediction is started.")
    print("----------------------")
    print("Words that are predicted differently between two models")
    print("----------------------")
    for prediction in prediction_list:
        p_prediction = predict(all_misspelled[index], 0)
        if prediction != p_prediction:
            print(prediction, p_prediction)
        if prediction is not "":
            valid_word_count += 1
        if prediction == all_correct[index]:
            acc += 1
        if p_prediction == all_correct[index]:
            p_acc += 1
        index += 1
    print("----------------------")
    print("--------Results-------")
    print("Language Model and Noisy Channel Model :", acc/valid_word_count)
    print("Only Language Model :", p_acc/valid_word_count)
    print("----------------------")
    file.close()