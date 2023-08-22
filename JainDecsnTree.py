def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"

def isSpam(sms):
    # decsn tree:
    """
    Rule 1: If URL present in the message, THEN it is probably a smishing message.
    Rule 2: If the message contains any mathematical symbol like +, -, <, >, /, etc., THEN it is a probably a smishing
    message.
    Rule 3: IF message contains any currency sign like “$”, “£”, etc., THEN it is a probably a smishing message.
        We have selected two symbols frequently present in the smishing message namely $ (Dollar) and £ (Pound).
    Rule 4: IF mobile number present in the message, THEN it is a probably a smishing message.
    Rule 5: The presence of suspicious keywords like, free, accident, awards, dating, won, service, lottery, mins,
    visit, delivery, cash, claim, Prize, delivery, etc. are considered as smishing keywords. If any of the suspicious
    keyword present in the message, THEN it is a presumably a smishing message.
    Rule 6: IF message length is greater than 150 character, THEN it is potentially a smishing message.
        This length including space, symbols, special characters, smileys, etc.
    Rule 7: IF message is the self-answering type, THEN it is a likely a smishing message.
        The presence of selfanswering SMS asks the user to subscribe or unsubscribe any service.
    Rule 8: IF message contains visual morphemes, THEN it is probably a smishing message.
        Visual Morphemes are numerals and other signs used in writing text messages or emails etc.
    Rule 9: IF message contains the e-mail address, THEN it is likely a smishing message.
    """


    return False



if __name__ == "__main__":
    TP = TN = FP = FN = 0


    # Process dataset into something usable
    dataset = open("dataset/SMSSpamCollection", "r")
    dataset = dataset.readlines()
    categories = {"ham": False, "spam": True}


    # convert each sms to a list of 2 items, with True indicating that it's spam and False indicating ham
    # use a list instead of a tuple because lists are modifiable
    for i in range (len(dataset)):
        sms = dataset[i].replace("\n", "").split("\t")
        dataset[i] = (categories[sms[0]], sms[1])

        # plug into decision tree
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


    TP /= 5574
    TN /= 5574
    FP /= 5574
    FN /= 5574


    # print confusion matrix
    print("\t\t\t\t\t\tReality:\n" +
          "\t\t\t\t|\tHam\t\t|\tSpam\t|\n" +
          "\t\t\tHam\t|" + format(TN) + "|" + format(FN) + "|\n"
          "Prediction:\t----|-----------|-----------|\n"
          "\t\t\tSpam|" + format(FP) + "|" + format(TP) + "|\n"
          "\t\t\t\t|\t\t\t|\t\t\t|\n")