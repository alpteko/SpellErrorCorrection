#######################
### Spell Correction #####
The program has 4 modules.
1-) LanguageModel for learning language Model.
2-) ErrorMode for learning Noisy Channel Model.
3-) EditDistance for finding the edits for learning
Error Models and back-tracing for confusion matrix.
4-) main for running learning and generating the prediction.
To run the program you need python3 without extrapackage.
python3 main.py <spelling-error-txt-file>
it will produce the result in prediction.txt
the name of the traning corpus must be corpus.txt
the name of the error traning set must be spell-errors.txt
if you do not have test, please assign TEST variable in main.py
False to run the code for only predcition.(TEST = FALSE )

