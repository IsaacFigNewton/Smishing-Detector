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
                wordPiece = word[start:end + 1]
                if wordPiece in susList:
                    score += weightScaling * susList[wordPiece]
                if wordPiece in wordList:
                    score += 0.35
                if wordPiece in antiWordList:
                    score -= 0.24


    # score += 0.03 * r.susCharCount(sms)

    if (len(sms) < 30):
        score -= 5


    if (score >= 0):
        return True

    return False