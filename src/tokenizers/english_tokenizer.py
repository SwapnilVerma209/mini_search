from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer

from .tokenizer import Tokenizer

class EnglishTokenizer(Tokenizer):
    """A tokenizer for the English language.
    
    Provides an interface for getting English tokens at different stages of
    processing either as a list or as a dictonary with tokens and their
    occurence indicies. Utilizes NLTK's English tokenizer, stemmer, and
    stopword data.

    Attributes
    ----------
    stops : set
        A set of English stopwords.
    stemmer : EnglishStemmer
        A NLTK Snowball English stemmer.
    
    Methods
    -------
    get_raw_token_list(text : str) -> list
        Returns a list of unprocessed tokens.
    get_raw_token_dict(text : str) -> dict
        Returns a dictionary of unprocessed tokens paired with their counts.
    get_stemmed_token_list(text : str) -> list
        Returns a list of stemmed tokens.
    get_stemmed_token_dict(text : str) -> dict
        Returns a dictionary of stemmed tokens paired with their counts.
    get_filtered_token_list(text : str) -> list
        Returns a list of stemmed and filtered tokens.
    get_filtered_token_dict(text : str) -> dict
        Returns a dictionary of stemmed and filtered tokens paired with their
        counts.
    """
    stops = set(stopwords.words('english'))
    stemmer = EnglishStemmer()

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
        return word_tokenize(text)
    
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
        stemmed_token_list = self.get_raw_token_list(text)
        for i in range(len(stemmed_token_list)):
            token = stemmed_token_list[i]
            stemmed_token_list[i] = self.stemmer.stem(token)
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