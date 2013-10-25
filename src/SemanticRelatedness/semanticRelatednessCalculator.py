import sys
import os
sys.path.insert(0, os.path.abspath(".."))
from Preprocessing.preprocessingTools import Preprocessor
from collections import defaultdict
import math

class SemanticRelatednessCalculatorESA:
    """Calculates the semantic relatedness of text fragments using the ESA technique."""

    def __init__(self, ESAConceptsInfo, tokenType=Preprocessor.TokenType.raw, shouldFilterStopWords=True, shouldFilterPunctuation=True):
        self.__Concepts_TFIDF_InvertedIndex = ESAConceptsInfo.get_TFIDF_InvertedIndex()
        self.__numberOfConcepts = ESAConceptsInfo.getNumberOfConcepts()
        self.__tokenSet = ESAConceptsInfo.getWordSet()
        self.__tokenType = tokenType
        self.__shouldFilterPunctuation = shouldFilterPunctuation
        self.__shouldFilterStopWords = shouldFilterStopWords

    def __getTokenFrequencies(self, tokenList):
        """Get the frequencies of all tokens in tokenList."""

        wordFrequencies = defaultdict(int)
        for token in tokenList:
            wordFrequencies[token] = wordFrequencies[token] + 1
        return wordFrequencies

    def __getWeightedVectorOfConcepts(self, tokenList):
        """Returns the weighted vector of concepts for the words in tokenList."""

        tf = self.__getTokenFrequencies(tokenList)
        weightedVectorOfConcepts = [0 for i in range(self.__numberOfConcepts)]
        for concept in range(1, self.__numberOfConcepts + 1):
            for word in tokenList:
                weightedVectorOfConcepts[concept - 1] = weightedVectorOfConcepts[concept - 1] + (self.__Concepts_TFIDF_InvertedIndex[word][concept] * tf[word])
        return weightedVectorOfConcepts

    def __getNorm(self, vector):
        """Returns the norm of vector."""

        return math.sqrt(sum([vector[i] ** 2 for i in range(len(vector))]))

    def __getDotProduct(self, vector1, vector2):
        """Returns the dot product of vector1 and vector2."""

        return sum([vector1[i] * vector2[i] for i in range(len(vector1))])

    def __getCosineSimilarity(self, vector1, vector2):
        """Returns the cosine similarity score for vector1 and vector2."""

        dotProduct = self.__getDotProduct(vector1, vector2)
        vector1_norm = self.__getNorm(vector1)
        vector2_norm = self.__getNorm(vector2)
        cosineSimilarity = dotProduct / (vector1_norm * vector2_norm)
        return cosineSimilarity

    def getSemanticRelatednessScore(self, text1, text2):
        """Calculates the semantic relatedness of text1 and text2, and returns the final score."""

        preprocessor1 = Preprocessor(text1, self.__shouldFilterStopWords, self.__shouldFilterPunctuation)
        tokens1 = preprocessor1.getTokens(self.__tokenType)
        preprocessor2 = Preprocessor(text2, self.__shouldFilterStopWords, self.__shouldFilterPunctuation)
        tokens2 = preprocessor2.getTokens(self.__tokenType)
        
        weightedVectorOfConcepts1 = self.__getWeightedVectorOfConcepts(tokens1)
        weightedVectorOfConcepts2 = self.__getWeightedVectorOfConcepts(tokens2)

        ESA_score = self.__getCosineSimilarity(weightedVectorOfConcepts1, weightedVectorOfConcepts2)
        return ESA_score