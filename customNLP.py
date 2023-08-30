import math

maxSussiness = 5.5
antiSusScale = 0.8
maxLen = 10
maxTokenLeng = 20
minThreshold = 1

def inRanges(tuple, ranges):
    # if len(ranges) > 0:
    #     print(ranges)

    for range in ranges:
        # if the start or end falls within the range
        if (range[0] <= tuple[0] and tuple[0] < range[1] or range[0] <= tuple[1] and tuple[1] < range[1]):
            return True

    return False

# decompose text into a minimal set of tokens from tokens dictionary
def tokenize(text, tokens):
    # print("tokenizing sms...")
    # tokens to return
    tokenSet = set()
    # ranges to exclude from token consideration
    excludeRanges = []

    # for some combined offset
    offset = 0
    while offset < len(text):

        # loop through all possible maximal strings of the text up to the offset
        start = 0
        while start < offset + 1:
            end = len(text) - offset + start

            # if the token is not in a range of chars to be excluded from consideration
            if not inRanges((start, end), excludeRanges):
                token = text[start: end]
                # check if it's a valid token
                if token in tokens:
                    tokenSet.add(token)
                    # if the token is in the token dict,
                    # remove it from the text to consider by inserting it into a sorted list of ranges to exclude
                    i = 0
                    # print(len(excludeRanges))
                    if len(excludeRanges) > 0:
                        while excludeRanges[i][0] < start and i < len(excludeRanges) - 1:
                            i += 1
                            # print(i)
                            # print(excludeRanges[i][0] < start and i < len(excludeRanges))
                        # handle off-by-one bug
                        if (i == len(excludeRanges) - 1):
                            excludeRanges.append((start, end))
                        else:
                            excludeRanges.insert(i, (start, end))
                    else:
                        excludeRanges.append((start, end))

            start += 1
        offset += 1

    return tokenSet

# create a dictionary of tokens that appear in the dataset and the number of docs that contain them
def getDFDict(dataset, hamSpam):
    dfDict = {}

    for sms in dataset:
        # print(sms[1])
        # add a token to the idfDict if the sms from which it originated is the type desired
        if (sms[0] == hamSpam):
            countedTokens = set()

            # for some combined offset...
            for offset in range(len(sms[1])):
                # ...loop through all possible maximal strings of the text up to the offset
                for start in range(offset + 1):
                    token = sms[1][start: len(sms[1]) - offset + start]

                    # if it's already in the token set...
                    if len(token) < maxTokenLeng and token in dfDict:
                        # ...and the token hasn't been counted for this sms yet
                        if token not in countedTokens:
                            # ...and it's a maximal token string
                            if len(tokenize(token, dfDict)) == 1:
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
        if (minFreq >= dict[key] or (len(key) >= maxLen and " " not in key)):
            # add it to a list of tokens to prune
            tokensToRemove.append(key)

    for token in tokensToRemove:
        del dict[token]

    return dict


def sigmoid(freq):
    try:
        return 1 / (1.0 + math.exp(-freq))
    except OverflowError:
        return 0


# combine the set of tokens commonly found in spam with the set of tokens commonly found in ham destructively
def getTokenSet(dataset, minSusFreq, minAntiSusFreq):
    tokensToRemove = []

    print("\tcreating sus token set...")
    susDict = getDFDict(dataset, True)
    print("\tpruning sus token set...")
    susDict = pruneTokens(susDict, minSusFreq)
    print("\tcreating antisus token set...")
    antiSusDict = getDFDict(dataset, False)
    print("\tpruning antisus token set...")
    antiSusDict = pruneTokens(antiSusDict, minAntiSusFreq)


    print("\tcombining token sets...")
    # combine the sus and antisus frequencies destructively and then put them on a stretched sigmoid about 0
    for sus in susDict.keys():
        if sus in antiSusDict:
            susDict[sus] = 2 * sigmoid(susDict[sus] - antiSusDict[sus]) - 1

        else:
            susDict[sus] = maxSussiness

    for antiSus in antiSusDict.keys():
        if antiSus not in susDict:
            susDict[antiSus] = -antiSusScale * math.log(antiSusDict[antiSus])

    # trim the fat off the token list
    for sus in susDict.keys():
        # if it's below the threshold, it probably won't affect the outcome much
        if abs(susDict[sus]) < minThreshold:
            tokensToRemove.append(sus)

    for token in tokensToRemove:
        if token in susDict:
            del susDict[token]

    return susDict