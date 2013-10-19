class Tuples:
    """Generates the tuples to store the values associated
    in calculation of tf-idf score"""
    
    def __init__(self, documentList):
        self.__documentList = documentList
        self.__tuplesList = []

    def generateTuple(self, documentText):
        """Generate the tuple: unique_words, count_of_words 
        for a specific document"""
        
        wordSet = set([])
        wordToWordCount = {}
        listOfWords = documentText.splitlines()
        for word in listOfWords:
            if word not in wordSet:
                wordToWordCount[word] = listOfWords.count(word)
                wordSet.add(word)
        return wordSet, wordToWordCount

    def process(self):
        """Process the list containing the documents path to
        generate the tuples"""
        
        for document in self.__documentList:
            with open(document) as f:
                text = f.read()
            self.__tuplesList.append(self.generateTuple(text))
        
    def getTuplesList(self):
        """Fetch the generated list of tuples"""
        
        return self.__tuplesList
        
    def getWordSet(self):
        """Fetch the set of unique words from the data"""
        
        return set([words for wordSet, wordToCount in self.__tuplesList for words in wordSet])
