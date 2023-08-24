import math

# minSusFreq = 1
# minAntiSusFreq = 4

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

            # check if each word in the text is in the idfDict, and if it isn't put it there
            for word in text:
                if word in idfDict:
                    if word not in countedWords:
                        idfDict[word] += 1
                        countedWords.add(word)
                else:
                    idfDict[word] = 1

    return idfDict


def removeUncommonWords(dict, minFreq):
    wordsToRemove = []

    for key in dict.keys():
        if (minFreq >= dict[key]):
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
def getSusDict(dataset, minSusFreq, minAntiSusFreq):
    susDict = removeUncommonWords(getDFDict(dataset, True), minSusFreq)
    antiSusDict = removeUncommonWords(getDFDict(dataset, False), minAntiSusFreq)


    # combine the sus and antisus frequencies destructively
    for sus in susDict.keys():
        if sus in antiSusDict:
            susDict[sus] = susDict[sus] - antiSusDict[sus] * 0.7

    for antiSus in antiSusDict.keys():
        if antiSus not in susDict:
            susDict[antiSus] = -1 * antiSusDict[antiSus]

    for sus in susDict.keys():
        susDict[sus] = sigmoid(susDict[sus])

    return susDict


    # # combine the sus and antisus frequencies destructively using idf
    # max pos accuracy of 85.68%
    # max neg accuracy of 84.83%
    # for sus in susDict.keys():
    #     # get idf of sus words
    #     susDict[sus] = math.log(5574.0 / susDict[sus])
    #     if sus in antiSusDict:
    #         # add the log of the df of the antisus words to the sus weight
    #         susDict[sus] = susDict[sus] - math.log(antiSusDict[sus])
    #
    # for antiSus in antiSusDict.keys():
    #     if antiSus not in susDict:
    #         # add the log of the df of the antisus words to the sus weight
    #         susDict[antiSus] = -1 * math.log(5574.0 / antiSusDict[antiSus])
    #
    # # for sus in susDict.keys():
    # #     susDict[sus] = sigmoid(susDict[sus])
    #
    # return susDict