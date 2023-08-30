import nltk
from nltk import tokenize

"""
Tkinter/ML approach:
    1 Extract token set from training data
    2 Tokenize each sms in training data using the new tokenSet
    3 Plug tokens' frequencies into different ML approaches as features
    4 Determine best ML approach?
"""

# # extract tokens from the training data
# def getTokenSet(dataset):
#     tokenSet = set()
#     corpus = ""
#     # combine all the sms's into one corpus to be tokenized, with each sms separated by a new line
#     for sms in dataset:
#         corpus += "\n" + sms[1]
#
#     # tokenize the dataset into a set of tokens
#     tokens = tokenize.word_tokenize(dataset)
#     for token in tokens:
#         tokenSet.add(token)
#
#     return tokenSet

def tokenize(sms, tokenSet):
    return tokenize.word_tokenize(sms)
