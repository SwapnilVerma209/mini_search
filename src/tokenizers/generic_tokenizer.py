from .tokenizer import Tokenizer

class GenericTokenizer(Tokenizer):
    """A generic tokenizer for unknown languages.

    Creates character bigrams as tokens. Should work on most languages, but is
    very space inefficient compared to the other more specialized tokenizers.
    Should be used as a last resort.

    Methods
    -------
    get_raw_token_list(text : str) -> list
        Returns a list of character bigrams.
    get_raw_token_dict(text : str) -> dict
        Returns a dictionary of character bigrams paired with their counts.
    get_stemmed_token_list(text : str) -> list
        Returns a list of character bigrams.
    get_stemmed_token_dict(text : str) -> dict
        Returns a dictionary of character bigrams paired with their counts.
    get_filtered_token_list(text : str) -> list
        Returns a list of character bigrams.
    get_filtered_token_dict(text : str) -> dict
        Returns a dictionary of character bigrams paired with their counts.
    """
    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        """Creates and returns a list of character bigrams.

        Whitespace characters are removed from the text prior to creating
        tokens.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of character bigrams generated from the string.
        """
        text = "".join(text.split())
        raw_token_list = []
        for i in range(len(text) - 1):
            token = text[i:i+2].lower()
            raw_token_list.append(token)
        return raw_token_list
    
    def get_stemmed_token_list(self, text: str) -> list:
        """Creates and returns a list of character bigrams.

        Whitespace characters are removed from the text prior to creating
        tokens.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of character bigrams generated from the string.
        """
        return self.get_raw_token_list(text)
    
    def get_filtered_token_list(self, text: str) -> list:
        """Creates and returns a list of character bigrams.

        Whitespace characters are removed from the text prior to creating
        tokens.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of character bigrams generated from the string.
        """
        return self.get_raw_token_list(text)