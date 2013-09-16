import workerpool
import os
import urllib2
from bs4 import BeautifulSoup

class MedlineDataExtractor(workerpool.Job):
    """Fetch the data from the given link and save"""
    
    def __init__(self, url, count, isArticle):
        self.__url = url
        self.__count = count
        self.__path = "../data/Medline/"
        self.__isArticle = isArticle

    def __fetchHtml(self):
        response = urllib2.urlopen(self.__url)
        html_doc = response.read()
        response.close()
        return html_doc
        
    def __saveTopic(self, soupObj, fileName):
        """Fetch and save data from different topics"""
        
        title = soupObj.find("h1",{"id":"tp_title"})
        alsoKnown = soupObj.find("div",{"id":"ht_alsoknown"})
        body = soupObj.find("div",{"id":"tpsummary"})
        if not title == None and not body == None:
            title = title.text
            body = body.text
            text = "Title: " +title + '\n\n'
            if not alsoKnown == None:
                text += alsoKnown + '\n\n'
            text += body
            self.__count += 1
            with open(self.__path + fileName,'w') as f:
                f.write(text.encode('utf-8'))
    

    def __saveArticle(self, soupObj):
        """Fetch and save data from different articles"""
        
        title = soupObj.find("h1",{"class":"pheader"})
        body = soupObj.find("div",{"id":"encymain"})
        if not title == None and not body == None:
            title = title.text
            body = body.div.div
            self.__count += 1
            fileName = title.encode('utf-8')
            fileName = fileName.replace('/', '_')
            fileName = fileName.replace(' ', '_')
            fileName = fileName.replace('-', '_')
            text = ""
            text += 'Title: '+title + '\n\n'

            while not body == None:
                if body.text == 'References':
                    break
                if body.name == 'h2':
                    text += '\n\n'+ 'Subtopic: '+body.text+'\n'
                else:
                    text += body.text
                body = body.nextSibling
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

        if self.__isArticle == 0:
            fileName = self.__url[lenUrl-idx1: lenUrl-5]        
            self.__saveTopic(soup, fileName)
            
        else:
            self.__saveArticle(soup)
        
