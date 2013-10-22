from __future__ import division
from math import log
from collections import defaultdict

class TfIdfGenerator:
    """Generates tf-idf values for the words in training data"""
        
    def __init__(self, documentList):
        self.__documentList = documentList
        self.__TFIDF_InvertedIndex = defaultdict(lambda: defaultdict(int))
                   
    def __getIDF(self, df, numberOfDocuments):
        """returns idf value for a word"""
        
        return log(numberOfDocuments/df)
        
    def generate(self):
        """Generates tf-idf scores from document tuples"""

        TF_InvertedIndex = defaultdict(lambda: defaultdict(int))
        DF = defaultdict(int)
        IDF = defaultdict(int)
        wordSet = set([])
        numberOfDocuments = len(self.__documentList)
        #Indexing for documents starts with 1
        conceptId = 1
        
        for document in self.__documentList:
            wordsInCurrentDocument = set([])
            with open(document) as f:
                text = f.read()
            words = text.splitlines()
            for word in words:
                TF_InvertedIndex[word][conceptId] += 1
                wordsInCurrentDocument.add(word)        
            wordSet = wordSet.union(wordsInCurrentDocument)
            for word in wordsInCurrentDocument:
                DF[word] += 1
            conceptId += 1
        
        for word in wordSet:
            if DF[word] == 0:
                self.__TFIDF_InvertedIndex[word][ConceptId] = 0
            else:
                for ConceptId in TF_InvertedIndex[word].keys():
                    self.__TFIDF_InvertedIndex[word][ConceptId] = TF_InvertedIndex[word][ConceptId] * self.__getIDF(DF[word], numberOfDocuments)
        print len(wordSet), "words found in", numberOfDocuments, "documents."
        
    def get_TFIDF_InvertedIndex(self):
        """Fetch inverted indexed TF-IDF stored in dictionary"""

        return self.__TFIDF_InvertedIndex
