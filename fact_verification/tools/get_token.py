import spacy
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import spacy
import string
def get_subject(text,en_nlp):
    text = text.replace("'s","")

    doc = en_nlp(text)
    # sentence = next(doc.sents) 
    
    
    # find root word
    root_word = get_root_verb(text,en_nlp)
    
    # if root word is none
    if not root_word:
        return None
    
    front = ''
    for word in doc:
        if str(word)==root_word:
            break
        front+= str(word)+' '  

    subject = ''    

    for chunk in doc.noun_chunks:
        
        if  (chunk.root.dep_=='nsubj'or  chunk.root.dep_=='nsubjpass') and chunk.root.head.text== root_word :
            subject = chunk.text
        # print(chunk.text, chunk.root.text, chunk.root.dep_,
        #     chunk.root.head.text)
    if not subject:
        return get_subject2(doc)
    # find subject position
    infront = False
    for chunk in doc.noun_chunks:
        if chunk.text in front:
            infront = True
    # find subject phrase          
    result = ''
    for chunk in doc.noun_chunks:
        if infront:
            if chunk.text in front:
                result+= chunk.text+' '
        else:
            if chunk.text not in front:
                result+= chunk.text+' '
    return result

def get_root_verb(text,en_nlp):
    temp_text = ''
    for i in text:
        if i !='-':
            temp_text+=i
    text = temp_text
    # en_nlp = spacy.load('en_core_web_sm')
    doc = en_nlp(text)
    result= []
    for word in doc:
        if word.dep_=='ROOT' and word.pos_=='VERB':
            result.append(str(word))
    if len(result)==1:
        return result[0]
    return None
def judge_rb(word):
    try:
        if pos_tag([word])=='RB':
            return True
    except:
        return False
def judge_nn(word):
    try:
        if pos_tag([word])=='NN':
            return True
    except:
        return False

print()

def get_lemma(text, en_nlp):

    doc = en_nlp(text)
    result= ''
    for token in doc:
        result+=token.lemma_+' '
    return result


def get_subject2(doc):
    result_set = set()
    dep_list = []
    sent_list = []
    subject,root_verb = '', ''
    for token in doc:
        sent_list.append(token.text)
        dep_list.append(token.dep_)

    for token in doc:
        if token.dep_ == 'nsubj':
            subject = token.text
            break
    for token in doc:
        if token.dep_ == 'ROOT':
            root_verb = token.text
            break
    
    if not root_verb or not subject:
        return None
    result_set.add(subject)
    subject_index=sent_list.index(subject)

    root_index= sent_list.index(root_verb)

    nn = ['PROPN','NOUN','NUM']
    if subject_index< root_index:
        for index in range(root_index):
            if dep_list[index] in nn:
                result_set.add(sent_list[index])
        return ' '.join(list(result_set))
    else:
        for index in range(root_index,len(sent_list)):
            if dep_list[index] in nn:
                result_set.add(sent_list[index])
        return ' '.join(list(result_set))
    
def get_date(en_nlp, command):
    
    doc = en_nlp(command)
    month = ['January','February','March','April','May','June','July','August','September','October','November','December']
    for ent in doc.ents:
        judge_right= True
        if ent.label_=='DATE':
            text = ent.text
            word_list = text.split(' ')
            
            for word in word_list:
                if word not in month or not word.isdigit():
                    judge_right = False
                    break
        if judge_right :
            return ent.text
    return None
        
def get_money(en_nlp, command):
        
    doc = en_nlp(command)

    for ent in doc.ents:
        if ent.label_=='MONEY':
            return ent.text
    return None
        
# import spacy
# en_nlp = spacy.load('en_core_web_sm')
# a = "Comedy is something performed by Fred Armisen"
# print(get_subject(a,en_nlp))
