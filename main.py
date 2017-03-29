from LanguageModel import learn_language_model, prior_probability
from ErrorModel import learn_error_model, likelihood
learn_language_model('corpus.txt')
learn_error_model('spell-errors.txt')

