import sys, os, lucene
from datetime import datetime
# from IndexFiles import IndexFiles

from org.apache.lucene.analysis import LowerCaseFilter, StopFilter
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.analysis.standard import StandardTokenizer, StandardFilter
from org.apache.pylucene.analysis import PythonAnalyzer
from org.apache.lucene.analysis import CachingTokenFilter

from nltk.stem import PorterStemmer 
from nltk.stem import WordNetLemmatizer


class PorterStemmerAnalyzer(PythonAnalyzer):
    def createComponents(self, fieldName):


        source = StandardTokenizer()
        filter = StandardFilter(source)
        filter = LowerCaseFilter(filter)
        filter = PorterStemFilter(filter)
        # filter = CachingTokenFilter(filter)
        filter = StopFilter(filter, StopAnalyzer.ENGLISH_STOP_WORDS_SET)


        return self.TokenStreamComponents(source, filter)

    def initReader(self, fieldName, reader):

        return reader

class TitleAnalyzer(PythonAnalyzer):
    def createComponents(self, fieldName):


        source = StandardTokenizer()
        filter = StandardFilter(source)
        filter = LowerCaseFilter(filter)
        # filter = CachingTokenFilter(filter)

        return self.TokenStreamComponents(source, filter)

    def initReader(self, fieldName, reader):

        return reader

def get_analyzer():
    return PorterStemmerAnalyzer()

def title_analyzer():
    return TitleAnalyzer()