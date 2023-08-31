from nltk.tokenize import word_tokenize

# get the document frequencies of word n-grams
def tokenDFs(dataset, hamSpam, nGrams):
    dfDict = {}

    for sms in dataset:
        # print(sms[1])
        # add a token to the dfDict if the sms from which it originated is the type desired
        if (sms[0] == hamSpam):
            words = word_tokenize(sms[1])
            countedTokens = set()

            for n in nGrams:
                for i in range(len(words) - n):
                    # let the token be the combination of several words tokenized from the original sms
                    token = " ".join(words[i: i + n])
                    # if it's already in the token set...
                    if token in dfDict:
                        # ...and the token hasn't been counted for this sms yet
                        if token not in countedTokens:
                            # increment the token counter
                            dfDict[token] += 1
                            # add it to the list of tokens to ignore
                            countedTokens.add(token)
                    else:
                        dfDict[token] = 1

    return dfDict

def pruneTokens(dict, minFreq):
    tokensToRemove = []

    for key in dict.keys():
        if (minFreq >= dict[key]):
            # add it to a list of tokens to prune
            tokensToRemove.append(key)

    for token in tokensToRemove:
        del dict[token]

    return dict