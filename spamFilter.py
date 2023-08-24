import rules as r

def isSpam(sms):
    # decsn tree:
    # if (r.susWordCount(sms) > 0):
    #     if (r.containsPhoneNum(sms)
    #         or r.containsEmail(sms)
    #         or r.containsURL(sms)
    #         or r.containsCurrency(sms)
    #         or r.weirdCharCount(sms) > 0
    #         or r.isLong(sms)
    #         or r.mathSymbolCount(sms) > 0):
    #         return True
    #     else:
    #         return r.selfAnswering(sms)
    #
    # else:
    #     return r.containsPhoneNum(sms) or r.containsURL(sms) or r.containsEmail(sms)

    score = 0
    if (r.containsURL(sms)):
        score += 0.5

    score += 0.3 * r.mathSymbolCount(sms)

    if (r.containsCurrency(sms)):
        score += 0.5

    if (r.containsPhoneNum(sms)):
        score += 0.5

    score += 0.3 * r.susWordCount(sms)

    if (r.isLong(sms)):
        score += 0.5

    if (r.selfAnswering(sms)):
        score += 0.5

    # if (containsMorpheme(sms)):
    #     score += 0.05

    if (r.containsEmail(sms)):
        score += 0.5

    score += 0.05 * r.weirdCharCount(sms)

    if (score >= 0.5):
        return True
    return False