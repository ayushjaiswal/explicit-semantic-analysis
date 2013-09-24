from medlineLinkExtractor import MedlineLinkExtractor
from medlineDataExtractor import MedlineDataExtractor
import workerpool

# Extract topics and articles url
mLE = MedlineLinkExtractor()
mLE.readXml("../../../etc/mplus_topics_2013-09-14.xml")
topics = mLE.getTopics()
articles = mLE.getArticles()
topicCount = 0
articleCount = 0
        
# Downloader
pool = workerpool.WorkerPool(size=20)
for url in topics:
    topicCount = topicCount + 1
    job = MedlineDataExtractor(url, isArticle=False)
    pool.put(job)
    
for url in articles:
    articleCount = articleCount + 1
    job = MedlineDataExtractor(url, isArticle=True)
    pool.put(job)

pool.shutdown()
pool.wait()
print str(topicCount) + ' Topics downloaded'
print str(articleCount) + ' Articles downloaded'
print 'Run medlineIndexer.py file to build index of topics/aricles'
