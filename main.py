import nlp
import spamFilter as sf

weightScaling = 0.01

def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"


if __name__ == "__main__":

    TP = TN = FP = FN = 0

    wordlist = open("wordlist.txt", "r").readlines()
    for i in range(len(wordlist)):
        wordlist[i] = wordlist[i].replace("\n", "")

    antiWordlist = open("antiwordlist.txt", "r").readlines()
    for i in range(len(antiWordlist)):
        antiWordlist[i] = antiWordlist[i].replace("\n", "")

    dataset = open("dataset/SMSSpamCollection", "r")
    dataset = dataset.readlines()

    categories = {"ham": False, "spam": True}

    # convert each sms to a list of 2 items, with True indicating that it's spam and False indicating ham
    # then convert each sms entry to a tuple
    for i in range (len(dataset)):
        # let sms be the current text as a list [ham/spam, text]
        sms = dataset[i].replace("\n", "").lower().split("\t")

        # let the current entry in the dataset be a tuple of (True/False, text)
        dataset[i] = (categories[sms[0]], sms[1])
        # print(sms[i])

    # mins of 1 used in search, maxes of 20 used in search because no visible improvement after that
    # defaults are 1, 10
    susWords = {}#nlp.getSusDict(dataset, 1, 10)
    # print(susWords)

    for sms in dataset:

        # plug sms into decision tree
        # default is weightScaling
        # weight range of 0.00 - 0.99 used in search, optimal found to be 0.0147
        category = sf.isSpam(sms[1], wordlist, antiWordlist, susWords, 0.0147)

        # determine confusion matrix stats
        # if the algo thinks it's spam
        if (category):

            # and spam in reality
            if (sms[0]):
                TP += 1
            # or ham in reality
            else:
                # print("False positive: " + sms[1])
                FP += 1

        # if the algo thinks it's ham
        else:

            # and spam in reality
            if (sms[0]):
                # print("False negative: " + sms[1])
                FN += 1
            # or ham in reality
            else:
                TN += 1

    TP /= 5574
    TN /= 5574
    FP /= 5574
    FN /= 5574

    print(susWords)
    print("\nTrue Pos Accuracy:\t" + str('%.2f'%(TP / (TP + FN) * 100)) + "%")
    print("True Neg Accuracy:\t" + str('%.2f'%(TN / (TN + FP) * 100)) + "%")
    print("Average Accuracy:\t"
            + str('%.2f'%(((TP / (TP + FN))
            + (TN / (TN + FP))) * 50))
            + "%")

    # print confusion matrix
    print("\t\t\t\t\t\tReality:\n" +
          "\t\t\t\t|\tHam\t\t|\tSpam\t|\n" +
          "\t\t\tHam\t|" + format(TN) + "|" + format(FN) + "|\n"
          "Prediction:\t----|-----------|-----------|\n"
          "\t\t\tSpam|" + format(FP) + "|" + format(TP) + "|\n"
          "\t\t\t\t|\t\t\t|\t\t\t|\n")
