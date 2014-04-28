#Configuration file for ESAModel

from tokenFIdfGenerator import TokenFIdfGenerator

#source folder of preprocessed data to be used
srcFolder = "../../data/Medline/preprocessed/Merged"

#index file for files in source folder
indexFilePath = "../../data/Medline/MergedIndex"

#Destination folder for dumper
dumperDestination = "../../data/ESAModel/"

#Dumped filename
dumpFileName = "TFIDF_InvertedIndex_Merged.pkl"

#termType can be TokenFIdfGenerator.TermType.term or TokenFIdfGenerator.TermType.synset
termType = TokenFIdfGenerator.TermType.term