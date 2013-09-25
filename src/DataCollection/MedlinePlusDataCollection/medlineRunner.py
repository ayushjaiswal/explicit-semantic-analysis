from medlineLinkExtractor import MedlineLinkExtractor
from medlineDataExtractor import MedlineDataExtractor
import workerpool

topicsXML_path = "../../../etc/mplus_topics_2013-09-14.xml"
dataPath = "../../../data/Medline/"
topicFolder = 'Topics'
articleFolder = 'Articles'

class MedlineRunner:
    """Class to run the Medline data collection pipeline."""

    def __init__(self, topicsXML_path, dataPath, topicFolder, articleFolder):
        self.__topicsXML_path = topicsXML_path
        self.__topicPath = dataPath + topicFolder + '/'
        self.__articlePath = dataPath + articleFolder + '/'

    def downloadAndExtract(self):
        """Downloads and extracts Medline data."""
        
        # Extract topics and articles url
        mLE = MedlineLinkExtractor()
        mLE.readXml(self.__topicsXML_path)
        topics = mLE.getTopics()
        articles = mLE.getArticles()
        topicCount = 0
        articleCount = 0
                
        # Downloader
        pool = workerpool.WorkerPool(size=20)
        for url in topics:
            topicCount = topicCount + 1
            job = MedlineDataExtractor(url, self.__topicPath, isArticle=False)
            pool.put(job)
            
        for url in articles:
            articleCount = articleCount + 1
            job = MedlineDataExtractor(url, self.__articlePath, isArticle=True)
            pool.put(job)

        pool.shutdown()
        pool.wait()
        print str(topicCount) + ' Topics downloaded'
        print str(articleCount) + ' Articles downloaded'
        print 'Run medlineIndexer.py file to build index of topics/aricles'

def main():
    """To run this module as a standalone program."""

    medlineRunner = MedlineRunner(topicsXML_path, dataPath, topicFolder, articleFolder)
    medlineRunner.downloadAndExtract()

if __name__ == '__main__':
    main()