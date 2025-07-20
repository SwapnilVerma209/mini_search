import requests
import sys
import unicodedata
from urllib.parse import urljoin

import nltk
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from zh_sentence.tokenizer import tokenize as zh_tokenize

nltk.data.path.append('../nltk')
nltk.download('punkt_tab', download_dir='../nltk')
nltk.download('stopwords', download_dir='../nltk')

class Parser:
    stops = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    def __init__(self, url: str):
        self.reset(url)

    def reset(self, url: str) -> void:
        self.url = url
        self._make_soup()

    def _get_html(self) -> str:
        response = requests.get(self.url)
        return response.text

    def _make_soup(self) -> void:
        html = self._get_html()
        self.soup = BeautifulSoup(html, 'html.parser')

    def _is_punctuation(string: str) -> bool:
        if len(string) != 1:
            return False
        return unicodedata.category(string[0]).startswith("P")

    def _get_tokens(string: str) -> dict:
        tokens = word_tokenize(string)
        for i in range(len(tokens)):
            token = tokens[i]
            tokens[i] = stemmer.stem(token)
        filtered_tokens = {}
        for i in range(len(tokens)):
            token = tokens[i]
            if _is_punctuation(token):
                continue
            if token in stops:
                continue
            if token not in filtered_tokens:
                filtered_tokens[token] = [i]
            else:
                filtered_tokens[token].append(i)
        return filtered_tokens

    def get_title_tokens(soup: BeautifulSoup) -> dict:
        return _get_tokens(soup.head.title.string)

    def _get_hn_tokens(soup: BeautifulSoup, n: int) -> list:
        if n < 1 or n > 6:
            return []
        header_type = 'h%d' % n
        header_tokens = []
        for header in soup.find_all(header_type):
            header_tokens.append(_get_tokens(header.text))
        return header_tokens

    def get_header_tokens(soup: BeautifulSoup) -> list:
        header_tokens = [None]
        for i in range(1, 7):
            header_tokens.append(_get_hn_tokens(soup, i))
        return header_tokens

    def get_paragraph_tokens(soup: BeautifulSoup) -> list:
        paragraph_tokens = []
        for paragraph in soup.find_all('p'):
            paragraph_tokens.append(_get_tokens(paragraph.text))
        return paragraph_tokens

    def get_urls(base: str, soup: BeautifulSoup) -> list:
        urls = []
        for anchor in soup.find_all('a'):
            url = anchor.get('href')
            url = urljoin(base, url)
            urls.append(url)
        return urls

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <url>', file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    html = _get_html(url)
    soup = _make_soup(html)
    title_tokens = get_title_tokens(soup)
    print()
    print('---Title Tokens---')
    print(title_tokens)
    print()
    header_tokens = get_header_tokens(soup)
    print('---Header Tokens---')
    print(header_tokens)
    print()
    paragraph_tokens = get_paragraph_tokens(soup)
    print('---Paragraph Tokens---')
    print(paragraph_tokens)
    print()
    urls = get_urls(url, soup)
    print('---URLs---')
    print(urls)
    print()
    sys.exit(0)