from __future__ import division
from math import log
from collections import defaultdict

class TfIdfGenerator:
    """Generates tf-idf values for the words in training data"""
        
    def __init__(self, documentList):
        self.__documentList = documentList
        self.__numberOfDocuments = len(self.__documentList)
        self.__TFIDF_InvertedIndex = defaultdict(lambda: defaultdict(int))
        self.__wordSet = set([])
        self.generate()
                   
    def __getIDF(self, df):
        """Returns IDF value for a word."""
        
        return log(self.__numberOfDocuments / df)
        
    def generate(self):
        """Generates tf-idf scores from document tuples."""

        TF_InvertedIndex = defaultdict(lambda: defaultdict(int))
        DF = defaultdict(int)
        #Indexing for documents starts with 1
        conceptId = 1
        
        for document in self.__documentList:
            wordsInCurrentDocument = set([])
            text = ""
            with open(document) as f:
                text = f.read()
            words = text.splitlines()
            for word in words:
                TF_InvertedIndex[word][conceptId] = TF_InvertedIndex[word][conceptId] + 1
                wordsInCurrentDocument.add(word)        
            for word in wordsInCurrentDocument:
                DF[word] = DF[word] + 1
            self.__wordSet = self.__wordSet.union(wordsInCurrentDocument)
            conceptId = conceptId + 1
        
        for word in self.__wordSet:
            if DF[word] == 0:
                self.__TFIDF_InvertedIndex[word][ConceptId] = 0
            else:
                for conceptId in TF_InvertedIndex[word].keys():
                    self.__TFIDF_InvertedIndex[word][conceptId] = TF_InvertedIndex[word][conceptId] * self.__getIDF(DF[word])
        print len(self.__wordSet), "words found in", self.__numberOfDocuments, "documents."
        
    def get_TFIDF_InvertedIndex(self):
        """Fetch inverted indexed of TF-IDF values."""

        return self.__TFIDF_InvertedIndex

    def getWordSet(self):
        """Returns the set of all words in all documents."""

        return self.__wordSet

    def getNumberOfDocuments(self):
        """Returns the set of all documents."""

        return self.__numberOfDocuments