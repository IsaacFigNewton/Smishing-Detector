import rules as r

def isSpam(sms):

    score = 0
    if (r.containsURL(sms)):
        score += 0.4

    if (r.containsPhoneNum(sms)):
        score += 0.5

    # idea: weigh different words differently based on whether they're more likely to appear in a spam or ham text
    # maybe this is where TFIDF/NLP comes in
    score += 0.2 * r.susWordCount(sms)

    score += 0.03 * r.susCharCount(sms)

    # if (r.isLong(sms)):
    #     score += 0.05


    if (score >= 0.5):
        return True
    return False