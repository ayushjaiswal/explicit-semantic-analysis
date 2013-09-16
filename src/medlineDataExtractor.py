import urllib2
from bs4 import BeautifulSoup

class MedlineDataExtractor:
    """Extracts data from links"""
    
    def __init__(self):
        self.__count = 0
        self.__path = "../data/Medline/"
        self.__indexFile = open(self.__path + "index",'a+')
            
    
    
    def __fetchHtml(self,link):
        response = urllib2.urlopen(link)
        html_doc = response.read()
        response.close()
        return html_doc
    
   
    def extractTopicData(self, link):
        soup = BeautifulSoup(self.__fetchHtml(link))
        title = soup.find("h1",{"id":"tp_title"})
        alsoKnown = soup.find("div",{"id":"alsoknown"})
        body = soup.find("div",{"id":"tpsummary"})
        
        if not title == None and not body == None:
            title = title.text
            body = body.text
            text = "Title: " +title + '\n\n'
            if not alsoKnown == None:
                text += alsoKnown + '\n\n'
            text += body
            self.__count += 1
            with open(self.__path + str(self.__count),'w') as f:
                f.write(text.encode('utf-8'))
            self.__indexFile.write(str(self.__count) + '. ' + title + '\n')
        
        
    def extractArticleData(self, link):
        soup = BeautifulSoup(self.__fetchHtml(link))
        title = soup.find("h1",{"class":"pheader"})
        body = soup.find("div",{"id":"encymain"})

        if not title == None and not body == None:
            title = title.text
            body = body.div.div
            self.__count += 1
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
            with open(self.__path + str(self.__count), 'w') as f:
                f.write(text)
            self.__indexFile.write(str(self.__count) + '.' + title+'\n')
            
            
    def closeIndexFile(self):
        self.__indexFile.close()
