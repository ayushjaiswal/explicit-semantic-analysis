import workerpool
import re
import os
import urllib2
from bs4 import BeautifulSoup

class MedlineDataExtractor(workerpool.Job):
    """Fetches the data from the given link and save"""
    
    def __init__(self, url, isArticle=False):
        self.__url = url
        self.__topicPath = "../../../data/Medline/Topics/"
        self.__articlePath = "../../../data/Medline/Articles/"
        self.__isArticle = isArticle
        if not os.path.exists(self.__articlePath):
            os.makedirs(self.__articlePath)
        if not os.path.exists(self.__topicPath):
            os.makedirs(self.__topicPath)
        

    def __fetchHtml(self):
        response = urllib2.urlopen(self.__url)
        html_doc = response.read()
        response.close()
        return html_doc
        

    def __saveTopic(self, soupObj):
        """Fetches and saves data from different topics"""
        
        title = soupObj.find("h1", {"id":"tp_title"})
        alsoKnown = soupObj.find("div", {"id":"ht_alsoknown"})
        body = soupObj.find("div", {"id":"tpsummary"})
        if not title is None and not body is None:
            titleText = title.text.strip().encode('utf-8')
            fileName = re.sub(' +', ' ', titleText)
            fileName = re.sub('_+', ' ', fileName)
            fileName = re.sub('/+', ' ', fileName)
            bodyText = body.text
            text = "Title: " + titleText + '\n\n'
            if not alsoKnown is None:
                text = text + alsoKnown + '\n\n'
            text = text + bodyText
            text = text + '\n\n'+'Link of medline: '+self.__url
            with open(self.__topicPath + fileName,'w') as f:
                f.write(text.encode('utf-8'))
            print 'Downloaded topic : %s'%fileName
    

    def __saveArticle(self, soupObj):
        """Fetches and saves data from different articles"""
        
        title = soupObj.find("h1", {"class":"pheader"})
        body = soupObj.find("div", {"id":"encymain"})
        if not title is None and not body is None:
            titleText = title.text.strip()
            bodyContents = body.div.div
            fileName = titleText.encode('utf-8')
            fileName = re.sub('/+', ' ',fileName)
            fileName = re.sub('_+', ' ',fileName)
            fileName = re.sub(' +', ' ',fileName)
            text = 'Title: ' + titleText + '\n\n'
            while not bodyContents is None:
                if bodyContents.text == 'References':
                    break
                if bodyContents.name == 'h2':
                    text = text + '\n\n' + 'Subtopic: ' + bodyContents.text + '\n'
                else:
                    text = text + bodyContents.text
                bodyContents = bodyContents.nextSibling
            text = text + '\n\n'+'Link of medline: '+self.__url
            text = text.encode('utf-8')
            with open(self.__articlePath + fileName, 'w') as f:
                f.write(text)
            print 'Downloaded article : %s'%fileName
                                    

    def run(self):
        soup = BeautifulSoup(self.__fetchHtml())
        if self.__isArticle:
            self.__saveArticle(soup)
        else:
            self.__saveTopic(soup)
