##############################
# Preprocess the input files
##############################

# -*- coding: utf-8 -*-

import csv
import constant
import os
import xlrd
from openpyxl import Workbook
import re
import json
from os.path import *
import sys
from itertools import islice  
from gopage import parser

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

def contain_chinese(check_str):
    match = zhPattern.search(check_str)
    if match:
        return True   
    return False

def parse_emails(content):
    emails = []
    rough_pattern = re.compile('[A-Za-z0-9-\._]+(@| at | \[at\] |\[at\]| \(at\) |\(at\)| @ | \-at\- |<at>)(([a-z0-9\-]+)(\.| dot | \. | \[dot\] |\(dot\)|<dot>))+([a-z]+)')
    rough_match = rough_pattern.finditer(content)
    for rm in rough_match:
        pattern = re.compile('(([A-Za-z0-9-_]+)(\.| dot | \. )?)+(@| at | \[at\] |\[at\]| \(at\) |\(at\)| @ | \-at\- |<at>)(([a-z0-9\-]+)(\.| dot | \. | \[dot\] |\(dot\)|<dot>))+([a-z]+)')
        match = pattern.finditer(rm.group())
        for m in match:
            emails.append(m.group().lower().replace(' dot ', '.').replace('(dot)', '.').replace(' at ', '@').replace('[at]', '@').replace('(at)', '@').replace('(@)', '@').replace(' [dot] ', '.').replace('<dot>', '.').replace('<at>', '@').replace('--@--', '@').replace('-at-', '@').replace(' ', ''))
    return emails
    
def split_aff(aff):
    for sep in constant.AFF_SEPARATOR:
        if sep in aff:
            return aff.split(sep)
    return aff.split(';')

def find_simple_affiliation(aff):
    
    print('aff:',aff)
    aff_list = split_aff(aff)
    print('aff_list:',aff_list)
    
    simple_aff = aff_list[0]
    
    for m in constant.AFF_MATCH:
        if m in aff:
            simple_aff_list = [s for s in aff_list if m in s]
            simple_aff = simple_aff_list[0]
            break
        
    if len(simple_aff.split(' ')) > 11:
        m = re.search('\(.*?\)',aff)
        if m:
            simple_aff = simple_aff[m.start()+1:m.end()-1]
    
    print('simple_aff:',simple_aff)
    return simple_aff, True

def rearrange_info(fname):
    
    id2info = {}
       
    with open(join(constant.RAW_DIR,fname),'r',encoding='utf-8') as f:
        content = csv.reader(f)
        for roww in content:
            if roww[0] == 'ID':
                continue
            
            affiliation = roww[3]
            if len(affiliation)>0 :
                simple_affiliation, error = find_simple_affiliation(affiliation)
            else:
                simple_affiliation = ''
                    
            id2info[roww[0]] = {
                'name': roww[1],
                'id': roww[0],
                'name_zh': roww[2],
                'affiliation': roww[3],
                'simple_affiliation': simple_affiliation,
                'email_list': parse_emails(roww[4]),
                'h_index': roww[6],
                'keyword': roww[7],
                'language': roww[8],
                'relevance': roww[9],
                'cag': roww[10]
            }

    return id2info
    
if __name__ == '__main__':
    rearrange_info('test.csv')
    