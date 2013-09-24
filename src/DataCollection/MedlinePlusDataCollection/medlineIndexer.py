#save the index files for aricles and topics 
import re
from os import listdir
from os.path import isfile, join

topicPath = '../../../data/Medline/Topics/'
articlePath = '../../../data/Medline/Articles/'
indexFilePath = '../../../data/Medline/'
topicFiles = [fileName for fileName in listdir(topicPath) if isfile(topicPath+fileName) and not fileName[:-1] == '~']
articleFiles = [fileName for fileName in listdir(articlePath) if isfile(articlePath+fileName) and not fileName[:-1] == '~']
with open(indexFilePath+'TopicIndex','w') as f:
    for fileName in topicFiles:
        f.write(fileName + '\n')

with open(indexFilePath+'ArticleIndex','w') as f:
    for fileName in articleFiles:
        f.write(fileName + '\n')
