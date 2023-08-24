import rules as r

def isSpam(sms, wordList, weightScaling):
    score = 0

    if (r.containsURL(sms)):
        score += 0.4

    if (r.containsPhoneNum(sms)):
        score += 0.5


    for word in sms:
        # for end in range(len(word)):
        #     for start in range(end):
        #         if word[start:end + 1] in susWords:
        if word in wordList:
            score += weightScaling * wordList[word]

    score += 0.03 * r.susCharCount(sms)

    # if (r.isLong(sms)):
    #     score += 0.05


    if (score >= 0.5):
        return True
    return False