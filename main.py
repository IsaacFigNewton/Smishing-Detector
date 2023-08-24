import spamFilter as sf

def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"

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
        category = sf.isSpam(sms[1])

        # determine confusion matrix stats
        # if the algo thinks it's spam
        if (category):

            # and spam in reality
            if (dataset[i][0]):
                TP += 1
            # or ham in reality
            else:
                # print("False positive: " + dataset[i][1])
                FP += 1

        # if the algo thinks it's ham
        else:

            # and spam in reality
            if (dataset[i][0]):
                print("False negative: " + dataset[i][1])
                FN += 1
            # or ham in reality
            else:
                TN += 1

    TP /= 5574
    TN /= 5574
    FP /= 5574
    FN /= 5574

    print("\n\nTrue Pos Accuracy:\t" + str('%.2f'%(TP / (TP + FN) * 100)) + "%")
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
