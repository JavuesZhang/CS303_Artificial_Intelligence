# -*- coding: utf-8 -*-
from sklearn import svm, metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import argparse
import json

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train_file', type=str, default='./submodule/train.json')
    parser.add_argument('-i', '--test_file', type=str, default='./submodule/testdataexample')
    args = parser.parse_args()
    train_file = args.train_file
    test_file = args.test_file

    with open(train_file, 'r') as f:
        data = json.load(f)
    with open(test_file, 'r') as f:
        test_data = json.load(f)

    train_words = []
    train_tags = []
    for dic in data:
        train_words.append(dic['data'])
        train_tags.append(dic['label'])

    text_clf = Pipeline([
        ('vect', CountVectorizer()), 
        ('tfidf', TfidfTransformer()), 
        ('clf', SGDClassifier(
            loss='hinge', 
            penalty='l2', 
            alpha=1e-4, 
            random_state=42, 
            max_iter=500, 
            tol=None)), 
    ])
    # parameters = {
    #     'clf__alpha': (1e-2, 1e-3, 1e-4, 1e-5)
    #     }
    # gs_clf = GridSearchCV(text_clf, parameters, cv=10, n_jobs=-1)
    # gs_clf = gs_clf.fit(train_words[:400], train_tags[:400])
    # print(gs_clf.best_estimator_)
    # gs_clf = gs_clf.best_estimator_
    # predicted = gs_clf.predict(test_words)

    text_clf.fit(train_words, train_tags)
    predicted = text_clf.predict(test_data)
    fo = open('./output.txt', 'w')
    for clf in predicted:
        fo.write(str(clf) + '\n')
    
    fo.close()