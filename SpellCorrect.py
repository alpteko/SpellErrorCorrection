from ErrorModel import likelihood
from LanguageModel import prior_probability, check_word


def predict(word, f):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    candidates = {}
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    ### If insertion mistake is occured.
    for L, R in splits:
        if R:
            cand_word = L + R[1:]
            if check_word(cand_word):
                if len(L) is 0:
                    candidates[cand_word] = likelihood(' ', R[0], 2*f) * prior_probability(cand_word)
                else:
                    candidates[cand_word] = likelihood(L[-1], R[0], 2*f) * prior_probability(cand_word)
            else:
                continue
        else:
            continue
    ### If Deletion error is occurred.
    for L, R in splits:
        for c in letters:
            cand_word = L + c + R
            if check_word(cand_word):
                if len(L) is 0:
                    candidates[cand_word] = likelihood(' ', c, 1 * f) * prior_probability(cand_word)
                else:
                    candidates[cand_word] = likelihood(L[-1], c, 1 * f) * prior_probability(cand_word)
            else:
                continue
    ### For Substitution error
    for L, R in splits:
        for c in letters:
            if R:
                cand_word = L + c + R[1:]
                if check_word(cand_word):
                        candidates[cand_word] = likelihood(R[0], c, 3 * f) * prior_probability(cand_word)
                else:
                    continue
            else:
                continue
    ### For transposition error.
    for L, R in splits:
        if len(R) > 1:
            cand_word = L + R[1] + R[0] + R[2:]
            if check_word(cand_word):
                    candidates[cand_word] = likelihood(R[1], R[0], 4 * f) * prior_probability(cand_word)
            else:
                continue
        else:
            continue
    try:
        return max(candidates, key=candidates.get)
    except:
        return ""
