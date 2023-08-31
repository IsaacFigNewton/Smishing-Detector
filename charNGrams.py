import customNLP as nlp

# create a dictionary of character n-gram tokens that appear in the dataset and the number of docs that contain them
def tokenDFs(dataset, hamSpam, nGrams = None):
    dfDict = {}

    for sms in dataset:
        # print(sms[1])
        # add a token to the dfDict if the sms from which it originated is the type desired
        if (sms[0] == hamSpam):
            countedTokens = set()

            # if you don't want to create maximal char n-grams and just want to create char n-grams of specific n's
            if not nGrams is None:
                for n in nGrams:
                    for start in range(len(sms[1]) - n):
                        # let the token be the combination of several words tokenized from the original sms
                        token = sms[1][start: start + n]
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
            else:
                # for some combined offset...
                for offset in range(len(sms[1])):
                    # ...loop through all possible maximal strings of the text up to the offset
                    for start in range(offset + 1):
                        token = sms[1][start: len(sms[1]) - offset + start]

                        # if it's already in the token set...
                        if len(token) < nlp.maxTokenLeng and token in dfDict:
                            # ...and the token hasn't been counted for this sms yet
                            if token not in countedTokens:
                                # ...and it's a maximal token string
                                if len(nlp.tokenize(token, dfDict)) == 1:
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
        if (minFreq >= dict[key] or (len(key) >= nlp.maxLen and " " not in key)):
            # add it to a list of tokens to prune
            tokensToRemove.append(key)

    for token in tokensToRemove:
        del dict[token]

    return dict