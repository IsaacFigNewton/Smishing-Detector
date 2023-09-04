import random

import numpy as np
import matplotlib.pyplot as plt
import nltk

import customNLP as nlp
import wordNGrams as chris
import charNGrams as chan
import MLNLP as ml

datasetSize = 1
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




def testNewParams(trainingset, nGrams, optimalParams, currParam, upperLowerDiv):
    currParam += 3
    params = optimalParams.copy()
    #
    # minSusFreq1 = optimalParams[3]
    # minAntisusFreq1 = optimalParams[4]
    # maxTokenLen1 = optimalParams[5]
    # bias1 = optimalParams[6]
    # minSusLen1 = optimalParams[7]
    # lenImportance1 = optimalParams[8]
    # maxSussiness1 = optimalParams[9]
    # antiSusScale1 = optimalParams[10]
    # minWeightThreshold1 = optimalParams[11]

    # originally checking in 0.01 increments, but that was intractably slow and maybe unnecessary after all
    for param in range(upperLowerDiv[0], upperLowerDiv[1]):
        param /= upperLowerDiv[2]
        params[currParam] = param

        TP = TN = FP = FN = 0

        # print("creating token sets...")
        tokenSet = nlp.getTokenSet(trainingset,
                                   params[3],
                                   params[4],
                                   params[5],
                                   nGrams[0],
                                   nGrams[1],
                                   params[9],
                                   params[10])


        tokenSet = nlp.pruneFurther(tokenSet, params[11])

        # print("testing spam detection...")
        for sms in testset:

            category = isSpam(sms[1], tokenSet, params[9], params[6], params[7], params[8])

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


        if AA > optimalParams[0]:
            optimalParams = params.copy()
            optimalParams[0] = AA
            optimalParams[1] = TPA
            optimalParams[2] = TNA


        # print("Current value: " + str('%.3f' % (param)))
        # # print("True Pos Accuracy:\t" + str('%.2f'%(TPA * 100)) + "%")
        # # print("True Neg Accuracy:\t" + str('%.2f'%(TNA * 100)) + "%")
        # print("Average Accuracy:\t"
        #         + str('%.2f'%(AA * 100))
        #         + "%")
        # print(optimalParams)


    print("Optimal parameters: " + str(optimalParams))
    return optimalParams





# **********************************************************************************************************************
if __name__ == "__main__":
    minSusFreq = 3
    minAntisusFreq = 12
    maxTokenLen = 10
    bias = -5.55
    minSusLen = 42
    lengImportance = 3
    maxSussiness = 5.0
    antiSusScale = 0.65
    minWeightThreshold = 1

    # minSusFreq = random.randint(1, 10)
    # minAntisusFreq = random.randint(1, 20)
    # maxTokenLen = random.randint(2, 20)
    # bias = random.randint(1, 20) / -2
    # minSusLen = random.randint(1, 30)
    # lengImportance = random.randint(1, 10)
    # maxSussiness = random.randint(1, 20)
    # antiSusScale = random.randint(1, 10)/10
    # minWeightThreshold = random.randint(1, 20) / 10

    # Optimal parameters: [0.9802035514750365, 0.986206896551724, 0.9742002063983488, 3.0, 12, 10, -5.55, 42.0, 3, 5.0, 0.65, 1]

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
                     minWeightThreshold]

    print("\nFinding optimal minSusFreq...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 0, (0, 5, 1))

    print("\nFinding optimal minAntisusFreq...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 1, (5, 15, 1))

    print("\nFinding optimal minSusLen...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 4, (10, 50, 1))

    print("\nFinding optimal maxTokenLen...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 2, (5, 15, 1))

    print("\nFinding optimal lengImportance...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 5, (20, 40, 10))

    print("\nFinding optimal maxSussiness...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 6, (500, 600, 100))

    print("\nFinding optimal antiSusScale...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 7, (50, 150, 100))

    print("\nFinding optimal bias...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 3, (-600, -500, 100))

    print("\nFinding optimal minWeightThreshold...")
    optimalParams = testNewParams(trainingset, [wordNGrams, charNGrams], optimalParams, 8, (50, 150, 100))


    print("\n\nOptimal parameters: " + str(optimalParams))


    # TP = TN = FP = FN = 0
    #
    # # print("creating token sets...")
    # tokenSet = nlp.getTokenSet(trainingset,
    #                            minSusFreq,
    #                            minAntisusFreq,
    #                            maxTokenLen,
    #                            wordNGrams,
    #                            charNGrams,
    #                            maxSussiness,
    #                            antiSusScale)
    #
    # tokenSet = nlp.pruneFurther(tokenSet, minWeightThreshold)
    #
    # # print("testing spam detection...")
    # for sms in testset:
    #
    #     category = isSpam(sms[1], tokenSet, maxSussiness, bias, minSusLen, lenImportance)
    #
    #     # determine confusion matrix stats
    #     # if the algo thinks it's spam
    #     if (category):
    #
    #         # and spam in reality
    #         if (sms[0]):
    #             TP += 1
    #         # or ham in reality
    #         else:
    #             # print("False positive: " + sms[1])
    #             FP += 1
    #
    #     # if the algo thinks it's ham
    #     else:
    #
    #         # and spam in reality
    #         if (sms[0]):
    #             # print("False negative: " + sms[1])
    #             FN += 1
    #         # or ham in reality
    #         else:
    #             TN += 1
    #
    # TP /= len(testset)
    # TN /= len(testset)
    # FP /= len(testset)
    # FN /= len(testset)
    # # TP accuracy
    # TPA = TP / (TP + FN)
    # # TN accuracy
    # TNA = TN / (TN + FP)
    # # Average accuracy
    # AA = (TPA + TNA) / 2
    #
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
