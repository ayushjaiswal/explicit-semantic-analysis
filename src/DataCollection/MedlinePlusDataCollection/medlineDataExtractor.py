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
            text = '<?xml version="1.0" encoding="UTF-8"?>\n<topic>\n'
            text = text + '<title>' + titleText + '</title>\n'
            if not alsoKnown is None:
                text = text + '<alsoKnown>'+ alsoKnown + '</alsoKnown>\n'
            text = text + '<body>' + bodyText + '</body>\n'
            text = text + '<link>' + self.__url + '</link>\n</topic>'
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
            fileName = titleText.encode('utf-8')
            fileName = re.sub('/+', ' ',fileName)
            fileName = re.sub('_+', ' ',fileName)
            fileName = re.sub(' +', ' ',fileName)
            text = '<?xml version="1.0" encoding="UTF-8"?>\n<article>\n'
            text = text + '<title>' + titleText + '</title>\n'
            text = text + "<body>"
            while not bodyContents is None:
                if bodyContents.text == 'References':
                    break
                text = text + bodyContents.text
                bodyContents = bodyContents.nextSibling
            text = text + '</body>\n'
            text = text + '<link>' + self.__url + '</link>\n</article>'
            text = text.encode('utf-8')
            with open(self.__savePath + fileName, 'w') as f:
                f.write(text)
            print 'Downloaded article :', fileName
                                    
    def run(self):
        soup = BeautifulSoup(self.__fetchHtml())
        if self.__isArticle:
            self.__saveArticle(soup)
        else:
            self.__saveTopic(soup)
