from chinese import ChineseAnalyzer
import nltk
from nltk.corpus import stopwords

from .tokenizer import Tokenizer

class ChineseTokenizer(Tokenizer):
    """A tokenizer for Mandarin Chinese.
    
    Provides an interface for getting Chinese tokens at different stages of
    processing either as a list or as a dictonary with tokens and their
    occurence indicies. Utilizes the ChineseAnalyzer from the package chinese,
    and NLTK's Chinese stopword data.

    Attributes
    ----------
    stops : set
        A set of Chinese stopwords.
    analyzer : ChineseAnalyzer
        A tool for analyzing Chinese text from the chinese package.
    
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

    stops = set(stopwords.words('chinese'))
    analyzer = ChineseAnalyzer()

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        """Creates and returns a list of unprocessed tokens.

        Words in the given string are separated as tokens and put into a list.
        Whitespaces are removed in order for the tokenizer to behave like other
        tokenizers. Apart from that, no stemming or filtering is done.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of raw tokens generated from the string.
        """

        text = ''.join(text.split())
        return self.analyzer.parse(text).tokens()
    
    def get_stemmed_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed tokens.

        NOTE: No stemming is actually done here; Chinese has very little
        morphology.

        No punctuation is filtered.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of stemmed tokens generated from the string.
        """

        return self.get_raw_token_list(text)
    
    def get_filtered_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed and filtered tokens.

        NOTE: No stemming is actually done here; Chinese has very little
        morphology.

        Words in the given string are separated as tokens, filtered of
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