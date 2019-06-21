"""
This script create indexes for wiki files
The wiki files should exist in folder 'wiki-pages-text' under current path
THe output index file generate in folder 'IndexFiles.index' under current path
"""

import lucene
import hashlib

import sys, os, threading, time	
from datetime import datetime		
from java.nio.file import Paths	
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory

import unicodedata
from tools import get_token
from tools import my_analyzer
from tools import search
import progressbar as pb

"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(Paths.get(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 30000000)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print ('\ncommit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print ('done')

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(True)
        t1.setIndexOptions(IndexOptions.DOCS)

        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(False)
        t2.setIndexOptions(IndexOptions.DOCS)

        cnt = 0
        total = len(os.listdir(root))
        
        slot = total//100

        error_num = 0
        widgets = ['Total {} files: '.format(total), pb.Percentage(), ' ', 
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
        timer = pb.ProgressBar(widgets=widgets, maxval=total).start()   
        
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if filename.startswith('.'):
                    continue
                if not filename.endswith('.txt'):
                    continue
                # print ("adding", filename)
                try:
                    
                    path = os.path.join(root, filename)
                    file = open(path)
                    line_contents = file.readline()
                    line_contents = unicodedata.normalize('NFC',line_contents)
                    while line_contents:
                        
                    # file.close()
                        doc_split = line_contents.split(' ',2)

                        if doc_split[1].isdigit():

                            real_doc = doc_split[0]+' '+doc_split[1]
                            
                            title = doc_split[0].replace('_',' ').replace('-LRB-','').replace('-RRB-','').replace('-COLON-','').replace('-',' ').replace('_',' ')

                            doc_id = doc_split[0]+" "+doc_split[1]

                            doc_id =  hashlib.md5(doc_id.encode('utf-8')).hexdigest()
                            
                            
                            doc = Document()
                            doc.add(Field("doc_id", doc_id, t1))
                            doc.add(Field("real_doc",real_doc, t2))
                            doc.add(Field("title", title, t1))
                            if len(line_contents) > 0:
                                content_all = doc_split[2].replace('-LRB-','').replace('-RRB-','').replace('-COLON-','').replace('-',' ').replace('_',' ')
                                doc.add(Field("contents", content_all, t1))


                            else:
                                print ("warning: no content in %s" % filename)
                            writer.addDocument(doc)

                        else: 
                            error_num+=1

                        line_contents = str(file.readline())

                    cnt+=1
                    # if cnt%slot==0 or cnt ==total:
                    #     recv_per=int(100*cnt/total)
                    #     show(recv_per)
                    timer.update(cnt)
                    
                except Exception as e:
                    print ("\nFailed in indexDocs: ",filename," \nerror: ",e)
        print('\nBroken lines: ',error_num)

def show(percent,width=50):
    if percent >= 100:
        percent=100

    show_str=('[%%-%ds]' %width) %(int(width * percent/100)*"#")
    print('\r%s %d%%' %(show_str,percent),end='')

if __name__ == '__main__':
    
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    TEST_ALL = os.path.join(base_dir, "wiki-pages-text")
    INDEX_DIR = os.path.join(base_dir, "IndexFiles.index")

    isExist = os.path.isdir(INDEX_DIR)
    if isExist:
        for file in os.listdir(INDEX_DIR):
            os.remove(os.path.join(INDEX_DIR,file))


    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        content_analyzer = my_analyzer.get_analyzer()
        IndexFiles(TEST_ALL, os.path.join(base_dir, INDEX_DIR),
                    content_analyzer)
        end = datetime.now()
        print (end - start)
    except:
        print( "Failed: ")