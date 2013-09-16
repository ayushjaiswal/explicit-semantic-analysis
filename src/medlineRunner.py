from medlineLinkExtractor import MedlineLinkExtractor
from medlineDataExtractor import MedlineDataExtractor
import workerpool

mLE = MedlineLinkExtractor()
mLE.readXml("../etc/mplus_topics_2013-09-14.xml")
topics = mLE.getTopics()
articles = mLE.getArticles()
count = 0
        
pool = workerpool.WorkerPool(size=100)
for url in articles:
    count+= 1
    job = MedlineDataExtractor(url, count, 1)
    pool.put(job)

for url in topics:
    count += 1
    job = MedlineDataExtractor(url,count, 0)
    pool.put(job)
    
pool.shutdown()
pool.wait()

