# Saves the index files for aricles and topics 
import re
from os import listdir
from os.path import isfile, join, exists

dataPath = "../../../data/raw/Medline/"
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

        if exists(self.__topicPath):
            topicList = listdir(self.__topicPath)
            topicFiles = [fileName for fileName in topicList if isfile(self.__topicPath + fileName) and fileName[:-1] != '~']
            with open(self.__indexFilePath + 'TopicIndex', 'w') as f:
                for fileName in topicFiles:
                    f.write(self.__getRow(fileName, self.__topicFolder))
        else:
            print "Topics folder doesn't exist."

        if exists(self.__articlePath):
            articleList = listdir(self.__articlePath)
            articleFiles = [fileName for fileName in articleList if isfile(self.__articlePath + fileName) and fileName[:-1] != '~']
            with open(self.__indexFilePath + 'ArticleIndex', 'w') as f:
                for fileName in articleFiles:
                    f.write(self.__getRow(fileName, self.__articleFolder))
        else:
            print "Articles folder doesn't exist."

def main():
    """To run indexing as a standalone program."""

    print "Indexing files..."
    indexer = MedlineIndexer(dataPath, topicFolder, articleFolder)
    indexer.indexFiles()
    print "Done."


if __name__ == '__main__':
    main()