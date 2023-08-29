import rules as r
import nlp
def isSpam(sms, wordList, antiWordList, susList, weightScaling):
    score = 0

    # if (r.containsURL(sms)):
    #     score += 0.4
    #
    # if (r.containsPhoneNum(sms)):
    #     score += 0.5

    tokens = nlp.tokenize(sms, susList)

    # print(sms)
    # print("tokens: " + str(tokens))
    # print()

    for token in tokens:
        score += weightScaling * susList[token]
        # if token in wordList:
        #     score += 0.35
        # if token in antiWordList:
        #     score -= 0.24


    # score += 0.03 * r.susCharCount(sms)

    # if (len(sms) < 30):
    #     score -= 5


    if (score >= 0):
        return True

    return False