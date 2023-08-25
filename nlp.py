import math

# create a dictionary of words that appear in the dataset and the number of docs that contain them
def getDFDict(dataset, hamSpam):
    idfDict = {}

    # wordlist = open("wordlist.txt", "r").readlines()
    # for i in range(len(wordlist)):
    #     wordlist[i] = wordlist[i].replace("\n", "")
    #
    # for word in wordlist:
    #     idfDict[word] = 0.4

    for sms in dataset:
        # add a word to the idfDict if the sms from which it originated is the type desired
        if (sms[0] == hamSpam):
            countedWords = set()

            # break each sms into a list of its component words
            text = sms[1]
            text = text.split(" ")

            # check if every possible word in the text is in the idfDict, and if it isn't put it there
            for word in text:
                for end in range(len(word)):
                    for start in range(end):
                        wordPiece = word[start:end + 1]
                        if wordPiece in idfDict:
                            if wordPiece not in countedWords:
                                idfDict[wordPiece] += 1
                                countedWords.add(wordPiece)
                        else:
                            idfDict[wordPiece] = 1

    return idfDict


def pruneWords(dict, minFreq, maxLen):
    wordsToRemove = []

    for key in dict.keys():
        if (minFreq >= dict[key] or len(key) >= maxLen):
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

    susDict = pruneWords(getDFDict(dataset, True), minSusFreq, maxLen)
    antiSusDict = pruneWords(getDFDict(dataset, False), minAntiSusFreq, maxLen)


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