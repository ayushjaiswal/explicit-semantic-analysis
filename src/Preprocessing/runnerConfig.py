#Configuration file for PreprocessorRunner
from preprocessingTools import Preprocessor
#source path for raw data
rawDataPath = "../../data/Medline/raw/Topics"

#destination path for preprocessed data
preprocessedDataPath = "../../data/Medline/preprocessed/Topics"

#Tag in which data lies
dataTag = "body"

#Filter stop words
shouldFilterStopWords = True

#Filter punctuations
shouldFilterPunctuation = True

#Type of token
tokenType = Preprocessor.TokenType.lemmatized

#Type of token for input text (which may not be in sentences)
inputTokenType = Preprocessor.TokenType.raw