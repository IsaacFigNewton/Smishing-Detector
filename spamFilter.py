import rules as r

def isSpam(sms, wordList, antiWordList, susList, weightScaling):
    score = 0

    if (r.containsURL(sms)):
        score += 0.4

    if (r.containsPhoneNum(sms)):
        score += 0.5

    words = sms.split(" ")
    for word in words:

        for end in range(len(word)):
            for start in range(end):
                if word[start:end + 1] in susList:
                    score += weightScaling * susList[word]
                if word[start:end + 1] in wordList:
                    score += 0.35
                if word[start:end + 1] in antiWordList:
                    score -= 0.24


    score += 0.03 * r.susCharCount(sms)

    # if (r.isLong(sms)):
    #     score += 0.05


    if (score >= 0.5):
        return True

    return False