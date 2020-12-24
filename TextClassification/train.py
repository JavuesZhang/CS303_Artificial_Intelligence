# -*- coding: utf-8 -*-
from sklearn import svm, metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import argparse
import pandas

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train_file', type=str, default='./submodule/train.json')
    args = parser.parse_args()
    train_file = args.train_file

    data = pandas.read_json(train_file)

    train_words, test_words, train_tags, test_tags = train_test_split(
                                                        data['data'],
                                                        data['label'],
                                                        test_size=0.1,
                                                        random_state=0)

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
    predicted = text_clf.predict(test_words)
    fo = open('./output.txt', 'w')
    str1 = ''
    for clf in predicted:
        str1 += str(clf) + '\n'
    
    fo.write(str1)
    fo.close()