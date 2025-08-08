import requests
from urllib.parse import urljoin
import bcp47
from bs4 import BeautifulSoup
from bs4.element import Tag

from tokenizers import *

class Parser:
    """A multilanguage HTML parser.
    
    This parser can download the HTML of sites, and generate tokens for its
    title, headers, and paragraphs. It reads the HTML 'lang' attribute, and
    tokenizes the elements accordingly. This includes stemming and stopword
    removal.

    Supported languages:
    - English
    - Mandarin Chinese
    - Hindi
    - Spanish
    - Modern Standard Arabic

    For webpages of other languages, this parser uses a generic tokenizer that
    generates character bigrams. This is expected to work with almost all
    languages, but it is very space inefficent.

    Additionally, the parser can extract all links from the webpage, and
    automatically convert all relative URLs into 

    Attributes
    ----------
    tokenizer_dict : dict
        Contains the tokenizers for the supported languages.
    gen_tokenizer : GenericTokenizer
        Tokenizer for unsupported languages.
    url : str
        URL of the current page.
    soup : BeautifulSoup
        A representation of the current webpage as a nested data structure.
    
    Methods
    -------
    set_url(url: str)
        Sets the url of the current page, initialize attributes.
    get_title_tokens() -> dict
        Returns a dictionary of the word's tokens.
    get_header_tokens() -> list
        Returns a 2D list of header token dicts.
    get_paragraph_tokens() -> list
        Returns a list of paragraph token dicts.
    get_urls() -> list
        Returns a list of the page's URLs.
    """

    tokenizer_dict = {
        'English': english_tokenizer.EnglishTokenizer(),
        'Chinese': chinese_tokenizer.ChineseTokenizer(),
        'Hindi': hindi_tokenizer.HindiTokenizer(),
        'Hindi (Latin)': hindi_latin_tokenizer.HindiLatinTokenizer(),
        'Spanish': spanish_tokenizer.SpanishTokenizer(),
        'Arabic': arabic_tokenizer.ArabicTokenizer(),
    }
    gen_tokenizer = generic_tokenizer.GenericTokenizer()

    language_dict = cls._create_lang_dict()

    @classmethod
    def _create_lang_dict(cls) -> dict:
        """Creates and returns a dictionary mapping HTML language subtags to
        supported languages.

        The keys are the language subtags representing sublanguages of the
        supported languages. The value is the simple language name,
        corresponding to the keys of the tokenizer dictionary.

        Returns
        -------
        lang_dict : dict
            The mappings of HTML language subtags to simple language names.
        """
        lang_dict = {}
        for sublanguage, tag in bcp47.languages.items():
            for language in tokenizer_dict:
                if language in sublanguage:
                    if language == 'Hindi':
                        if 'Latin' not in sublanguage:
                            lang_dict[tag] = language
                    else:
                        lang_dict[tag] = language
        return lang_dict
            
    def __init__(self):
        pass
    
    def _get_language(self, tag: Tag) -> str:
        """Gets the language of the HTML element as indicated by the HTML.

        First, the element represented by the BeautifulSoup tag is checked for
        a lang attribute of its own. If it does not, then this method searches
        for the closest ancestor with a lang attribute. If none is found, then
        None is returned.

        In either case, if the lang attribute matches a supported language,
        then the simple name of the language is returned (corresponding to the
        keys of the tokenizer dictionary). Otherwise, None is returned.

        Returns
        -------
        : str
            The simple name of the language of the element represented by tag,
            None otherwise.
        """
        for node in tag.self_and_parents:
            if 'lang' in node.attrs:
                lang = node['lang']
                if lang in self.language_dict:
                    return self.language_dict[lang]
                return None
        return None


    def _get_tokenizer(self, tag: Tag) -> tokenizer.Tokenizer:
        """Returns a tokenizer the HTML element represented by tag.

        The language of the HTML element is found, then it is used to find the 
        language's tokenizer in tokenizer_dict. If the entry does not exist,
        the generic tokenizer is returned.

        Parameters
        ----------
        tag : Tag
            The BeautifulSoup Tag representing the the HTML element.

        Returns
        -------
        tokenizer : Tokenizer
            A tokenizer for HTML element's language.
        """
        language = self._get_language(tag)
        if language == None:
            return self.gen_tokenizer
        return self.tokenizer_dict[language]

    def set_url(self, url: str) -> None:
        """Sets the current page to that of the given URL.

        Generates a BeautifulSoup object for the webpage, and uses the global
        'lang' attribute to set the primary tokenizer.

        Parameters
        ----------
        url : str
            The URL of the page.
        """
        self.url = url
        self._make_soup()

    def _get_html(self) -> str:
        """Downloads and returns the HTML text from the URL.

        Returns
        ------
        html : str
            The downloaded HTML text.
        """
        response = requests.get(self.url)
        return response.text

    def _make_soup(self) -> None:
        """Creates a BeautifulSoup object from the webpage.
        
        The HTML text is downloaded from the URL.
        """
        html = self._get_html()
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_title_tokens(self) -> dict:
        """Generates and returns a dictionary of the page's title element
        tokens.

        If the title has a 'lang' attribute, then a differnt tokenizer from the
        primary one is used. Tokens are stemmed and stripped of stopwords and
        standalone punctuation.
        
        The returned dictionary has the tokens as keys,
        and a list of the tokens' respective word indicies (0-indexed).

        Returns
        -------
        title_tokens : dict
            A dictionary of the page's title element tokens and their
            occurences.
        """
        title_tag = self.soup.head.title
        tok = self._get_tokenizer(title_tag)
        title_text = title_tag.string
        return tok.get_filtered_token_dict(title_text)

    def _get_hn_tokens(self, n: int) -> list:
        """Generates and returns a list of dictionaries corresponding to each
        h<n> element.

        The ith element of the list represents the ith h<n> element. Each
        dictionary has the tokens as keys, and a list of the tokens' respective
        word indicies (0-indexed).

        If a header has a 'lang' attribute, then a differnt tokenizer from
        the primary one is used. Tokens are stemmed and stripped of stopwords
        and standalone punctuation.
        
        Parameters
        ----------
        n : int
            The header level to search.

        Returns
        -------
        header_tokens : list
            A list with one token dictionary for each hn element.
        """
        if n < 1 or n > 6:
            return []
        header_type = 'h%d' % n
        header_tokens = []
        for header_tag in self.soup.find_all(header_type):
            tok = self._get_tokenizer(header_tag)
            header_text = header_tag.text
            tokens = tok.get_filtered_token_dict(header_text)
            header_tokens.append(tokens)
        return header_tokens

    def get_header_tokens(self) -> list:
        """Generates and returns a 2D list of header token dictionaries.

        The ith row of the list contains the list of header tokens
        corresponding to the h<i> elements. The jth element of the ith row
        represents the jth h<i> element. Each dictionary has the tokens as
        keys, and a list of the tokens' respective word indicies (0-indexed).

        If a header has a 'lang' attribute, then a differnt tokenizer from
        the primary one is used. Tokens are stemmed and stripped of stopwords
        and standalone punctuation.

        Returns
        -------
        header_tokens : list
            A 2D list of token dictionaries.
        """
        header_tokens = [None]
        for i in range(1, 7):
            header_tokens.append(self._get_hn_tokens(i))
        return header_tokens

    def get_paragraph_tokens(self) -> list:
        """Generates and returns a list of paragraph token dictionaries.

        The ith element of the list corresponds to the ith paragraph element
        on the page. Each dictionary has the tokens as keys, and a list of the
        tokens' respectiveword indicies (0-indexed).

        If a paragraph has a 'lang' attribute, then a differnt tokenizer from
        the primary one is used. Tokens are stemmed and stripped of stopwords
        and standalone punctuation.

        Returns
        -------
        paragraph : list
            A list of paragraph token dictionaries
        """
        paragraph_tokens = []
        for paragraph_tag in self.soup.find_all('p'):
            tok = self._get_tokenizer(paragraph_tag)
            paragraph_text = paragraph_tag.text
            tokens = tok.get_filtered_token_dict(paragraph_text)
            paragraph_tokens.append(tokens)
        return paragraph_tokens

    def get_urls(self) -> list:
        """Generates and returns a list of URLs from the page.

        Any relative URLs are automatically converted into absolute URLs.

        Returns
        -------
        urls : list
            A list of URLs from the page.
        """
        urls = []
        for anchor in self.soup.find_all('a'):
            raw_url = anchor.get('href')
            abs_url = urljoin(self.url, raw_url)
            urls.append(abs_url)
        return urls