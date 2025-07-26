import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from tokenizers import *

class Parser:
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
        if lang in self.tokenizer_dict:
            return self.tokenizer_dict[lang]
        return self.gen_tokenizer

    def set_url(self, url: str) -> None:
        self.url = url
        self._make_soup()
        self.primary_tok = self.gen_tokenizer
        if 'lang' in self.soup.html.attrs:
            primary_lang = self.soup.html['lang']
            self.primary_tok = self._get_tokenizer(primary_lang)

    def _get_html(self) -> str:
        response = requests.get(self.url)
        return response.text

    def _make_soup(self) -> None:
        html = self._get_html()
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_title_tokens(self) -> dict:
        title_tag = self.soup.head.title
        tok = self.primary_tok
        if 'lang' in title_tag.attrs:
            lang = title_tag['lang']
            tok = self._get_tokenizer(lang)
        title_text = title_tag.string
        return tok.get_filtered_token_dict(title_text)

    def _get_hn_tokens(self, n: int) -> list:
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
        header_tokens = [None]
        for i in range(1, 7):
            header_tokens.append(self._get_hn_tokens(i))
        return header_tokens

    def get_paragraph_tokens(self) -> list:
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
        urls = []
        for anchor in self.soup.find_all('a'):
            raw_url = anchor.get('href')
            abs_url = urljoin(self.url, raw_url)
            urls.append(abs_url)
        return urls