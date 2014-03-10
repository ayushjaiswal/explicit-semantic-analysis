from SemanticRelatedness.srcRunner import SRC_Runner

ApplicationRunner = SRC_Runner
ApplicationName = 'Semantic Relatedness Calculator'
ESADumpPath = '../data/ESAModel/'
ESADumpFileName = 'TFIDF_InvertedIndex_Merged.pkl'
BatchDataFile = '../data/test/MayoSRS.csv'  # Required if the Semantic Relatedness Calculator has to be run in batch mode
Word1Index = 3  # Required if the Semantic Relatedness Calculator has to be run in batch mode
Word2Index = 4  # Required if the Semantic Relatedness Calculator has to be run in batch mode
BatchResultsDumpFile = 'results_Coders_Merged.csv'  # Required if the Semantic Relatedness Calculator has to be run in batch mode