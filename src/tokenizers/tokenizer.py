import unicodedata
from abc import ABC, abstractmethod

class Tokenizer(ABC):
    """An abstract Tokenizer class.
    
    Provides an interface for getting tokens at different stages of processing
    either as a list or as a dictonary with tokens and their occurence
    indicies. All the token list methods are abstract, while the token dict
    functions are already implemented, and do not need to be implemented in
    subclasses.

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
    @abstractmethod
    def __init__(self):
        pass

    def _make_token_dict(self, token_list: list) -> dict:
        """Creates and returns a token dict given a token list.
        
        The dict has each unique token as the key, and a list of their indicies
        as the value.

        Parameters
        ----------
        token_list : list
            The list of tokens to create a token dict out of.

        Returns
        -------
        token_dict : dict
            A dictionary of tokens with lists of their indicies in the
            original list.
        """
        token_dict = {}
        for i in range(len(token_list)):
            token = token_list[i]
            if token in token_dict:
                token_dict[token].append(i)
            else:
                token_dict[token] = [i]
        return token_dict

    def _is_punctuation(self, text: str) -> bool:
        """Determines if a given string is a standalone punctuation.

        A string is considered a standalone punctuation if it only consists of
        one character, and that character is a punctuation.

        Parameters:
        -----------
        text : str
            The string to be checked.
        
        Returns
        -------
        is_punctuation : bool
            True if the string is a stanalone punctuation, false otherwise.
        """
        if len(text) != 1:
            return False
        return unicodedata.category(text[0]).startswith("P")

    @abstractmethod
    def get_raw_token_list(self, text: str) -> list:
        """Creates and returns a list of unprocessed tokens.

        Words in the given string are separated as tokens and put into a list.
        No stemming or filtering is done. Implementation details are dependent
        on the language being processed.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of raw tokens generated from the string.
        """
        return None
    
    def get_raw_token_dict(self, text: str) -> dict:
        """Generates a dictionary of raw tokens from the given string.

        The string is separated into tokens and put into a list. No stemming
        or filtering is done at this point. Then, tokens from the list are put
        into a dict. The dict has each unique token as the key, and a list of
        their indicies as the value.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        raw_token_dict : dict
            A dictionary of raw tokens and their occurence indicies.
        """
        token_list = self.get_raw_token_list(text)
        return self._make_token_dict(token_list)
    
    @abstractmethod
    def get_stemmed_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed tokens.

        Words in the given string are separated as tokens, stemmed, and put
        into a list. No filtering is done. Implementation details are dependent
        on the language being processed.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of stemmed tokens generated from the string.
        """
        return None
    
    def get_stemmed_token_dict(self, text: str) -> dict:
        """Generates a dictionary of stemmed tokens from the given string.

        The string is separated into tokens, stemmed, and put into a list.
        Then, tokens from the list are put into a dict. The dict has each
        unique token as the key, and a list of their indicies as the value.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        raw_token_dict : dict
            A dictionary of stemmed tokens and their occurence indicies.
        """
        token_list = self.get_stemmed_token_list(text)
        return self._make_token_dict(token_list)

    @abstractmethod
    def get_filtered_token_list(self, text: str) -> list:
        """Creates and returns a list of stemmed and filtered tokens.

        Words in the given string are separated as tokens, stemmed, filtered of
        stopwords and standalone punctuation, and put into a list.
        Implementation details are dependent on the language being processed.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of stemmed and filtered tokens generated from the string.
        """
        return None
    
    def get_filtered_token_dict(self, text: str) -> dict:
        """Generates a dictionary of stemmed and filtered tokens from the given
        string.

        Words in the given string are separated as tokens, stemmed, filtered of
        stopwords and standalone punctuation, and put into a list. Then, tokens
        from the list are put into a dict. The dict has each unique token as
        the key, and a list of their indicies as the value.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        raw_token_dict : dict
            A dictionary of stemmed and filtered tokens and their occurence
            indicies.
        """
        token_list = self.get_filtered_token_list(text)
        return self._make_token_dict(token_list)