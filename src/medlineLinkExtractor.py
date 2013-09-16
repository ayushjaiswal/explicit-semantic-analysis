import re

class MedlineLinkExtractor:
    """Extracts links from medline xml files"""

    def __init__(self):
        self.__topics = set([])
        self.__articles = set([])

    def readXml(self, relativeSrcFilePath):
        """Reads the xml file and extract links of topics and articles"""
        
        patternTopics = 'http://www\.nlm\.nih\.gov/medlineplus/\w+\.html'
        patternArticles = 'http://www\.nlm\.nih\.gov/medlineplus/ency/article/\d+\.htm'
        with open(relativeSrcFilePath) as f_xml:
            text = f_xml.read()
        self.__topics = set(re.findall(patternTopics, text))
        self.__articles = set(re.findall(patternArticles, text))
        
    def getTopics(self):
        return list(self.__topics)
       
    def getArticles(self):
        return list(self.__articles)
