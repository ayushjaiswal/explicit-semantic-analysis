from medlineLinkExtractor import MedlineLinkExtractor
from medlineDataExtractor import MedlineDataExtractor
from os import listdir
from os.path import isfile, join
import workerpool

#extract topics and articles url
mLE = MedlineLinkExtractor()
mLE.readXml("../../../etc/mplus_topics_2013-09-14.xml")
topics = mLE.getTopics()
articles = mLE.getArticles()
topicCount = 0
articleCount = 0
        
#Downloader
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

#save the index files for aricles and topics 
topicPath = '../../../data/Medline/Topics/'
articlePath = '../../../data/Medline/Articles/'
indexFilePath = '../../../data/Medline/'
topicFiles = [fileName for fileName in listdir(topicPath) if isfile(topicPath+fileName)]
articleFiles = [fileName for fileName in listdir(articlePath) if isfile(articlePath+fileName)]
with open(indexFilePath+'Topics Index','w') as f:
    for fileName in topicFiles:
        f.write(fileName + '\n')

with open(indexFilePath+'Article Index','w') as f:
    for fileName in articleFiles:
        f.write(fileName + '\n')
