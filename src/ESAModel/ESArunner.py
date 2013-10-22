from tfIdfGenerator import TfIdfGenerator
from objectDumperAndLoader import ObjectDumperAndLoader
import os

srcFolder = "../../data/Medline/preprocessed/Topics"
indexFilePath = "../../data/Medline/TopicIndex"
dumperDestination = "../../data/ESAModel/"
dumperFileName = "TFIDF_InvertedIndex.pkl"

class Runner:
    """Runner for ESA model"""
    
    def __init__(self, folderPath, indexFilePath, dumperDestination, dumperFileName):
        if folderPath[:-1] != '/':
            folderPath  =  folderPath + '/'
        if dumperDestination[:-1] != '/':
            dumperDestination  =  dumperDestination + '/'
        self.__dumperDestination = dumperDestination
        if not os.path.exists(self.__dumperDestination):
            os.makedirs(self.__dumperDestination)
        self.__dumperFileName = dumperFileName
        self.__folderPath = folderPath
        self.__indexFilePath = indexFilePath
        
        
    def run(self):
        """Generates inverse tf-idf score and saves at specified location"""
         
        with open(self.__indexFilePath) as f:
            text = f.read().splitlines()
            listOfFiles = [name.split('||||')[0] for name in text]
        
        documentList = [self.__folderPath + fileName for fileName in listOfFiles]

        print 'Generating tf-idf scores.'
        tfIdfGeneratorObj = TfIdfGenerator(documentList)
        tfIdfGeneratorObj.generate()
        print 'tf-idf scores generated.\n'
        tfidf = tfIdfGeneratorObj.get_TFIDF_InvertedIndex()

        print 'Dumping object..'
        objectDumperAndLoader = ObjectDumperAndLoader()
        objectDumperAndLoader.dump(tfidf, self.__dumperDestination, self.__dumperFileName)
        print 'object saved at', self.__dumperDestination+self.__dumperFileName

if __name__ == "__main__":
    runner = Runner(srcFolder, indexFilePath, dumperDestination, dumperFileName)
    runner.run()
