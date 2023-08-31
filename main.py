import numpy as np
import matplotlib.pyplot as plt
import nltk

import customNLP as nlp
import wordNGrams as chris
import charNGrams as chan
import MLNLP as ml

datasetSize = 1
testingsetSize = 0.2
minSusFreq = 4
minAntisusFreq = 12
bias = -5.5
minSusLeng = 30
lengImportance = 3

def isSpam(sms, susList):
    score = bias

    # tokens = chris.tokenize(sms, susList)
    tokens = nlp.tokenize(sms, susList)
    for token in tokens:
        score += susList[token]


    # print(sms)
    # print("tokens: " + str(tokens))
    # print()

    if (len(sms) < minSusLeng):
        score -= lengImportance * nlp.maxSussiness

    if (score >= 0):
        return True

    return False




def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"




if __name__ == "__main__":
    # nltk.download()
    TP = TN = FP = FN = 0

    dataset = open("dataset/SMSSpamCollection", "r")
    dataset = dataset.readlines()
    trainingset = [None] * int((1 - testingsetSize) * len(dataset) * datasetSize)
    testset = [None] * int(testingsetSize * len(dataset) * datasetSize)

    categories = {"ham": False, "spam": True}

    print("creating testing and training datasets...")
    # convert each sms to a list of 2 items, with True indicating that it's spam and False indicating ham
    # then convert each sms entry to a tuple
    for i in range(int(len(dataset) * datasetSize)):
        # let sms be the current text as a list [ham/spam, text]
        sms = dataset[i].replace("\n", "").split("\t")

        # if it's one of the first 90%, put it in the training dataset
        if (i < len(trainingset)):
            # let the current entry in the dataset be a tuple of (True/False, text)
            trainingset[i] = (categories[sms[0]], sms[1])

        # if it's one of the last 10%, put it in the testing dataset
        else:
            # let the current entry in the dataset be a tuple of (True/False, text)
            testset[i - len(trainingset) - 1] = (categories[sms[0]], sms[1])

        # print(sms[i])

    print("creating token sets...")
    tokenSet = nlp.getTokenSet(trainingset, minSusFreq, minAntisusFreq)

    print("testing spam detection...")
    for sms in testset:

        category = isSpam(sms[1], tokenSet)

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

    TP /= len(testset)
    TN /= len(testset)
    FP /= len(testset)
    FN /= len(testset)

    # susTokenDoc = open("susDict.txt", "w")
    # for token, weight in susWords.items():
    #     susTokenDoc.writeline(str(token) + "\t" + str(weight))
    # susTokenDoc.close()

    print(tokenSet)
    print("\nExtracted token list size: " + str(len(tokenSet)))
    print("True Pos Accuracy:\t" + str('%.2f'%(TP / (TP + FN) * 100)) + "%")
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
