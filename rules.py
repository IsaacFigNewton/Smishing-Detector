import re

egg = "egg"
susWords = open("wordlist.txt", "r").readlines()
for i in range(len(susWords)):
    susWords[i] = susWords[i].replace("\n", "")

susChars = open("charlist.txt", "r").readlines()
for i in range(len(susChars)):
    susChars[i] = susChars[i].replace("\n", "")

# Rule 1: If URL present in the message, THEN it is probably a smishing message.
def containsURL(sms):
    sms.replace(". ", ".")
    text = sms.split(" ")

    for word in text:
        # if it matches the format of a URL
        if word.find("..") < 0\
                and word.count(".") > 1\
                and len(word) > 11\
                and re.match(r"^(http://)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/[a-zA-Z0-9_\-./]+)?(\?[a-zA-Z0-9=&]+)?$", word):
            return True

    return False


# broken
def containsURL(sms):
    text = sms.split(" ")

    for word in text:
        # if it matches the format of a URL
        if re.match(r"^(?:mailto:)?(?:[a-zA-Z0-9][a-zA-Z0-9\-.]*\.)?(?:[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*\.)?[a-zA-Z0-9][a-zA-Z0-9\-.]*\.[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})$", word):
            return True

    return False


# not accurate enough
# Rule 4: IF mobile number present in the message, THEN it is a probably a smishing message.
def containsPhoneNum(sms):
    # if sms == "do you want a new video handset? 750 any time any network mins? unlimited text? camcorder? reply or call now 08000930705 for del sat am":
    #     print(egg)

    # determine if the sms contains a number and if so, get the first index of one
    firstNumI = 1000
    for i in range(10):
        numI = sms.find(str(i))

        # starting with the first occurrence of a number and going until there's not enough space for a phone # to exist
        j = numI
        while j > -1 and j < len(sms) - 10:
            # check if it might be a phone number without the symbols
            if (sms[j: j + 5].isdigit() or sms[j: j + 11].isdigit()):
                return True

            # check the next occurrence of the number, if one exists
            nextRelI = sms[j + 1:].find(str(i))

            # if one does exist, move j to that respective index in sms
            if (nextRelI > -1):
                j += nextRelI + 1
            else:
                break

        if numI < firstNumI and numI > -1:
            firstNumI = numI


    # check all strings that may be parsed to form a phone number
    for end in range(firstNumI, len(sms)):
        for start in range(i):
            if bool(re.match("^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$", sms[start: end + 1])):
                return True

    return False


# Rule 5: The presence of suspicious keywords like, free, accident, awards, dating, won, service, lottery, mins,
    #   visit, delivery, cash, claim, Prize, delivery, etc. are considered as smishing keywords. If any of the suspicious
    #   keyword present in the message, THEN it is a presumably a smishing message.
def susWordCount(sms):
    textCombos = sms.split(" ")
    count = 0

    for word in textCombos:
        for end in range(len(word)):
            for start in range(end):
                if word[start:end + 1] in susWords:
                    count += 1

    return count


# Rule 6: IF message length is greater than 150 character, THEN it is potentially a smishing message.
#     This length including space, symbols, special characters, smileys, etc.
def isLong(sms):
    return len(sms) > 150


def susCharCount(sms):
    count = 0
    for char in sms:
        if ord(char) > 126 or char in susChars:
            count += 1

    return count