from SemanticRelatedness.srcRunner import SRC_Runner

ApplicationRunner = SRC_Runner
ApplicationName = 'Semantic Relatedness Calculator'
ESADumpPath = '../data/ESAModel/'
ESADumpFileName = 'TFIDF_InvertedIndex.pkl'
BatchDataFile = '../data/test/MiniMayoSRS.csv'  # Required if the Semantic Relatedness Calculator has to be run in batch mode
Word1Index = 3  # Required if the Semantic Relatedness Calculator has to be run in batch mode
Word2Index = 4  # Required if the Semantic Relatedness Calculator has to be run in batch mode
BatchResultsDumpFile = 'results.csv'  # Required if the Semantic Relatedness Calculator has to be run in batch mode