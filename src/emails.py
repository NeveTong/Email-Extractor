#############################################
# Get the emails and classification results
#############################################

import os
import csv
import constant
import json
import prep
import myparser
import pickle
import feature
import util
import crawler
from os.path import join


class Classifier:
    model = None
    threshold = 0.5

    @classmethod
    def pred_proba(cls, X):
        if not cls.model:
            with open(constant.SVM_MOD_PATH, 'rb') as f:
                cls.model = pickle.load(f)
        probs = cls.model.predict_proba(X)
        probs = [p[1] for p in probs]
        return probs


@util.cache('json')
def get_snippets(person, aff=True):
    if aff == True:
        query = '{} {} email'.format(person['name'], person['simple_affiliation'])
    else:
        query = '{} email'.format(person['name'])
    gpage = crawler.search(query, usecache=True, useproxy=True, cache='../cache/{}.html'.format(person['id']), checkpage=True)
    snippets1 = myparser.parse(gpage)
    
    if len(person['name_zh']) > 0:  
        if aff == True:
            query = '{} {} email'.format(person['name_zh'], person['simple_affiliation'])
        else:
            query = '{} email'.format(person['name_zh'])
        gpage = crawler.search(query, usecache=True, useproxy=True, cache='../cache/Chinese/{}.html'.format(person['id']), checkpage=True)
        snippets2 = myparser.parse(gpage)       
        return snippets1+snippets2
    else:
        return snippets1
 

def get_emails(person):
    X = []
    emails = []
    snpts_cache = join(constant.CACHE_SNPTS_DIR, str(person['id']) + '.json')
    snippets = get_snippets(person, aff=True, usecache=True, cache=snpts_cache, cverbose=True)
    snippets = myparser.filt_email(snippets)
    if not snippets:
        return []
    for snippet in snippets:
        X += feature.get_snippet_X(person, snippet)
        emails += snippet['emails']
    probs = Classifier.pred_proba(X)
    eps = zip(emails, probs)
    eps = sorted(eps, key=lambda a: a[1], reverse=True)
    
    if len(person['simple_affiliation'].split(' ')) > 11 and eps[0][1] < 0.9:
        print('sim_aff too long: ',person['simple_affiliation'])
        snpts_cache = join(constant.CACHE_NOAFF_SNPTS_DIR, str(person['id']) + '.json')
        snippets = get_snippets(person, aff=False, usecache=True, cache=snpts_cache, cverbose=True)
        snippets = myparser.filt_email(snippets)
        if not snippets:
            return []
        for snippet in snippets:
            X += feature.get_snippet_X(person, snippet)
            emails += snippet['emails']
        probs = Classifier.pred_proba(X)
        eps = zip(emails, probs)
        eps = sorted(eps, key=lambda a: a[1], reverse=True)
        
    return eps