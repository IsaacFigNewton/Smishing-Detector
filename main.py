import customNLP as nlp
# import random
# import nltk

datasetSize = 1
testingsetSize = 0.2

# 1st sublist is the sus list, 2nd sublist is the antisus list
charNGrams = [[4, 5, 6, 7, 9],[4, 5, 6, 7]]   # [[6],[6]]
wordNGrams = [[0],[0]]      # [[4],[4]]

def getSpamScore(sms, susList, maxSussiness, bias, minSusLen, lenImportance):
    score = bias

    tokens = nlp.tokenize(sms, susList)
    for token in tokens:
        score += susList[token]

    if (len(sms) < minSusLen):
        score -= lenImportance * maxSussiness


    # print(sms)
    # print(format(score))
    # # print("tokens: " + str(tokens))
    # print()

    return score




def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"




def testNewParams(trainingSet, testingSet, nGrams, optimalParams, currParam, upperLowerDiv):
    currParam += 3
    params = optimalParams.copy()

    for param in range(upperLowerDiv[0], upperLowerDiv[1]):
        param /= upperLowerDiv[2]
        params[currParam] = param

        TP = TN = FP = FN = 0

        tokenSet = nlp.getTokenSet(trainingSet,
                                   params[3],
                                   params[4],
                                   params[5],
                                   nGrams[0],
                                   nGrams[1],
                                   params[9],
                                   params[10])


        tokenSet = nlp.pruneFurther(tokenSet, params[11])

        for sms in testingSet:
            score = getSpamScore(sms[1], tokenSet, params[9], params[6], params[7], params[8])
            category = score >= 0

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


        TP /= len(testingSet)
        TN /= len(testingSet)
        FP /= len(testingSet)
        FN /= len(testingSet)
        # TP accuracy
        TPA = TP / (TP + FN + 1e-10)
        # TN accuracy
        TNA = TN / (TN + FP + 1e-10)
        # Average accuracy
        AA = (TPA + TNA) / 2

        if TPA > optimalParams[1]:
            optimalParams = params.copy()
            optimalParams[0] = AA
            optimalParams[1] = TPA
            optimalParams[2] = TNA

    print("Optimal parameters: " + str(optimalParams))
    return optimalParams





