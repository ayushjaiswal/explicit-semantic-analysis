from preprocessingTools import Preprocessor
import xml.etree.ElementTree as ET
import os
import runnerConfig

class PreprocessorRunner:
    """Class to run the data preprocessing pipeline."""

    def __init__(self, shouldFilterStopWords=True, shouldFilterPunctuation=True, tokenType=Preprocessor.TokenType.raw):
        self.__shouldFilterStopWords = shouldFilterStopWords
        self.__shouldFilterPunctuation = shouldFilterPunctuation
        self.tokenType = tokenType

    def __getFullPath(self, path, filename):
        """Returns the full path of 'filename' after concatenating it to 'path'(the folder path)."""

        fullpath = path
        if path[-1] != '/':
            fullpath = fullpath + '/'
        fullpath = fullpath + filename
        return fullpath

    def __filterIllegal(self, text):
        """Removes & from text which can create problems if not escaped."""

        return text.replace('&', '')

    def __getTags(self, tagName):
        """Returns opening and closing tags for the tagName."""

        startTag = '<' + tagName + '>'
        endTag = '</' + tagName + '>'
        return startTag, endTag

    def __readXMLFile(self, path, filename, dataTag):
        """Reads XML file and returns contents."""

        fullpath = self.__getFullPath(path, filename)
        text = ""
        with open(fullpath, 'r') as f:
            text = f.read()
        opening, closing = self.__getTags(dataTag)
        startIdx = text.index(opening) + len(opening)
        endIdx = text.index(closing, startIdx)
        body = text[startIdx:endIdx]
        return body

    def __writeFile(self, path, filename, text):
        """Writes 'text' on file 'path/filename'."""

        fullpath = self.__getFullPath(path, filename)
        with open(fullpath, 'w') as f:
            f.write(text)

    def preprocessText(self, text):
        """Returns the list of tokens after preprocessing 'text'."""

        preprocessor = Preprocessor(self.__shouldFilterStopWords, self.__shouldFilterPunctuation)
        processedTokens = preprocessor.getTokens(text, self.tokenType)
        return processedTokens

    def preprocessFiles(self, rawDataPath, dataTag, preprocessedDataPath):
        """Preprocesses files in 'rawDataPath' folder, and saves them with the same file name in 'preprocessedDataPath'."""

        if os.path.exists(rawDataPath):
            if not os.path.exists(preprocessedDataPath):
                os.makedirs(preprocessedDataPath)
            rawFiles = os.listdir(rawDataPath)
            for rawFile in rawFiles:
                if rawFile[0] == '.':
                    continue
                rawText = self.__readXMLFile(rawDataPath, rawFile, dataTag)
                processedTokens = self.preprocessText(rawText)
                processedText = '\n'.join(processedTokens)
                self.__writeFile(preprocessedDataPath, rawFile, processedText)
                print "Processed file:", rawFile
            print "Preprocessing done!"
        else:
            "Source path does not exist!"

def main():
    preprocessor = PreprocessorRunner(runnerConfig.shouldFilterStopWords, runnerConfig.shouldFilterPunctuation, runnerConfig.tokenType)
    preprocessor.preprocessFiles(runnerConfig.rawDataPath, runnerConfig.dataTag, runnerConfig.preprocessedDataPath)

if __name__ == '__main__':
    main()
