import nlp
import spamFilter as sf

weightScaling = 0.01

def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"


if __name__ == "__main__":

    # Process dataset into something usable
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

    min = 1

    # mins of 1 used in search, maxes of 20 used in search because no visible improvement after that
    for k in range(min, 20):
        for l in range(min, 20):
            # weight range of 0.00 - 0.99 used in search
            for w in range(100):
                TP = TN = FP = FN = 0

                # defaults are 1, 10
                susWords = nlp.getSusDict(dataset, k, l)
                # print(susWords)

                for sms in dataset:

                    # plug sms into decision tree
                    # default is weightScaling
                    category = sf.isSpam(sms[1], susWords, w/100.0)

                    # determine confusion matrix stats
                    # if the algo thinks it's spam
                    if (category):

                        # and spam in reality
                        if (sms[0]):
                            TP += 1
                        # or ham in reality
                        else:
                            # print("False positive: " + dataset[i][1])
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

                if (TP / (TP + FN) > 0.9 and TN / (TN + FP) > 0.9):
                    print("\n\nSus min threshold: " + str(k))
                    print("Antisus min threshold: " + str(l))
                    print("Word weight scaling: " + str(w/100))
                    print("True Pos Accuracy:\t" + str('%.2f'%(TP / (TP + FN) * 100)) + "%")
                    print("True Neg Accuracy:\t" + str('%.2f'%(TN / (TN + FP) * 100)) + "%")
    # print("Average Accuracy:\t"
    #         + str('%.2f'%(((TP / (TP + FN))
    #         + (TN / (TN + FP))) * 50))
    #         + "%")

    # # print confusion matrix
    # print("\t\t\t\t\t\tReality:\n" +
    #       "\t\t\t\t|\tHam\t\t|\tSpam\t|\n" +
    #       "\t\t\tHam\t|" + format(TN) + "|" + format(FN) + "|\n"
    #       "Prediction:\t----|-----------|-----------|\n"
    #       "\t\t\tSpam|" + format(FP) + "|" + format(TP) + "|\n"
    #       "\t\t\t\t|\t\t\t|\t\t\t|\n")
    print("Finished")
