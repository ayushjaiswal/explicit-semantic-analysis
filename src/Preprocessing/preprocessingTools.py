# This creates a layer of abstraction between the functions required 
# for preprocessing raw text and their implementations.
# Here, we use the implementations provided by NLTK.

import nltk
from collections import defaultdict

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

    def __init__(self, shouldFilterStopWords=True, shouldFilterPunctuation=True):
        self.__shouldFilterStopWords = shouldFilterStopWords
        self.__shouldFilterPunctuation = shouldFilterPunctuation
        self.__stopWords = nltk.corpus.stopwords.words('english')

    def __tokenize(self, text):
        """Tokenizes raw text into words and punctuation marks."""
        
        return nltk.tokenize.wordpunct_tokenize(text.replace(". ", " . "))

    def __stem(self, tokens):
        """Performs stemming on tokens and returns the list of stems."""

        porter = nltk.PorterStemmer()
        return [porter.stem(t) for t in tokens]

    def __lemmatize(self, tagged_tokens):
        """Performs lemmatization on POS tagged tokens and returns the list of lemmas."""

        wnl = nltk.WordNetLemmatizer()
        pos_map = defaultdict(lambda: 'n', {'N' : 'n', 'J' : 'a', 'V' : 'v', 'R' : 'r'})
        return [wnl.lemmatize(token, pos_map[pos_tag[0]]) for token, pos_tag in tagged_tokens]

    def __isNotPunctuation(self, x):
        """Returns True if x is a punctuation mark."""

        return ((len(x) > 1) or x.isalnum())

    def __POSTag(self, tokens):
        """Performs Parts of Speech Tagging on the tokens and returns list of (token, tag)."""

        return nltk.pos_tag(tokens)

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

    def getTokens(self, text, type=TokenType.raw):
        """Returns tokens after preprocessing text.

        type can be the following token types:
            self.TokenType.raw (default)
            self.TokenType.stemmed
            self.TokenType.lemmatized

        shouldFilterPunctuation can be:
            True (default)
            False

        """

        tokens = []
        self.TokenType = Preprocessor.TokenType
        if type == self.TokenType.stemmed:
            tokens = [t.lower() for t in self.__tokenize(text)]
            tokens = self.__stem(tokens)
        elif type == self.TokenType.lemmatized:
            taggedTokens = self.__POSTag(self.__tokenize(text))
            tokens = self.__lemmatize(taggedTokens)
        else:
            tokens = [t.lower() for t in self.__tokenize(text)]

        if self.__shouldFilterStopWords:
            tokens = self.__filterStopWords(tokens)

        if self.__shouldFilterPunctuation:
            return self.__filterPunctuation(tokens)
        else:
            return tokens