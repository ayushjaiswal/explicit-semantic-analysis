import sys
import os
sys.path.insert(0, os.path.abspath(".."))
from tokenFIdfGenerator import TokenFIdfGenerator
from objectDumperAndLoader import ObjectDumperAndLoader
from ESA_util import ESADumpDS
import os
import runnerConfig

class ESARunner:
    """Runner for ESA model"""
    
    def __init__(self, folderPath, indexFilePath, dumperDestination, dumpFileName, termType):
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
        self.__termType = termType
        
        
    def run(self):
        """Generates inverse token_frequency-idf score and saves at specified location"""
         
        text = ""
        listOfFiles = []
        with open(self.__indexFilePath) as f:
            text = f.read().splitlines()
            listOfFiles = [name.split('||||')[0] for name in text]
        
        documentList = [self.__folderPath + fileName for fileName in listOfFiles]

        print 'Generating token_frequency-idf scores...'
        tokenFIdfGeneratorObj = TokenFIdfGenerator(documentList, self.__termType)
        print 'TokenF-IDF scores generated.\n'
        TokenFIDF_InvertedIndex = tokenFIdfGeneratorObj.get_TokenFIDF_InvertedIndex()
        tokenSet = tokenFIdfGeneratorObj.getTokenSet()
        numberOfDocuments = tokenFIdfGeneratorObj.getNumberOfDocuments()

        ESADump = ESADumpDS(tokenSet, numberOfDocuments, TokenFIDF_InvertedIndex)

        print 'Dumping object..'
        objectDumperAndLoader = ObjectDumperAndLoader()
        objectDumperAndLoader.dump(ESADump, self.__dumperDestination, self.__dumpFileName)
        print 'TokenFIDF-inverted-index dump saved at:', self.__dumperDestination + self.__dumpFileName

if __name__ == "__main__":
    runner = ESARunner(runnerConfig.srcFolder, runnerConfig.indexFilePath, runnerConfig.dumperDestination, runnerConfig.dumpFileName, runnerConfig.termType)
    runner.run()
