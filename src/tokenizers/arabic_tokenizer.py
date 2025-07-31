import nltk
from nltk.stem.snowball import ArabicStemmer
from nltk.tokenize.regexp import wordpunct_tokenize
from nltk.corpus import stopwords

from .tokenizer import Tokenizer

class ArabicTokenizer(Tokenizer):
    """A tokenizer for Arabic.
    
    Provides an interface for getting Arabic tokens at different stages of
    processing either as a list or as a dictonary with tokens and their
    occurence indicies. Utilizes NLTK's word-punctuation tokenizer, and NLTK's
    Arabic stemmer and stopword data.

    Attributes
    ----------
    stops : set
        A set of Arabic stopwords.
    stemmer : ArabicStemmer
        A NLTK Snowball Arabic stemmer.
    
    Methods
    -------
    get_raw_token_list(text : str) -> list
        Returns a list of unprocessed tokens.
    get_raw_token_dict(text : str) -> dict
        Returns a dictionary of unprocessed tokens paired with their occurence
        indicies.
    get_stemmed_token_list(text : str) -> list
        Returns a list of stemmed tokens.
    get_stemmed_token_dict(text : str) -> dict
        Returns a dictionary of stemmed tokens paired with their occurence
        indicies.
    get_filtered_token_list(text : str) -> list
        Returns a list of stemmed and filtered tokens.
    get_filtered_token_dict(text : str) -> dict
        Returns a dictionary of stemmed and filtered tokens paired with their
        occurence indicies.
    """

    stops = set(stopwords.words('arabic'))
    stemmer = ArabicStemmer()

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        """Creates and returns a list of unprocessed tokens.

        Words in the given string are separated as tokens and put into a list.
        No stemming or filtering is done.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of raw tokens generated from the string.
        """

        token_list = wordpunct_tokenize(text)
        raw_token_list = []
        for i in range(len(token_list)):
            token = token_list[i].strip()
            if len(token) == 0:
                continue
            raw_token_list.append(token)
        return raw_token_list
    
    def get_stemmed_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed tokens.

        Words in the given string are separated as tokens, stemmed, and put
        into a list. No filtering is done.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of stemmed tokens generated from the string.
        """

        raw_token_list = self.get_raw_token_list(text)
        stemmed_token_list = []
        for i in range(len(raw_token_list)):
            token = raw_token_list[i]
            token = self.stemmer.stem(token)
            token = token.strip()
            if len(token) == 0:
                continue
            stemmed_token_list.append(token)
        return stemmed_token_list
    
    def get_filtered_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed and filtered tokens.

        Words in the given string are separated as tokens, stemmed, filtered of
        stopwords and standalone punctuation, and put into a list.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of stemmed and filtered tokens generated from the string.
        """

        stemmed_token_list = self.get_stemmed_token_list(text)
        filtered_token_list = []
        for token in stemmed_token_list:
            if self._is_punctuation(token) or token in self.stops:
                continue
            filtered_token_list.append(token)
        return filtered_token_list