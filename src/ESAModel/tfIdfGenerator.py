from __future__ import division
from math import log
from collections import defaultdict

class TfIdfGenerator:
    """Generates tf-idf values for the words in training data"""
    
    def __init__(self, tuplesList, wordSet):
        self.__wordSet = wordSet 
        self.__tuplesList = tuplesList
        self.__inverseTFIDF = defaultdict(int)
        
    def generate(self):
        """Generates tf-idf scores from document tuples"""

        documentCount = len(self.__tuplesList)
        for word in self.__wordSet:
            keys = []
            df, tf, idf, conceptId = 0, 0, 0, 1
            for wordSet, wordToCount in self.__tuplesList:
                if word in wordSet:
                    tf = wordToCount[word]
                    df = df + 1
                else:
                    tf = 0
                if tf != 0:
                    self.__inverseTFIDF[word, conceptId] = tf
                    keys.append((word, conceptId))                    
                conceptId = conceptId + 1
            if df == 0:
                idf = 0
            else:
                idf = log(documentCount/df)
            if keys != []:
                for key in keys:
                    self.__inverseTFIDF[key] = self.__inverseTFIDF[key]*idf
            print word
        print len(self.__wordSet), "words found in", documentCount, "documents."

    def getInverseTFIDF(self):
        """Fetch inverse tf-idf score stored in dictionary"""

        return self.__inverseTFIDF
