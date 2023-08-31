import numpy as np
import matplotlib.pyplot as plt
import nltk

import customNLP as nlp
import wordNGrams as chris
import charNGrams as chan
import MLNLP as ml

datasetSize = 0.1
testingsetSize = 0.2

# 1st sublist is the sus list, 2nd sublist is the antisus list
ngram = [i for i in range(4, 20)]
charNGrams = [[6],[6]]
# no noticeable increases beyond 4-grams
wordNGrams = [[0],[0]]

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
        score -= lengImportance * maxSussiness

    if (score >= 0):
        return True

    return False




def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"




if __name__ == "__main__":
    # minSusFreq = 4
    # minAntisusFreq = 12
    # bias = -5.5
    # minSusLeng = 30
    # lengImportance = 3
    #
    # maxSussiness = 5.5
    # antiSusScale = 0.8
    # maxLen = 10
    # maxTokenLeng = 20
    # minWeightThreshold = 1

    allParams = []

    for minSusFreq in range(11):
        for minAntisusFreq in range(21):
            for bias in range(0, -40, -1):
                bias /= 4
                for minSusLeng in range(31):
                    for lengImportance in range(11):
                        for maxSussiness in range(41):
                            maxSussiness /= 4
                            for antiSusScale in range(21):
                                antiSusScale /= 20
                                for maxLen in range(21):
                                    for maxTokenLeng in range(31):
                                        for minWeightThreshold in range(101):
                                            minWeightThreshold /= 50
                                            # minAntisusFreq = 12
                                            # bias = -5.5
                                            # minSusLeng = 30
                                            # lengImportance = 3
                                            #
                                            # maxSussiness = 5.5
                                            # antiSusScale = 0.8
                                            # maxLen = 10
                                            # maxTokenLeng = 20
    
                                            TP = TN = FP = FN = 0
    
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
    
                                                # print(sms[i])
    
                                            # print("creating token sets...")
                                            tokenSet = nlp.getTokenSet(trainingset,
                                                                       minSusFreq,
                                                                       minAntisusFreq,
                                                                       maxLen,
                                                                       wordNGrams,
                                                                       charNGrams,
                                                                       maxSussiness,
                                                                       antiSusScale,
                                                                       minWeightThreshold)
    
                                            # print("testing spam detection...")
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
                                            # TP accuracy
                                            TPA = TP / (TP + FN)
                                            # TN accuracy
                                            TNA = TN / (TN + FP)
                                            # Average accuracy
                                            AA = (TPA + TNA) / 2
    
                                            # susTokenDoc = open("susDict.txt", "w")
                                            # for token, weight in susWords.items():
                                            #     susTokenDoc.writeline(str(token) + "\t" + str(weight))
                                            # susTokenDoc.close()
    
                                            # print(tokenSet)
    
                                            # exclude params from param file that result in no spam/ham detection
                                            if AA != 0.5:
                                                # have the accuracies be the header of the list/first items
                                                params = [AA, TPA, TNA,
                                                          minSusFreq,
                                                          minAntisusFreq,
                                                          bias,
                                                          minSusLeng,
                                                          lengImportance,
                                                          maxSussiness,
                                                          antiSusScale,
                                                          maxLen,
                                                          maxTokenLeng,
                                                          minWeightThreshold]
                                                allParams.append(params)

                                                # 97.09% is the rate to beat
                                                if params[0] > 0.9709:
                                                    print(params)
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

    # get the set of params that led to the highest avg accuracy
    optimalParams = [0, 0, 0]
    for params in allParams:
        # indexing should be 0 for AA, 1 for TPA, 2 for TNA, or >2 for anything else
        if params[0] > optimalParams[0]:
            optimalParams = params

    print("Optimal parameters: " + str(optimalParams))
    paramFile = open("params.txt", "w")
    for paramSet in allParams:
        for param in paramSet:
            paramFile.write(str(param) + " ")
        paramFile.write("\n")