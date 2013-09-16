from medlineLinkExtractor import MedlineLinkExtractor
from medlineDataExtractor import MedlineDataExtractor

mLE = MedlineLinkExtractor()
mLE.readXml("../etc/mplus_topics_2013-09-14.xml")

topics = mLE.getTopics()
articles = mLE.getArticles()
countTopics = len(topics)
countArticles = len(articles)

mDE = MedlineDataExtractor()

for topic in topics:
    mDE.extractTopicData(topic)
    countTopics -= 1
    print str(countTopics) + ' topics left'
    
for article in articles:
    mDE.extractArticleData(article)
    countArticles -= 1
    print str(countArticles) + ' articles left'
    
mDE.closeIndexFile()


