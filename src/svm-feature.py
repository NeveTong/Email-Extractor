###############################
# Training set for classifier
###############################

# -*- coding: utf-8 -*-

import os
import json
from emails import get_snippets
import feature
import myparser
import constant
from os.path import join

if __name__ == '__main__':
    with open(join(constant.ANALYSIS_DIR,'result_all.json')) as f:
        people = json.load(f)
        
    pid2snippets = {}   
    
    with open('svm-feature.txt','w') as wf, open('error.txt', 'w') as wf2:
        hit = 0
        empty = 0
        # person: id
        for pid in people:
            try:                           
                hit_flag = 0
                pid2snippets[pid] = {}
                person_dict = people.get(pid,'not found')
                
                snpts_cache = os.path.join(constant.CACHE_SNPTS_DIR, str(person_dict['id']) + '.json')
                snippets = get_snippets(person_dict, usecache=True, cache=snpts_cache, cverbose=True)
                snippets = myparser.filt_email(snippets)
                
                email_true_list = person_dict['email_list']
                if len(snippets) == 0:
                    empty += 1
                    
                for snippet in snippets:
                    # print("snippet:")
                    # print(snippet)
#                    email_list, prob_list = [list(t) for t in zip(*person_dict['email_list_crawl'])]
#                    feature_list = feature.get_snippet_X(person_dict, snippet)[0]                                         
#                    print(email_list)
                
                    feature_list = feature.get_snippet_X(person_dict, snippet)[0]
                    email_list = snippet['emails']
                    
                    for email in email_list:
                        if email in email_true_list:
                            label = 1
                            hit_flag = 1
                        else:
                            label = -1
                        pid2snippets[pid][email] = [label] + feature_list
                        label = '{:+}'.format(label)
                        featureLine = ' '.join(['{}:{:.3f}'.format(i, fval)    for i, fval in enumerate(feature_list, start=1)])
                        wf.write('{} {}\n'.format(label, featureLine))
                        # print('{} {}'.format(label, featureLine))
                    if hit_flag == 1:
                        hit += 1
                print(pid2snippets[pid])
            except Exception as e:
                print(e)
                wf2.write('{}\n'.format(pid))
    
    hit_rate = hit/len(people)
    net_hit_rate = hit/(len(people)-empty)
    with open('hit_rate.txt', 'w') as wf1:    
        wf1.write('{} {} {} {} {}'.format(len(people), hit, hit_rate, empty, net_hit_rate))
    
        
    with open('svm-feature.json', 'w') as wf3:    
        json.dump(pid2snippets, wf3, indent=4)
    
    
    
    
        