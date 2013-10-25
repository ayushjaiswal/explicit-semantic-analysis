class ESADumpDS:
    """A data structure to hold the set of words, number of concepts (numbered 1-n), and the TFIDF inverted index."""

    def __init__(self, wordSet, numberOfConcepts, TFIDF_InvertedIndex):
        self.__wordSet = wordSet
        self.__numberOfConcepts = numberOfConcepts
        self.__TFIDF_InvertedIndex = TFIDF_InvertedIndex

    def get_TFIDF_InvertedIndex(self):
        """Fetch inverted indexed of TF-IDF values."""

        return self.__TFIDF_InvertedIndex

    def getWordSet(self):
        """Returns the set of all words in all documents."""

        return self.__wordSet

    def getNumberOfConcepts(self):
        """Returns the set of all concepts."""

        return self.__numberOfConcepts