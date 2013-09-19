import workerpool
import os
import urllib2
from bs4 import BeautifulSoup

class MedlineDataExtractor(workerpool.Job):
    """Fetches the data from the given link and save"""
    
    def __init__(self, url, count, isArticle=False):
        self.__url = url
        self.__count = count
        self.__path = "a/" #"../../../data/Medline/"
        self.__isArticle = isArticle

    def __fetchHtml(self):
        response = urllib2.urlopen(self.__url)
        html_doc = response.read()
        response.close()
        return html_doc
        
    def __saveTopic(self, soupObj, fileName):
        """Fetches and saves data from different topics"""
        
        title = soupObj.find("h1", {"id":"tp_title"})
        alsoKnown = soupObj.find("div", {"id":"ht_alsoknown"})
        body = soupObj.find("div", {"id":"tpsummary"})
        if not title is None and not body is None:
            titleText = title.text
            bodyText = body.text
            text = "Title: " + titleText + '\n\n'
            if not alsoKnown is None:
                text = text + alsoKnown + '\n\n'
            text = text + bodyText
            self.__count = self.__count + 1
            with open(self.__path + fileName,'w') as f:
                f.write(text.encode('utf-8'))
    
    def __saveArticle(self, soupObj):
        """Fetches and saves data from different articles"""
        
        title = soupObj.find("h1", {"class":"pheader"})
        body = soupObj.find("div", {"id":"encymain"})
        if not title is None and not body is None:
            titleText = title.text
            bodyContents = body.div.div
            self.__count = self.__count + 1
            fileName = titleText.encode('utf-8')
            fileName = fileName.replace('/', '_')
            fileName = fileName.replace(' ', '_')
            fileName = fileName.replace('-', '_')
            text = 'Title: ' + titleText + '\n\n'
            while not bodyContents is None:
                if bodyContents.text == 'References':
                    break
                if bodyContents.name == 'h2':
                    text = text + '\n\n' + 'Subtopic: ' + bodyContents.text + '\n'
                else:
                    text = text + bodyContents.text
                bodyContents = bodyContents.nextSibling
            text = text.encode('utf-8')
            with open(self.__path + fileName, 'w') as f:
                f.write(text)
        else:
            print self.__url
             
    def run(self):
        soup = BeautifulSoup(self.__fetchHtml())
        link = self.__url[::-1]
        idx1 = link.find('/')
        lenUrl = len(link)
        if self.__isArticle:
            self.__saveArticle(soup)
        else:
            fileName = self.__url[lenUrl - idx1 : lenUrl-5]        
            self.__saveTopic(soup, fileName)