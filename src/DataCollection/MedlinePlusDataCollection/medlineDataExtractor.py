import workerpool
import re
import os
import urllib2
from bs4 import BeautifulSoup

class MedlineDataExtractor(workerpool.Job):
    """Fetches the data from the given link and save"""
    
    def __init__(self, url, savePath, isArticle=False):
        self.__url = url
        self.__savePath = savePath
        self.__isArticle = isArticle
        if not os.path.exists(self.__savePath):
            os.makedirs(self.__savePath)

    def __fetchHtml(self):
        response = urllib2.urlopen(self.__url)
        html_doc = response.read()
        response.close()
        return html_doc

    def __getTags(self, name):
        """Returns opening and closing tags given tag name."""

        openTag = '<' + name + '>'
        closeTag = '</' + name + '>'
        return openTag, closeTag

    def __getFileName(self, title):
        """Returns file name based on title."""

        fileName = title.encode('utf-8')
        fileName = re.sub(' +', ' ', fileName)
        fileName = re.sub('_+', ' ', fileName)
        fileName = re.sub('/+', ' ', fileName)
        return fileName

    def __textToXML(self, dictionary, root):
        """Convert raw text to XML given dictionary."""

        contents = '<?xml version="1.0" encoding="UTF-8"?>\n'
        openRootTag, closeRootTag = self.__getTags(root)
        contents = contents + openRootTag + '\n'
        for item in dictionary.keys():
            openTag, closeTag = self.__getTags(item)
            contents = contents + openTag + dictionary[item] + closeTag + '\n'
        contents = contents + closeRootTag
        return contents

    def __saveTopic(self, soupObj):
        """Fetches and saves data from different topics"""
        
        title = soupObj.find("h1", {"id":"tp_title"})
        alsoKnown = soupObj.find("div", {"id":"ht_alsoknown"})
        body = soupObj.find("div", {"id":"tpsummary"})
        if not title is None and not body is None:
            titleText = title.text.strip()
            fileName = self.__getFileName(titleText)
            bodyText = body.text
            fileContents = {}
            fileContents['title'] = titleText
            if not alsoKnown is None:
                fileContents['alsoKnown'] = alsoKnown
            fileContents['body'] = bodyText
            fileContents['link'] = self.__url
            text = self.__textToXML(fileContents, 'topic')
            if os.path.isfile(self.__savePath + fileName):
                fileName = fileName + '_1'
            with open(self.__savePath + fileName,'w') as f:
                f.write(text.encode('utf-8'))
            print 'Downloaded topic :', fileName
    
    def __saveArticle(self, soupObj):
        """Fetches and saves data from different articles"""
        
        title = soupObj.find("h1", {"class":"pheader"})
        body = soupObj.find("div", {"id":"encymain"})
        if not title is None and not body is None:
            titleText = title.text.strip()
            bodyContents = body.div.div
            fileName = self.__getFileName(titleText)
            fileContents = {}
            fileContents['title'] = titleText
            bodyText = ''
            while not bodyContents is None:
                if bodyContents.text == 'References':
                    break
                elif bodyContents.name == 'h2':
                    bodyText = bodyText + '\n'+ bodyContents.text + ' '
                elif bodyContents.name == 'ul':
                    bodyText = bodyText + bodyContents.getText(separator=u' ') + ' '
                else:
                    bodyText = bodyText + bodyContents.text + ' '
                bodyContents = bodyContents.nextSibling
            fileContents['body'] = bodyText
            fileContents['link'] = self.__url
            text = self.__textToXML(fileContents, 'article')
            if os.path.isfile(self.__savePath + fileName):
                fileName = fileName + '_1'
            with open(self.__savePath + fileName, 'w') as f:
                f.write(text.encode('utf-8'))
            print 'Downloaded article :', fileName
                                    
    def run(self):
        soup = BeautifulSoup(self.__fetchHtml())
        if self.__isArticle:
            self.__saveArticle(soup)
        else:
            self.__saveTopic(soup)
