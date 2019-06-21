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
from tools import my_analyzer
from tools import search
from tools import get_token
import string
import time
from nltk.corpus import stopwords 
import nltk
from nltk.corpus import wordnet as wn
from collections import Counter
import progressbar as pb
import spacy


def show(percent,width=50):
    if percent >= 100:
        percent=100

    show_str=('[%%-%ds]' %width) %(int(width * percent/100)*"#")
    print('\r%s %d%%' %(show_str,percent),end='')
    
def run(searcher, analyzer,command,en_nlp):

        

    original_command = command.replace('_',' ').replace('-',' ')
    stopwords = set(nltk.corpus.stopwords.words('english'))
    # title_set = {'over', 'whom','by', 'where', 'than', 'but', 'what', 'as', 'most', 'do', 'at', 'against', 'is', 'the', 'from', 'of', 'during', 'more', 'and', 'we', 'for', 'into', 'or', 'in', 'a', 'with', 'after', 'on', 'before', 'to', 'an', 'you'}
    # stopwords = stopwords - title_set
    
    command = unicodedata.normalize('NFC',command).replace('-',' ').replace("'s",'')
    exclude = set(string.punctuation)
    command = command.replace('-',' ')
    command = ''.join(ch for ch in command if ch not in exclude)
    
    # print ("Searching for:", command,'\n')

    # command_str without root verb
    root_verb = get_token.get_root_verb(command,en_nlp)
    content_query_list = [ch for ch in command.split(' ') if ch not in stopwords and ch != root_verb]
    # print('root verb is ',root_verb)
    """remove the root verb"""
    temp_list = []
    for elem in content_query_list:
        if elem != root_verb:
            temp_list.append(elem)
    temp_list = sorted(temp_list,reverse=True)
    content_query_list = temp_list        
    """remove the rb word"""
    
    content_query=' '.join(content_query_list)

    
    """get title query"""
    title_query = get_token.get_subject(command,en_nlp) 

    if not title_query:
        title_query = content_query
        
    title_query = title_query.lower()
    content_query = content_query.lower()

    query2 = QueryParser("contents", analyzer).parse(str(content_query))
    
        
    query3 = QueryParser("title", analyzer).parse(str(title_query))




    
    # print(query3)

    comman_tokens = query2.toString().replace(' ','').split('contents:')
    title_tokens = query3.toString().replace(' ','').split('title:')

    if title_tokens == ['']:
        query3 = query2
        title_tokens = comman_tokens
    
    title_tokens = sorted(list(filter(None, title_tokens)),reverse=True)
    comman_tokens = sorted(list(set(filter(None, comman_tokens))),reverse=True)
    LENTH_MATCH = len(comman_tokens)
    # print('\ntitle_tokens',title_tokens,'\n')
    # print('\ncomman_tokens',comman_tokens,'\n')
    # print('\noriginal_tokens',temp_list,'\n')
    # def get_token_str ():
    
    result_list = []

    # content
    scoreDocs3 = searcher.search(query3, 1000).scoreDocs
    # for scoreDoc3 in scoreDocs3:
    #     doc3 = searcher.doc(scoreDoc3.doc)
    #     # print(doc3.get("title"),doc3.get("contents"))

    month = ['april', 'august', 'decemb', 'februari', 'januari', 'juli', 'june', 'mai', 'march', 'novemb', 'octob', 'septemb']

    
    """ search full text"""
    score_result = Counter()
    re_search = {}
    have_searched_list = []
    
    
    match_score = Counter()
    match_length = {}
    title_query_list = title_query.split(' ')
    """ get primary """
    for scoreDoc3 in scoreDocs3:
                
        doc3 = searcher.doc(scoreDoc3.doc)
        match = 0
        title_content = doc3.get("title").lower()
        title_content_list = title_content.split(' ')
        if title_content not in match_score:

            for i in  title_query_list:
                if i in title_content_list:
                    match+=1
        
            match_score[title_content] = match
            match_length[title_content] = len(title_content.split(' '))
            
    primary_docs = []
    if not match_score:
        return []

    sorted_match_score= match_score.most_common()
    max_match = sorted_match_score[0][1]
    for i in sorted_match_score:
        if i[1]==max_match:
            primary_docs.append(i[0])

    min_length = 10
    
    for i in primary_docs:
        if len(i.split(' ')) <= min_length :
            min_length= len(i.split(' '))
    primary_list = []
    for i in primary_docs:
        if len(i.split(' ')) <= min_length+1:
            primary_list.append(i)
        
            
    content_id,content_realid,re_search={},{},{}
    """ 111 search based on title"""
    content_title ={}
    # print('primary===',primary_doc)
    for scoreDoc3 in scoreDocs3:  
            
        doc3 = searcher.doc(scoreDoc3.doc)
        doc_title = str(doc3.get("title"))
        
        if doc_title.lower() not in primary_list:
            continue
        doc3_id = doc3.get("doc_id")
        have_searched_list.append(doc3_id)
        # print(doc3.get('title'), doc3.get('contents'))
        match = 0
        
        doc_content = str(doc3.get("contents"))
        org = doc_content
        content_title[org] = doc_title
        doc_content = doc_title+' '+doc_content
        doc_content = ''.join(ch for ch in doc_content if ch not in exclude).lower()
        if not doc_content.replace(' ',''):
            continue

        doc_content_list = QueryParser("contents", analyzer).parse(doc_content).toString().replace(' ','').split('contents:')
        
        content_id[org] = doc_title
        content_realid[org] = doc3.get('real_doc')
        if root_verb:
            if root_verb not in stopwords and root_verb in doc_content:
                match+=1
                
        match_digit = 0
        match_month = 0
        for token in comman_tokens:
            
            
            digit_flag = False
            for i in token:
                if i.isdigit():
                    digit_flag = True
                    break
            if token in month:
                if match_month==1:
                    continue
                for m in month:
                    if m in doc_content_list:
                        match_month = 1
                        break
            if digit_flag:
                
                if match_digit==1:
                    continue
                for char in doc_content:
                    if char.isdigit():
                        match_digit=1
                        break
            elif token in doc_content_list:
                match+=1
            else:
                research_token = content_query_list[comman_tokens.index(token)]
                # this is original word in command
                if doc_content in re_search:
                    re_search[org].append(research_token)
                else:
                    re_search[org]=[research_token,]
        score_result[org]=match+match_digit+match_month
    

    if not score_result:
        return []

    sorted_list = score_result.most_common()
    most_match = sorted_list[0][1]
        
    
    if not score_result:
        return []
    sorted_list = score_result.most_common()
    most_match = sorted_list[0][1]
    # print('======== maxmatch',most_match)
    for i in sorted_list:
        if i[1]==most_match:
            # if i[0] not in result_list:
            result_list.append(i[0])
    
    result_list = result_list[:6]
    
    
    
    """ return """
    filtered_list = []
    result_lable_only = []
    resutl_lable_in_content = []
    for i in result_list:
        # print('===',content_realid)
        # a = i.strip(content_id[i])
        # if a[0]!=" ":
        #     a = ' '+a
        # filtered_str = content_realid[i] + a
        filtered_list.append(i)
        result_lable_only.append(content_realid[i])
        resutl_lable_in_content.append(content_realid[i]+' '+i)
    return resutl_lable_in_content


def run2(searcher, analyzer, command):
    command = unicodedata.normalize('NFC',command)
    # print ("Searching for:", command)
    hash_command = hashlib.md5(command.encode('utf-8')).hexdigest()
    query = QueryParser("doc_id", analyzer).parse(hash_command)
    scoreDocs = searcher.search(query, 1).scoreDocs
    # print ("%s total matching documents." % len(scoreDocs))
    for scoreDoc in scoreDocs:
        
        doc = searcher.doc(scoreDoc.doc)
        if hash_command == doc.get("doc_id"):
            return command+' '+doc.get("contents")
        else:
            print('error')
            print(command)
            print ('file:', doc.get("file"),'   ','doc_id:', doc.get("doc_id"),':     ', doc.get("contents"))
            return None
