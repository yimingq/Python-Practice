"""
This file is used to generate the 3_class_train_set.json file.
The input file 'train.json' should be in directory

1. It modify the original train.json file by adding the evidences
    for 'NOT ENOUGH INFO' label.
2. It exeact the evidence content based on sentence id

The output file will be in current directory
"""

INDEX_DIR = "IndexFiles.index"
import sys, os, lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import FuzzyQuery
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.index import Term
import hashlib
import unicodedata
import json
import string
import time
from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet as wn
from collections import Counter
import progressbar as pb
import spacy
from tools import get_token
from tools import my_analyzer
from tools import search


base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
INPUT_FILE = os.path.join(base_dir, 'train.json')
OUTPUT_FILE = os.path.join(base_dir, '3_class_train_set.json')
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print ('lucene', lucene.VERSION)
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
searcher = IndexSearcher(DirectoryReader.open(directory))
# analyzer = StandardAnalyzer()
analyzer = my_analyzer.get_analyzer()

""""""
en_nlp = spacy.load('en_core_web_sm')
file = json.loads(open(INPUT_FILE,encoding="utf-8").read())
start = time.time()
count = 0
total = len(file)
percent = len(file)//100
print(total)
print('start converting')
# progress bar
widgets = ['Total {} claims: '.format(total), pb.Percentage(), ' ',
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
timer = pb.ProgressBar(widgets=widgets, maxval=total).start()

for key, value in file.items():
    count+=1

    if value['label']=='NOT ENOUGH INFO':
        claim = value['claim']
        result_list = search.run(searcher, analyzer,claim,en_nlp)
        value['evidence']=result_list
    else:
        evidences = value['evidence']
        new_evidences=[]
        if len(evidences)>0:
            for sublist in evidences:
                query = str(sublist[0])+" "+str(sublist[1])
                new_evidences.append(search.run2(searcher, analyzer,query))

            value['evidence'] = new_evidences
            # print(new_evidences)
    timer.update(count)
    # if count%percent ==0 or count==total:
    #     recv_per=int(100*count/total)
    #     show(recv_per,width=100)


print("\ntime cost: "+ str(time.time()-start))
with open(OUTPUT_FILE ,'w',encoding='utf-8') as filename:
    json.dump(file, filename,indent=4)
print('output file: {}\n'.format(OUTPUT_FILE))



del searcher
