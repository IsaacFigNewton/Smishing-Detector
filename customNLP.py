import math
import wordNGrams as chris
import charNGrams as chan

maxSussiness = 5.5
antiSusScale = 0.8
maxLen = 10
maxTokenLeng = 20
minThreshold = 1
nGrams = [i for i in range(1, 20)]
susNGrams = nGrams
antiSusNGrams = nGrams



def inRanges(tuple, ranges):
    # if len(ranges) > 0:
    #     print(ranges)

    for range in ranges:
        # if the start or end falls within the range
        if (range[0] <= tuple[0] and tuple[0] < range[1] or range[0] <= tuple[1] and tuple[1] < range[1]):
            return True

    return False

# decompose text into a minimal set of character n-gram tokens from a provided set of tokens
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


def sigmoid(freq):
    try:
        return 1 / (1.0 + math.exp(-freq))
    except OverflowError:
        return 0


# combine the set of tokens commonly found in spam with the set of tokens commonly found in ham destructively
def getTokenSet(dataset, minSusFreq, minAntiSusFreq):
    tokensToRemove = []

    # print("\tcreating sus token set...")
    # susDict = chris.tokenDFs(dataset, True,  susNGrams)
    # print("\tpruning sus token set...")
    # susDict = chris.pruneTokens(susDict, minSusFreq)
    # # print(susDict)
    #
    # print("\tcreating antisus token set...")
    # antiSusDict = chris.tokenDFs(dataset, False, antiSusNGrams)
    # print("\tpruning antisus token set...")
    # antiSusDict = chris.pruneTokens(antiSusDict, minAntiSusFreq)
    # # print(antiSusDict)

    print("\tcreating sus token set...")
    susDict = chan.tokenDFs(dataset, True, susNGrams)
    print("\tpruning sus token set...")
    susDict = chan.pruneTokens(susDict, minSusFreq)

    print("\tcreating antisus token set...")
    antiSusDict = chan.tokenDFs(dataset, False, antiSusNGrams)
    print("\tpruning antisus token set...")
    antiSusDict = chan.pruneTokens(antiSusDict, minAntiSusFreq)


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