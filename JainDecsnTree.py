# phone number validation
import re

def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"


susWords = open("wordlist.txt", "r").read().split("  ")
urlWords = {"http://", "www."}
emailWords = {".com", ".net", ".uk"}

# rule 1
def containsURL(sms):
    text = sms.split(" ")
    for word in text:
        for i in range(len(word)):
            if word[0:i + 1] in urlWords:
                return True

    return False

# rule 2
def containsMath(sms):
    return ("+" or "-" or "<" or ">" or "*" or "/" in sms)

# rule 3
def containsCurrency(sms):
    return ("$" or "£" in sms)

# rule 4
def containsPhoneNum(sms):
    # check all strings that may be parsed to form a phone number

    # determine if the sms contains a number and if so, get the f
    firstNumI = 1000
    for i in range(10):
        numI = sms.find(str(i))
        if numI < firstNumI and numI > -1:
            firstNumI = numI

    for end in range(firstNumI, len(sms)):
        for start in range(i):
            if bool(re.match("^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$", sms[start: end + 1])):
                return True

    return False

# rule 5
def containsSusWords(sms):
    text = sms.split(" ")
    for word in text:
        if word in susWords:
            return True

    return False

# # rule 6
# # Rule 6: IF message length is greater than 150 character, THEN it is potentially a smishing message.
# #     This length including space, symbols, special characters, smileys, etc.
# def isLong(sms):
#     return len(sms) > 150

# rule 7
def selfAnswering(sms):
    return sms.find("subscribe") > -1

# rule 8
# Rule 8: IF message contains emojis, THEN it is probably a smishing message.
#     Emojis are numerals and other signs used in writing text messages or emails etc.
def containsMorpheme(sms):
    return False

# rule 9
# Rule 9: IF message contains the e-mail address, THEN it is likely a smishing message.
def containsEmail(sms):
    # if sms.find("@") > 0:
    #     text = sms.split(" ")
    #     for word in text:
    #         for i in range(len(word)):
    #             if word[-1: -1 * (i + 1)] in emailWords:
    #                 return True

    return False

# *******************************************************************************************************************************************

def isSpam(sms):
    # decsn tree:
    # Rule 5: The presence of suspicious keywords like, free, accident, awards, dating, won, service, lottery, mins,
    #   visit, delivery, cash, claim, Prize, delivery, etc. are considered as smishing keywords. If any of the suspicious
    #   keyword present in the message, THEN it is a presumably a smishing message.
    if (containsSusWords(sms)):

        # Rule 4: IF mobile number present in the message, THEN it is a probably a smishing message.
        if (containsPhoneNum(sms)):
            return True
        else:

            # Rule 1: If URL present in the message, THEN it is probably a smishing message.
            if (containsURL):
                return True
            else:

                # Rule 3: IF message contains any currency sign like “$”, “£”, etc., THEN it is a probably a smishing message.
                #     We have selected two symbols frequently present in the smishing message namely $ (Dollar) and £ (Pound).
                if (containsCurrency(sms)):
                    return True
                else:

                    # Rule 2: If the message contains any mathematical symbol like +, -, <, >, /, etc., THEN it is a probably a smishing
                    #     message.
                    if containsMath(sms):
                        return True
                    else:

                        # Rule 7: IF message is the self-answering type, THEN it is a likely a smishing message.
                        #     The presence of selfanswering SMS asks the user to subscribe or unsubscribe any service.
                        return selfAnswering(sms)

    else:
        # Rule 4: IF mobile number present in the message, THEN it is a probably a smishing message.
        return containsPhoneNum(sms) or containsURL(sms)

# *******************************************************************************************************************************************

if __name__ == "__main__":

    TP = TN = FP = FN = 0

    # Process dataset into something usable
    dataset = open("dataset/SMSSpamCollection", "r")
    dataset = dataset.readlines()
    categories = {"ham": False, "spam": True}


    # convert each sms to a list of 2 items, with True indicating that it's spam and False indicating ham
    # use a list instead of a tuple because lists are modifiable
    for i in range (len(dataset)):
        # let sms be the current text as a list [ham/spam, text]
        sms = dataset[i].replace("\n", "").lower().split("\t")
        # let the current entry in the dataset be a tuple of (True/False, text)
        dataset[i] = (categories[sms[0]], sms[1])
        # print(sms[i])

        # plug sms into decision tree
        category = isSpam(sms[1])

        # determine confusion matrix stats
        # if the algo thinks it's spam
        if (category):

            # and spam in reality
            if (dataset[i][0]):
                TP += 1
            # or ham in reality
            else:
                FP += 1

        # if the algo thinks it's ham
        else:

            # and spam in reality
            if (dataset[i][0]):
                FN += 1
            # or ham in reality
            else:
                TN += 1

    accuracy = (TP + TN)/(TP + TN + FP + FN)

    TP /= 5574
    TN /= 5574
    FP /= 5574
    FN /= 5574

    print("Accuracy:\t" + str('%.2f'%(accuracy * 100)) + "%")

    # print confusion matrix
    print("\t\t\t\t\t\tReality:\n" +
          "\t\t\t\t|\tHam\t\t|\tSpam\t|\n" +
          "\t\t\tHam\t|" + format(TN) + "|" + format(FN) + "|\n"
          "Prediction:\t----|-----------|-----------|\n"
          "\t\t\tSpam|" + format(FP) + "|" + format(TP) + "|\n"
          "\t\t\t\t|\t\t\t|\t\t\t|\n")
