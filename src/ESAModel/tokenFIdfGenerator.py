from __future__ import division
from math import log
from collections import defaultdict
from nltk.corpus import wordnet as wn

class TokenFIdfGenerator:
    """Generates token_frequency-idf values for the tokens in training data"""
        
    class TermType():
        """Enum for token types"""
        term = 0
        synset = 1

    def __init__(self, documentList, termType):
        self.__documentList = documentList
        self.__termType = termType
        self.__numberOfDocuments = len(self.__documentList)
        self.__TokenFIDF_InvertedIndex = defaultdict(lambda: defaultdict(int))
        self.__tokenSet = set([])
        self.generate()
                   
    def __getIDF(self, df):
        """Returns IDF value for a token."""
        
        return log(self.__numberOfDocuments / df)
        
    def __getSynsetList(self, words):
        """Returns a list of synsets by expanding each word in words to its synsets."""

        synsetList = []
        for word in words:
            synsetList = synsetList + [synset.name for synset in wn.synsets(word)]
        return synsetList

    def generate(self):
        """Generates token_frequency-idf scores from document tuples."""

        TokenF_InvertedIndex = defaultdict(lambda: defaultdict(int))
        DF = defaultdict(int)
        #Indexing for documents starts with 1
        conceptId = 1
        
        for document in self.__documentList:
            tokensInCurrentDocument = set([])
            text = ""
            with open(document) as f:
                text = f.read()
            words = text.splitlines()
            tokens = []
            if self.__termType == TokenFIdfGenerator.TermType.synset:
                tokens = self.__getSynsetList(words)
            else:
                tokens = words
            for token in tokens:
                TokenF_InvertedIndex[token][conceptId] = TokenF_InvertedIndex[token][conceptId] + 1
                tokensInCurrentDocument.add(token)        
            for token in tokensInCurrentDocument:
                DF[token] = DF[token] + 1
            self.__tokenSet = self.__tokenSet.union(tokensInCurrentDocument)
            conceptId = conceptId + 1
        
        for token in self.__tokenSet:
            if DF[token] == 0:
                self.__TokenFIDF_InvertedIndex[token][ConceptId] = 0
            else:
                for conceptId in TokenF_InvertedIndex[token].keys():
                    if self.__TokenFIDF_InvertedIndex[token][conceptId] > 0:
                        self.__TokenFIDF_InvertedIndex[token][conceptId] = 1 + log(self.__TokenFIDF_InvertedIndex[token][conceptId])  # sublinear scaling
                    self.__TokenFIDF_InvertedIndex[token][conceptId] = TokenF_InvertedIndex[token][conceptId] * self.__getIDF(DF[token])
        print len(self.__tokenSet), "tokens found in", self.__numberOfDocuments, "documents."
        
    def get_TokenFIDF_InvertedIndex(self):
        """Fetch inverted indexed of token_frequency-IDF values."""

        return self.__TokenFIDF_InvertedIndex

    def getTokenSet(self):
        """Returns the set of all tokens in all documents."""

        return self.__tokenSet

    def getNumberOfDocuments(self):
        """Returns the set of all documents."""

        return self.__numberOfDocuments