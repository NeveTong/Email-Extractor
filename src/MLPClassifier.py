# -*- coding: utf-8 -*-

import os
import sys
import json
import pickle
import sklearn
import constant
from sklearn.externals import joblib
from sklearn import metrics
from sklearn.svm import *
from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import cross_val_predict
from sklearn.neural_network import MLPClassifier
from sklearn.feature_selection import *
from sklearn.tree import *

def performance(true, pred_prob, threshold):
    predicted = [int(p > threshold) for p in pred_prob]
    print('-------')
#    print('{:.4f} {} {:.2f} {:.2f} {:.2f} {:.4f}'.format(C_,k_,d_,g_,c_,t_))
    f1 = 100 * metrics.f1_score(true, predicted)
    recall = 100 * metrics.recall_score(true, predicted)
    precision = 100 * metrics.precision_score(true, predicted)
    accuracy = 100 * metrics.accuracy_score(true, predicted)
    auc = 100 * metrics.roc_auc_score(true, pred_prob)
    print('f1        = {:.2f}'.format(f1))
    print('recall    = {:.2f}'.format(recall))
    print('precision = {:.2f}'.format(precision))
    print('accuracy  = {:.2f}'.format(accuracy))
    print('auc       = {:.2f}'.format(auc))
    return f1, recall, precision, accuracy, auc
    
        
class MLP(MLPClassifier):
    def predict(self, X):
        return self.predict_proba(X)

if __name__ == '__main__':  

    clf = MLP(activation='tanh',solver='adam')
    dataset = load_svmlight_file('svm-feature.txt')
    pred_prob = cross_val_predict(clf, dataset[0], dataset[1], cv=7)
    pred_prob = [p[1] for p in pred_prob]
    true = [int(p > 0) for p in dataset[1]]
    performance(true, pred_prob, 0.12)
    
    clf = MLPClassifier(activation='tanh',solver='adam')
    rf = clf.fit(dataset[0], dataset[1])
    with open(constant.MLP_MOD_PATH, 'wb') as f:
        s = pickle.dump(clf, f)
        
    with open(constant.MLP_MOD_PATH, 'rb') as f:
        ss = pickle.load(f)        
    probs = ss.predict_proba(dataset[0])
    print(probs)
    