# **********************************************************************************************************************
if __name__ == "__main__":
    # nltk.download()

    minSusFreq = 3
    minAntisusFreq = 12
    maxTokenLen = 10
    bias = -3.5
    minSusLen = 42
    lenImportance = 3
    maxSussiness = 5.0
    antiSusScale = 0.65
    minWeightThreshold = 1
    # Optimal parameters for Almeida set: [0.9802035514750365, 0.986206896551724, 0.9742002063983488, 3.0, 12, 10, -5.55, 42, 3, 5.0, 0.65, 1]

    categories = {"ham": False, "spam": True}

    trainingSet = open("dataset/SMSSpamCollection", "r").readlines()
    testingSet = open("chatgpt-spam.txt", "r", encoding="utf-8").readlines()
    # convert each sms to a list of 2 items, with True indicating that it's spam and False indicating ham
    # then convert each sms entry to a tuple
    for i in range(len(trainingSet)):
        # let sms be the current text as a list [ham/spam, text]
        sms = trainingSet[i].replace("\n", "").split("\t")
        # let the current entry in the dataset be a tuple of (True/False, text)
        trainingSet[i] = (categories[sms[0]], sms[1])
    for i in range(len(testingSet)):
        # let sms be the current text as a list [ham/spam, text]
        sms = testingSet[i].replace("\n", "").split("\t")
        # let the current entry in the dataset be a tuple of (True/False, text)
        testingSet[i] = (categories[sms[0]], sms[1])

    #
    # dataset = open("dataset/SMSSpamCollection", "r").readlines()
    # trainingSet = [None] * int((1 - testingsetSize) * len(dataset) * datasetSize)
    # testingSet = [None] * int(testingsetSize * len(dataset) * datasetSize)
    #
    # print("creating testing and training datasets...")
    # # convert each sms to a list of 2 items, with True indicating that it's spam and False indicating ham
    # # then convert each sms entry to a tuple
    # for i in range(int(len(dataset) * datasetSize)):
    #     # let sms be the current text as a list [ham/spam, text]
    #     sms = dataset[i].replace("\n", "").split("\t")
    #
    #     # if it's one of the first 90%, put it in the training dataset
    #     if (i < len(trainingSet)):
    #         # let the current entry in the dataset be a tuple of (True/False, text)
    #         trainingSet[i] = (categories[sms[0]], sms[1])
    #
    #     # if it's one of the last 10%, put it in the testing dataset
    #     else:
    #         # let the current entry in the dataset be a tuple of (True/False, text)
    #         testingSet[i - len(trainingSet) - 1] = (categories[sms[0]], sms[1])


    # optimalParams = [0, 0,  0,
    #                  minSusFreq,
    #                  minAntisusFreq,
    #                  maxTokenLen,
    #                  bias,
    #                  minSusLen,
    #                  lenImportance,
    #                  maxSussiness,
    #                  antiSusScale,
    #                  minWeightThreshold]
    # while True:
    #     print("\nFinding optimal minSusFreq...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 0, (0, 5, 1))
    #     print("\nFinding optimal minAntisusFreq...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 1, (5, 15, 1))
    #     print("\nFinding optimal minSusLen...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 4, (10, 50, 1))
    #     print("\nFinding optimal maxTokenLen...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 2, (5, 15, 1))
    #     print("\nFinding optimal lengImportance...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 5, (20, 40, 10))
    #     print("\nFinding optimal maxSussiness...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 6, (500, 600, 100))
    #     print("\nFinding optimal antiSusScale...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 7, (50, 150, 100))
    #     print("\nFinding optimal bias...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 3, (-600, -500, 100))
    #     print("\nFinding optimal minWeightThreshold...")
    #     optimalParams = testNewParams(trainingSet, testingSet, [wordNGrams, charNGrams], optimalParams, 8, (50, 150, 100))
    #     print("\n\nOptimal parameters: " + str(optimalParams))



    TP = TN = FP = FN = 0

    print("creating token sets...")
    tokenSet = nlp.getTokenSet(trainingSet,
                               minSusFreq,
                               minAntisusFreq,
                               maxTokenLen,
                               wordNGrams,
                               charNGrams,
                               maxSussiness,
                               antiSusScale)
    tokenSet = nlp.pruneFurther(tokenSet, minWeightThreshold)

    print("testing spam detection...\n")
    for sms in testingSet:

        score = getSpamScore(sms[1], tokenSet, maxSussiness, bias, minSusLen, lenImportance)
        category = score >= 0

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
                print("\nFalse negative: " + sms[1])
                print(score)
                FN += 1
            # or ham in reality
            else:
                TN += 1

    TP /= len(testingSet)
    TN /= len(testingSet)
    FP /= len(testingSet)
    FN /= len(testingSet)


    # TP accuracy
    TPA = TP / (TP + FN + 1e-10)
    # TN accuracy
    TNA = TN / (TN + FP + 1e-10)
    # Average accuracy
    AA = (TPA + TNA) / 2

    # print("\n" + str(tokenSet))

    print("\nExtracted token list size: " + str(len(tokenSet)))
    print("True Pos Accuracy:\t" + str('%.2f'%(TPA * 100)) + "%")
    print("True Neg Accuracy:\t" + str('%.2f'%(TNA * 100)) + "%")
    print("Average Accuracy:\t"  + str('%.2f'%(AA * 100))  + "%")
    # print confusion matrix
    print("\t\t\t\t\t\tReality:\n" +
          "\t\t\t\t|\tHam\t\t|\tSpam\t|\n" +
          "\t\t\tHam\t|" + format(TN) + "|" + format(FN) + "|\n"
          "Prediction:\t----|-----------|-----------|\n"
          "\t\t\tSpam|" + format(FP) + "|" + format(TP) + "|\n"
          "\t\t\t\t|\t\t\t|\t\t\t|\n")
