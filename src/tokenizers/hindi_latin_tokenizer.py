from indicnlp.transliterate.unicode_transliterate import ItransTransliterator

from .hindi_tokenizer import HindiTokenizer

class HindiLatinTokenizer(HindiTokenizer):
    """A tokenizer for Hindi in the Latin script.
    
    Provides an interface for getting Hindi tokens at different stages of
    processing either as a list or as a dictonary with tokens and their
    occurence indicies. Utilizes the stopword data from the stopwords_hindi
    package, and the transliterator, tokenizer, and the normalizer from
    indicnlp.

    Tokens are converted into the Devanagari script to maintain compatability
    with the standard Hindi tokenizer.

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

    def get_raw_token_list(self, text: str) -> list:
        """Creates and returns a list of unprocessed tokens.

        Words in the given string are separated as tokens and put into a list.
        Then, the words are converted from their Latin transliteration into the
        Devnagari script. No stemming or filtering is done.

        Parameters
        ----------
        text : str
            The text to generate tokens from.
        
        Returns
        -------
        token_list : list
            A list of raw tokens generated from the string.
        """
        text = ItransTransliterator.from_itrans(text, 'hi')
        return super().get_raw_token_list(text)
