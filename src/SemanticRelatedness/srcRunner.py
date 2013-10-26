import sys
import os
sys.path.insert(0, os.path.abspath(".."))
import Preprocessing.runnerConfig
from semanticRelatednessCalculator import SemanticRelatednessCalculatorESA

class SRC_Runner:
    """Runner for semantic relatedness calculation using ESA."""

    def __init__(self, ESAConceptsInfo): 
        self.__ESAConceptsInfo = ESAConceptsInfo
        self.__shouldFilterStopWords = Preprocessing.runnerConfig.shouldFilterStopWords
        self.__shouldFilterPunctuation = Preprocessing.runnerConfig.shouldFilterPunctuation
        self.__tokenType = Preprocessing.runnerConfig.tokenType
        self.__semanticRelatednessCalculator = SemanticRelatednessCalculatorESA(self.__ESAConceptsInfo, self.__tokenType, self.__shouldFilterStopWords, self.__shouldFilterPunctuation)

    def __readFile(self, filePath):
        """Reads a text file and returns the text."""

        text = ""
        with open(filePath) as f:
            text = f.read()
        return text

    def run(self):
        """Run the semantic relatedness calculator."""

        file1 = raw_input("Enter absolute path of the first document: ")
        file2 = raw_input("Enter absolute path of the second document: ")
        text1 = self.__readFile(file1)
        text2 = self.__readFile(file2)
        similarityScore = self.__semanticRelatednessCalculator.getSemanticRelatednessScore(text1, text2)
        print "The similarity score (0-1) is:", similarityScore