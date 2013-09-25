# Saves the index files for aricles and topics 
import re
from os import listdir
from os.path import isfile, join

dataPath = "../../../data/Medline/"
topicFolder = 'Topics'
articleFolder = 'Articles'

class MedlineIndexer:
    """Indexer for Medline articles and topics."""

    def __init__(self, dataPath, topicFolder, articleFolder):
        self.__topicPath = dataPath + topicFolder + '/'
        self.__articlePath = dataPath + articleFolder + '/'
        self.__indexFilePath = dataPath
        self.__topicFolder = topicFolder
        self.__articleFolder = articleFolder

    def __getRow(self, fileName, folderName):
        """Return row for CSV."""
        
        row = fileName + ', ' + folderName + '/' + fileName + '\n'
        return row

    def indexFiles(self):
        """Indexes topics and articles collected from Medline."""

        topicFiles = [fileName for fileName in listdir(self.__topicPath) if isfile(self.__topicPath + fileName) and fileName[:-1] != '~']
        articleFiles = [fileName for fileName in listdir(self.__articlePath) if isfile(self.__articlePath + fileName) and fileName[:-1] != '~']
        with open(self.__indexFilePath + 'TopicIndex', 'w') as f:
            for fileName in topicFiles:
                f.write(self.__getRow(fileName, self.__topicFolder))

        with open(self.__indexFilePath + 'ArticleIndex', 'w') as f:
            for fileName in articleFiles:
                f.write(self.__getRow(fileName, self.__articleFolder))

def main():
    """To run indexing as a standalone program."""

    print "Indexing files..."
    indexer = MedlineIndexer(dataPath, topicFolder, articleFolder)
    indexer.indexFiles()
    print "Done."


if __name__ == '__main__':
    main()