import random
import numpy as np
import matplotlib as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import nltk as nlp

datasetSize = 1
minSusLen = 500

charNGrams = range(1, 6)

def prune_tokens(dict, minFreq, maxLen):
    tokensToRemove = []

    for key in dict.keys():
        if (dict[key] <= minFreq or maxLen <= (len(key) and " " not in key)):
            # add it to a list of tokens to prune
            tokensToRemove.append(key)

    for token in tokensToRemove:
        del dict[token]

    return dict


# takes in a pd.Series, pd.DataFrame and returns an np.array
def knn_predict_spam(document, corpus):
    # clean the corpus
    corpus = corpus.dropna(axis=0)

    # extract the classifications and email bodies
    classifications = np.array(corpus["class"])
    corpus = corpus["text"]

    # print(document)

    # create and fit the vectorizer
    vec = TfidfVectorizer(norm=None, ngram_range=(1, 1))
    vec.fit(corpus)

    # vectorize the corpus and document
    corpus_sparse = vec.transform(corpus)
    document_sparse = vec.transform(document)

    # create and fit the model
    model = KNeighborsClassifier(n_neighbors=5, metric=(lambda x, y: 1 - cosine_similarity(x, y)))
    model.fit(corpus_sparse, np.array(classifications))

    return model.predict(document_sparse)


def get_spam_scores(documents, corpus):
    # add the bias
    scores = pd.Series(data=np.zeros(len(documents)))

    lenWeight = 0.01

    model_predictions = pd.Series(data = knn_predict_spam(documents, corpus).astype(float))
    print(model_predictions.head())
    scores = scores + model_predictions
    print(model_predictions.head())


    # if (len(sms) < minSusLen):
    #     score += lenWeight * len(sms)

    return scores

def format(stat):
    return "\t" + str('%.3f'%stat) + "\t"


if __name__ == "__main__":
    # nltk.download()

    categories = {"ham": 0, "spam": 1}
    corpus = pd.read_csv("dataset\SMSSpamCollection.txt", sep="\t", on_bad_lines='warn')

    # clean and prepare the dataset
    corpus.columns = ["class", "text"]
    classifications = corpus["class"]
    corpus["class"] = classifications.map(categories)
    corpus = corpus.loc[:200]

    train, test = train_test_split(corpus, test_size=0.2)
    predictions = pd.Series(data = get_spam_scores(test["text"], train))
    expected_and_predictions = pd.concat([test["class"], predictions], axis=1, ignore_index=True)

    print(expected_and_predictions.head())

    # # print(corpus.head())
    # sms = "free money click here"
    # print(sms)
    #
    # prediction = get_spam_score(pd.Series(data=[sms]), corpus)[0]
    # if 0 < prediction:
    #     print("The sms is spam")
    # else:
    #     print("The sms is ham")

