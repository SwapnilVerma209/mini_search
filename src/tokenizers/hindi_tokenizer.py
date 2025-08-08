import snowballstemmer
from stopwords_hindi import hindi_sw
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize import indic_tokenize

from .tokenizer import Tokenizer

class HindiTokenizer(Tokenizer):
    """A tokenizer for Hindi in the Devanagari script.
    
    Provides an interface for getting Hindi tokens at different stages of
    processing either as a list or as a dictonary with tokens and their
    occurence indicies. Utilizes the stopword data from the stopwords_hindi
    package, and the tokenizer and the normalizer from indicnlp.

    Attributes
    ----------
    stops : set
        A set of Hindi stopwords.
    stemmer : snowballstemmer
        A Snowball stemmer for Hindi.
    normalizer : DevanagariNormalizer
        A normalizer for the Devanagari script.
    
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

    stops = hindi_sw.get_hindi_sw()
    stemmer = snowballstemmer.stemmer('hindi')
    normalizer = IndicNormalizerFactory().get_normalizer('hi')

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

        text = self.normalizer.normalize(text)
        token_list = indic_tokenize.trivial_tokenize(text)
        raw_token_list = []
        for i in range(len(token_list)):
            token = token_list[i].strip()
            if len(token) == 0:
                continue
            raw_token_list.append(token)
        return raw_token_list

    def get_stemmed_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed tokens.

        Words in the given string are normalized, separated as tokens, stemmed,
        and put into a list. No filtering is done.

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
        return self.stemmer.stemWords(raw_token_list)
    
    def get_filtered_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed and filtered tokens.

        Words in the given string are normalized, separated as tokens, stemmed,
        filtered of stopwords and standalone punctuation, and put into a list.

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