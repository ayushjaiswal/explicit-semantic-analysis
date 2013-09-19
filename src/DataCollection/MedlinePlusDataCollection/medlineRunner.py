from medlineLinkExtractor import MedlineLinkExtractor
from medlineDataExtractor import MedlineDataExtractor
import workerpool

mLE = MedlineLinkExtractor()
mLE.readXml("../../../etc/mplus_topics_2013-09-14.xml")
topics = mLE.getTopics()
articles = mLE.getArticles()
count = 0
        
pool = workerpool.WorkerPool(size=100)
for url in articles:
    count = count + 1
    job = MedlineDataExtractor(url, count, isArticle=True)
    pool.put(job)

for url in topics:
    count = count + 1
    job = MedlineDataExtractor(url, count, isArticle=False)
    pool.put(job)
    
pool.shutdown()
pool.wait()