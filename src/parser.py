import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

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
    primary_tok : Tokenizer
        The primary tokenizer for the current page (based on the global 'lang'
        value).
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
        'en': english_tokenizer.EnglishTokenizer(),
        'zh': chinese_tokenizer.ChineseTokenizer(),
        'hi': hindi_tokenizer.HindiTokenizer(),
        'es': spanish_tokenizer.SpanishTokenizer(),
        'ar': arabic_tokenizer.ArabicTokenizer(),
    }
    gen_tokenizer = generic_tokenizer.GenericTokenizer()

    def __init__(self):
        pass
      
    def _get_tokenizer(self, lang: str) -> tokenizer.Tokenizer:
        """Returns a tokenizer for the given language tag.

        The language tag is used to find the language's tokenizer in
        tokenizer_dict. If the entry does not exist, the generic tokenizer is
        returned.

        Parameters
        ----------
        lang : str
            The HTML language tag.

        Returns
        -------
        tokenizer : Tokenizer
            A tokenizer for the given language.
        """
        if lang in self.tokenizer_dict:
            return self.tokenizer_dict[lang]
        return self.gen_tokenizer

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
        self.primary_tok = self.gen_tokenizer
        if 'lang' in self.soup.html.attrs:
            primary_lang = self.soup.html['lang']
            self.primary_tok = self._get_tokenizer(primary_lang)

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
        tok = self.primary_tok
        if 'lang' in title_tag.attrs:
            lang = title_tag['lang']
            tok = self._get_tokenizer(lang)
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
            tok = self.primary_tok
            if 'lang' in header_tag.attrs:
                lang = header_tag['lang']
                tok = self._get_tokenizer(lang)
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
            tok = self.primary_tok
            if 'lang' in paragraph_tag.attrs:
                lang = paragraph_tag['lang']
                tok = self._get_tokenizer(lang)
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