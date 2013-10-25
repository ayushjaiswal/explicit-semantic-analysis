from tfIdfGenerator import TfIdfGenerator
from objectDumperAndLoader import ObjectDumperAndLoader
from ESA_util import ESADumpDS
import os
import runnerConfig

class ESARunner:
    """Runner for ESA model"""
    
    def __init__(self, folderPath, indexFilePath, dumperDestination, dumpFileName):
        if folderPath[-1] != '/':
            folderPath  =  folderPath + '/'
        if dumperDestination[-1] != '/':
            dumperDestination  =  dumperDestination + '/'
        self.__dumperDestination = dumperDestination
        if not os.path.exists(self.__dumperDestination):
            os.makedirs(self.__dumperDestination)
        self.__dumpFileName = dumpFileName
        self.__folderPath = folderPath
        self.__indexFilePath = indexFilePath
        
        
    def run(self):
        """Generates inverse tf-idf score and saves at specified location"""
         
        text = ""
        listOfFiles = []
        with open(self.__indexFilePath) as f:
            text = f.read().splitlines()
            listOfFiles = [name.split('||||')[0] for name in text]
        
        documentList = [self.__folderPath + fileName for fileName in listOfFiles]

        print 'Generating tf-idf scores...'
        tfIdfGeneratorObj = TfIdfGenerator(documentList)
        print 'TF-IDF scores generated.\n'
        TFIDF_InvertedIndex = tfIdfGeneratorObj.get_TFIDF_InvertedIndex()
        wordSet = tfIdfGeneratorObj.getWordSet()
        numberOfDocuments = tfIdfGeneratorObj.getNumberOfDocuments()

        ESADump = ESADumpDS(wordSet, numberOfDocuments, TFIDF_InvertedIndex)

        print 'Dumping object..'
        objectDumperAndLoader = ObjectDumperAndLoader()
        objectDumperAndLoader.dump(ESADump, self.__dumperDestination, self.__dumpFileName)
        print 'TFIDF-inverted-index dump saved at:', self.__dumperDestination + self.__dumpFileName

if __name__ == "__main__":
    runner = ESARunner(runnerConfig.srcFolder, runnerConfig.indexFilePath, runnerConfig.dumperDestination, runnerConfig.dumpFileName)
    runner.run()
