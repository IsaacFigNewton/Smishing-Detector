import re

egg = "egg"

susChars = open("charlist.txt", "r").readlines()
for i in range(len(susChars)):
    susChars[i] = susChars[i].replace("\n", "")




# broken
def containsURL(sms):
    text = sms.split(" ")

    for word in text:
        # if it matches the format of a URL
        if re.match(r"^(?:mailto:)?(?:[a-zA-Z0-9][a-zA-Z0-9\-.]*\.)?(?:[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*\.)?[a-zA-Z0-9][a-zA-Z0-9\-.]*\.[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})$", word):
            return True

    return False


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


def susCharCount(sms):
    count = 0
    for char in sms:
        if ord(char) > 126 or char in susChars:
            count += 1

    return count