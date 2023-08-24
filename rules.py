import re

egg = "egg"
susWords = open("wordlist.txt", "r").read().split(" ")
urlWords = {"http://", "www."}
emailWords = {"com", "net", "uk"}
mathSymbols = {"+", "-", "=", "/", "*", ">", "<"}
currencies = {"$", "£"}
emojiIndicators = {"&lt;", "&gt;"}


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


# Rule 2: If the message contains any mathematical symbol like +, -, <, >, /, etc., THEN it is a probably a smishing
#     message.
def mathSymbolCount(sms):
    count = 0
    for symbol in mathSymbols:
        if (sms.find(symbol) > -1):
            count += 1
    return count


# Rule 3: IF message contains any currency sign like “$”, “£”, etc., THEN it is a probably a smishing message.
#     We have selected two symbols frequently present in the smishing message namely $ (Dollar) and £ (Pound).
def containsCurrency(sms):
    for symbol in currencies:
        if (sms.find(symbol) > -1):
            return True
    return False


# not accurate enough
# Rule 4: IF mobile number present in the message, THEN it is a probably a smishing message.
def containsPhoneNum(sms):
    if sms == "santa calling! would your little ones like a call from santa xmas eve? call 09058094583 to book your time.":
        print(egg)

    # determine if the sms contains a number and if so, get the first index of one
    firstNumI = 1000
    for i in range(10):

        numI = sms.find(str(i))

        # starting with the first occurrence of a number and going until there's not enough space for a phone # to exist
        j = numI
        while j > -1 and j < len(sms) - 10:
            # check if it might be a phone number without the symbols
            if (sms[j: j + 12].isdigit()):
                return True

            # check the next occurrence of the number, if one exists
            nextRelI = sms[j + 1: len(sms)].find(str(i))
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


# Rule 7: IF message is the self-answering type, THEN it is a likely a smishing message.
#     The presence of selfanswering SMS asks the user to subscribe or unsubscribe any service.
def selfAnswering(sms):
    return sms.find("subscribe") > -1


# Rule 8: IF message contains emojis, THEN it is probably a smishing message.
#     Emojis are numerals and other signs used in writing text messages or emails etc.
def containsMorpheme(sms):
    for emoji in emojiIndicators:
        if emoji in sms:
            return True
    return False


# Rule 9: IF message contains the e-mail address, THEN it is likely a smishing message.
def containsEmail(sms):
    if sms.find("@") > -1:
        # break the text following the @ symbol into words to check
        text = sms[sms.find("@"):-1].split(" ")
        for word in text:
            for i in range(len(word)):
                if word[i: -1] in emailWords:
                    return True

    return False


def weirdCharCount(sms):
    count = 0
    for char in sms:
        if ord(char) > 126:
            count += 1

    return count