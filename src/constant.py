# -*- coding: utf-8 -*-

import os
import re
from os.path import join, dirname, exists

def mkdir(dirpath):
    if not exists(dirpath):
        os.mkdir(dirpath)
        
#NAME_JOUR = 'Computational_Visual_Media'
#NAME_PRJ = 'Vol 2 No 4 2016'
#NAME_JOUR = 'Engineering'
#NAME_PRJ = '2017issue2'
#NAME_PRJ = 'new'
NAME_JOUR = 'JournalName'
NAME_PRJ = 'ProjectName'
                
        
SRC_DIR = dirname(__file__)
PRJ_DIR = dirname(SRC_DIR)
DAT_DIR = join(PRJ_DIR, 'data')
MOD_DIR = join(DAT_DIR, 'classifier')
PROXY_DIR = join(DAT_DIR, 'proxy')
CACHE_SNPTS_DIR = join(PRJ_DIR, 'cache')
CACHE_ZH_SNPTS_DIR = join(CACHE_SNPTS_DIR, 'Chinese')
CACHE_NOAFF_SNPTS_DIR = join(CACHE_SNPTS_DIR, 'Noaff')
DEBUG_DIR = join(PRJ_DIR,'debug')
ANALYSIS_DIR = join(DAT_DIR,'Analysis')
PEOPLE_INFO_DIR = join(DAT_DIR,'People_Info')
RAW_DIR = join(DAT_DIR, NAME_JOUR, NAME_PRJ, 'Original')
RESULT_DIR = join(DAT_DIR, NAME_JOUR, NAME_PRJ, 'Modified')

SVM_MOD_PATH = join(MOD_DIR, 'svm-model.pkl')
MLP_MOD_PATH = join(MOD_DIR, 'MLP.pkl')
IP_INFO_PATH = join(PROXY_DIR, 'ip_info.json')
RESULT_EXECL_PATH = join(RESULT_DIR, 'result.xlsx')
RESULT_CSV_PATH = join(RESULT_DIR, 'result.csv')
ERROR_PATH = join(DEBUG_DIR,'error.txt')
TEST_HTML_PATH = join(CACHE_SNPTS_DIR,'54082fdadabfae92b422cc66.html')

mkdir(CACHE_SNPTS_DIR)
mkdir(RESULT_DIR)
mkdir(DEBUG_DIR)

DELETE_LIST = ['email','admin','firstname','lastname','info']
FIELD = ['ID','Name','Aff','Email','Extracted','score','H-index','Keyword','Language','Relevance','Cag']
AFF_SEPARATOR = [';','|','-','?']
EMAIL_SEPARATOR = [',','/',';','、']
AFF_MATCH = ['Universi', 'enter','pital','nstitute','ollege','chool','partement', '大学', '院', '研究', '实验室']
ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

