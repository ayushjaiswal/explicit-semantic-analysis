# This creates a layer of abstraction between the functions required 
# for preprocessing raw text and their implementations.
# Here, we use the implementations provided by NLTK.

import nltk

class Preprocessor:
    """Preprocesses the raw text for further operations.

    Allows the option to filter stop words.
    This has to be passed as an argument(shouldFilterStopWords) to the constructor
    along with the raw text.

    shouldFilterStopWords can be:
        True
        False (default)

    """

    class TokenType():
        """Enum for token types"""
        raw = 0
        stemmed = 1
        lemmatized = 2

    def __init__(self, text, shouldFilterStopWords=True, shouldFilterPunctuation=True):
        self.__text = text
        self.__rawTokens = [t.lower() for t in self.__tokenize(self.__text)]
        self.__stopWords = nltk.corpus.stopwords.words('english')
        if shouldFilterStopWords:
            self.__rawTokens = self.__filterStopWords(self.__rawTokens)
        self.__shouldFilterPunctuation = shouldFilterPunctuation
        self.__stemmedTokens = self.__stem(self.__rawTokens)
        self.__lemmatizedTokens = self.__lemmatize(self.__rawTokens)
        self.TokenType = Preprocessor.TokenType

    def __tokenize(self, text):
        """Tokenizes raw text into words and punctuation marks."""
        
        return nltk.tokenize.wordpunct_tokenize(text.replace(". ", " . "))

    def __stem(self, tokens):
        """Performs stemming on tokens and returns the list of stems."""

        porter = nltk.PorterStemmer()
        return [porter.stem(t) for t in tokens]

    def __lemmatize(self, tokens):
        """Performs stemming on tokens and returns the list of lemmas."""

        wnl = nltk.WordNetLemmatizer()
        return [wnl.lemmatize(t) for t in tokens]

    def __isNotPunctuation(self, x):
        """Returns True if x is a punctuation mark."""

        return ((len(x) > 1) or x.isalnum())

    def __filterPunctuation(self, tokens):
        """Removes all punctuation marks from tokens."""

        filteredTokens = []
        for token in tokens:
            punctuationsOnly = True
            for c in token:
                if self.__isNotPunctuation(c):
                    punctuationsOnly = False
                    break
            if not punctuationsOnly:
                filteredTokens.append(token)
        return filteredTokens

    def __filterStopWords(self, tokens):
        """Removes all the stop words from tokens."""

        return [t for t in tokens if not t in self.__stopWords]

    def getTokens(self, type=TokenType.raw):
        """Returns tokens.

        type can be the following token types:
            self.TokenType.raw (default)
            self.TokenType.stemmed
            self.TokenType.lemmatized

        shouldFilterPunctuation can be:
            True (default)
            False

        """

        if type == self.TokenType.stemmed:
            tokens = self.__stemmedTokens
        elif type == self.TokenType.lemmatized:
            tokens = self.__lemmatizedTokens
        else:
            tokens = self.__rawTokens

        if self.__shouldFilterPunctuation:
            return self.__filterPunctuation(tokens)
        else:
            return tokens