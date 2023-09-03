import numpy as np
import matplotlib.pyplot as plt
import nltk

import customNLP as nlp
import wordNGrams as chris
import charNGrams as chan
import MLNLP as ml

datasetSize = 0.05
testingsetSize = 0.2

# 1st sublist is the sus list, 2nd sublist is the antisus list
ngram = [i for i in range(4, 20)]
charNGrams = [[6],[6]]
# no noticeable increases beyond 4-grams
wordNGrams = [[0],[0]]

def isSpam(sms, susList, maxSussiness, bias, minSusLen, lenImportance):
    score = bias

    # tokens = chris.tokenize(sms, susList)
    tokens = nlp.tokenize(sms, susList)
    for token in tokens:
        score += susList[token]


    # print(sms)
    # print("tokens: " + str(tokens))
    # print()

    if (len(sms) < minSusLen):
        score -= lenImportance * maxSussiness

    if (score >= 0):
        return True

    return False




def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"




def testNewParams(trainingset,
                   minSusFreq,
                   minAntisusFreq,
                   maxTokenLen,
                   bias,
                   minSusLen,
                   lenImportance,
                   wordNGrams,
                   charNGrams,
                   maxSussiness,
                   antiSusScale,
                   minWeightThreshold):
    TP = TN = FP = FN = 0

    # print("creating token sets...")
    tokenSet = nlp.getTokenSet(trainingset,
                               minSusFreq,
                               minAntisusFreq,
                               maxTokenLen,
                               wordNGrams,
                               charNGrams,
                               maxSussiness,
                               antiSusScale)

    tokenSet = nlp.pruneFurther(tokenSet, minWeightThreshold)

    # print("testing spam detection...")
    for sms in testset:

        category = isSpam(sms[1], tokenSet, maxSussiness, bias, minSusLen, lenImportance)

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
    # TP accuracy
    TPA = TP / (TP + FN)
    # TN accuracy
    TNA = TN / (TN + FP)
    # Average accuracy
    AA = (TPA + TNA) / 2

    return [AA, TPA, TNA]





# **********************************************************************************************************************
if __name__ == "__main__":
    minSusFreq = 4
    minAntisusFreq = 12
    bias = -5.5
    minSusLen = 30
    lengImportance = 3

    maxSussiness = 5.5
    antiSusScale = 0.8
    maxTokenLen = 10
    minWeightThreshold = 1

    loadingRate = 0.0
    allParams = []

    dataset = open("dataset/SMSSpamCollection", "r")
    dataset = dataset.readlines()
    trainingset = [None] * int((1 - testingsetSize) * len(dataset) * datasetSize)
    testset = [None] * int(testingsetSize * len(dataset) * datasetSize)

    categories = {"ham": False, "spam": True}

    # print("creating testing and training datasets...")
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


    #               AA  TPA TNA
    optimalParams = [0, 0,  0,
                     minSusFreq,
                     minAntisusFreq,
                     maxTokenLen,
                     bias,
                     minSusLen,
                     lengImportance,
                     maxSussiness,
                     antiSusScale,
                     maxTokenLen,
                     minWeightThreshold]



    print("Finding optimal minWeightThreshold...")
    # originally checking in 0.01 increments, but that was intractably slow and maybe unnecessary after all
    for minWeightThreshold in range(600):
        minWeightThreshold /= 50

        accuracies = testNewParams(trainingset,
                                     minSusFreq,
                                     minAntisusFreq,
                                     maxTokenLen,
                                     bias,
                                     minSusLen,
                                     lengImportance,
                                     wordNGrams,
                                     charNGrams,
                                     maxSussiness,
                                     antiSusScale,
                                     minWeightThreshold)

        print("minWeightThreshold = " + str('%.3f'%(minWeightThreshold)))
        print(accuracies)

        if accuracies[0] > optimalParams[0]:
            optimalParams = [accuracies[0], accuracies[1], accuracies[2],
                             minSusFreq,
                             minAntisusFreq,
                             maxTokenLen,
                             bias,
                             minSusLen,
                             lengImportance,
                             maxSussiness,
                             antiSusScale,
                             maxTokenLen,
                             minWeightThreshold]


    # for minSusFreq in range(5):
    #     for minAntisusFreq in range(10, 15):
    #         for minSusLen in range(20, 40):
    #             for lengImportance in range(5):
    #                 for maxSussiness in range(4, 24):
    #                     maxSussiness /= 4
    #
    #                     print("Progress: " + str('%.5f' % (loadingRate * 100)) + "%")
    #                     # originally checking in 0.05 increments, but that was intractably slow
    #                     for antiSusScale in range(10):
    #                         antiSusScale /= 10
    #                         for maxTokenLen in range(1, 15):
    #                             for bias in range(-4, -24, -1):
    #                                 bias /= 4


    print("Optimal parameters: " + str(optimalParams))
    # print("\nExtracted token list size: " + str(len(tokenSet)))
    # print("True Pos Accuracy:\t" + str('%.2f'%(TPA * 100)) + "%")
    # print("True Neg Accuracy:\t" + str('%.2f'%(TNA * 100)) + "%")
    # print("Average Accuracy:\t"
    #         + str('%.2f'%(AA * 100))
    #         + "%")
    #
    # # print confusion matrix
    # print("\t\t\t\t\t\tReality:\n" +
    #       "\t\t\t\t|\tHam\t\t|\tSpam\t|\n" +
    #       "\t\t\tHam\t|" + format(TN) + "|" + format(FN) + "|\n"
    #       "Prediction:\t----|-----------|-----------|\n"
    #       "\t\t\tSpam|" + format(FP) + "|" + format(TP) + "|\n"
    #       "\t\t\t\t|\t\t\t|\t\t\t|\n")
