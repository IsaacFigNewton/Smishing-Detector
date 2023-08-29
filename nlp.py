import math


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

# create a dictionary of words that appear in the dataset and the number of docs that contain them
def getDFDict(dataset, hamSpam):
    dfDict = {}

    for sms in dataset:
        # print(sms[1])
        # add a word to the idfDict if the sms from which it originated is the type desired
        if (sms[0] == hamSpam):
            countedWords = set()

            # check if tokens in set, starting with largest tokens
            # check if every possible word in the text is in the idfDict, and if it isn't put it there
            # for end in range(len(sms[1])):
            #     for start in range(end):
            #         token = sms[1][start:end + 1]
            #         if token in dfDict:
            #             if token not in countedWords:
            #                 dfDict[token] += 1
            #                 countedWords.add(token)
            #         else:
            #             dfDict[token] = 1

            # for some combined offset
            for offset in range(len(sms[1])):
                # loop through all possible maximal strings of the text up to the offset
                for start in range(offset + 1):
                    token = sms[1][start: len(sms[1]) - offset + start]

                    # if it's already in the token set...
                    if len(token) < 20 and token in dfDict:
                        # ...and the token hasn't been counted for this sms yet
                        if token not in countedWords:
                            # ...and it's a maximal token string
                            if len(tokenize(token, dfDict)) == 1:
                                # increment the token counter
                                dfDict[token] += 1
                            # add it to the list of tokens to ignore
                            countedWords.add(token)
                    else:
                        dfDict[token] = 1

    return dfDict


def pruneWords(dict, minFreq, maxLen):
    wordsToRemove = []

    for key in dict.keys():
        if (minFreq >= dict[key] or (len(key) >= maxLen and " " not in key)):
            # add it to a list of words to prune
            wordsToRemove.append(key)

    for word in wordsToRemove:
        del dict[word]

    return dict


# # IDF = log((total # of sms's)/(# sms's containing the word))
# # do log on the word/sms occurrences to get the IDF for each word
# def weightedIDF(frequency):
#     return math.log2(5574.0 / frequency) - math.log2(5574.0)

# sigmoid because why not
def sigmoid(freq):
    try:
        return 1 / (1.0 + math.exp(-freq))
    except OverflowError:
        return 0


# combine the dict of words commonly found in spam with the list of words commonly found in ham destructively
def getSusDict(dataset, minSusFreq = 1, minAntiSusFreq = 10, maxLen = 10):
    maxSussiness = 5.5
    antiSusScale = 0.8

    minThreshold = 1
    wordsToRemove = []

    print("\tcreating sus token set...")
    susDict = getDFDict(dataset, True)
    print("\tpruning sus token set...")
    susDict = pruneWords(susDict, minSusFreq, maxLen)
    print("\tcreating antisus token set...")
    antiSusDict = getDFDict(dataset, False)
    print("\tpruning antisus token set...")
    antiSusDict = pruneWords(antiSusDict, minAntiSusFreq, maxLen)


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

    # trim the fat off the word list
    for sus in susDict.keys():
        # if it's below the threshold, it probably won't affect the outcome much
        if abs(susDict[sus]) < minThreshold:
            wordsToRemove.append(sus)

        # # if components of the word are already in the word list
        # for end in range(len(sus)):
        #     for start in range(end):
        #         wordPiece = sus[start:end + 1]
        #         if wordPiece in susDict:
        #             wordsToRemove.append(sus)

    for word in wordsToRemove:
        if word in susDict:
            del susDict[word]

    return susDict