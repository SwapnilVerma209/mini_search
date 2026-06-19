"""Unit tests for the Parser class.

Tests use synthetic HTML injected directly into parser.soup so that no
network requests are made.  Each test verifies:
  - the correct number of title / header / paragraph / anchor elements
  - the correct tokenizer is selected based on 'lang' attributes
    (own attribute, inherited from ancestor, or absent entirely)
"""

import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

from context import parser, webpage
from parser import Parser
from webpage import Webpage


def make_parser(html: str) -> Parser:
    """Return a Parser whose soup is built from *html* without any HTTP call."""
    p = Parser(user_agent='test')
    p.url = 'http://example.com/'
    p.soup = BeautifulSoup(html, 'html.parser')
    return p


# ---------------------------------------------------------------------------
# Helper – which tokenizer class is actually used?
# ---------------------------------------------------------------------------

def tokenizer_name(tok) -> str:
    return type(tok).__name__


# ---------------------------------------------------------------------------
# Title tests
# ---------------------------------------------------------------------------

class TestGetTitleTokens(unittest.TestCase):

    def test_no_head(self):
        p = make_parser('<body><p>Hello</p></body>')
        self.assertEqual(p.get_title_tokens(), {})

    def test_no_title_element(self):
        p = make_parser('<html><head></head><body></body></html>')
        self.assertEqual(p.get_title_tokens(), {})

    def test_english_title(self):
        p = make_parser('<html lang="en"><head><title>The quick brown fox</title></head></html>')
        tokens = p.get_title_tokens()
        self.assertIsInstance(tokens, dict)
        self.assertGreater(len(tokens), 0)

    def test_spanish_title_own_lang(self):
        # title has its own lang attribute
        p = make_parser(
            '<html lang="en"><head>'
            '<title lang="es">El idioma español</title>'
            '</head></html>'
        )
        tok = p._get_tokenizer(p.soup.head.title)
        self.assertEqual(tokenizer_name(tok), 'SpanishTokenizer')

    def test_chinese_title_inherited(self):
        # lang on <html>, no lang on <title>
        p = make_parser(
            '<html lang="zh"><head><title>汉语</title></head></html>'
        )
        tok = p._get_tokenizer(p.soup.head.title)
        self.assertEqual(tokenizer_name(tok), 'ChineseTokenizer')

    def test_unknown_lang_uses_generic(self):
        p = make_parser(
            '<html lang="fr"><head><title>Le français</title></head></html>'
        )
        tok = p._get_tokenizer(p.soup.head.title)
        self.assertEqual(tokenizer_name(tok), 'GenericTokenizer')

    def test_no_lang_uses_generic(self):
        p = make_parser('<html><head><title>No language set</title></head></html>')
        tok = p._get_tokenizer(p.soup.head.title)
        self.assertEqual(tokenizer_name(tok), 'GenericTokenizer')


# ---------------------------------------------------------------------------
# Header tests
# ---------------------------------------------------------------------------

class TestGetHeaderTokens(unittest.TestCase):

    def _html_with_headers(self, *tags):
        body = ''.join(f'<{t}>text</{t}>' for t in tags)
        return f'<html lang="en"><body>{body}</body></html>'

    def test_result_has_seven_slots(self):
        # index 0 is None, indices 1-6 correspond to h1-h6
        p = make_parser('<html><body></body></html>')
        result = p.get_header_tokens()
        self.assertEqual(len(result), 7)
        self.assertIsNone(result[0])

    def test_counts_each_level(self):
        html = (
            '<html lang="en"><body>'
            '<h1>A</h1><h1>B</h1>'
            '<h2>C</h2>'
            '<h3>D</h3><h3>E</h3><h3>F</h3>'
            '</body></html>'
        )
        p = make_parser(html)
        result = p.get_header_tokens()
        self.assertEqual(len(result[1]), 2)   # h1
        self.assertEqual(len(result[2]), 1)   # h2
        self.assertEqual(len(result[3]), 3)   # h3
        self.assertEqual(len(result[4]), 0)   # h4 – none present
        self.assertEqual(len(result[5]), 0)
        self.assertEqual(len(result[6]), 0)

    def test_header_own_lang_arabic(self):
        html = (
            '<html lang="en"><body>'
            '<h1 lang="ar">مرحبا</h1>'
            '</body></html>'
        )
        p = make_parser(html)
        h1 = p.soup.find('h1')
        tok = p._get_tokenizer(h1)
        self.assertEqual(tokenizer_name(tok), 'ArabicTokenizer')

    def test_header_inherits_lang_from_section(self):
        # lang set on a <section>, not directly on the header
        html = (
            '<html lang="en"><body>'
            '<section lang="hi"><h2>हिन्दी</h2></section>'
            '</body></html>'
        )
        p = make_parser(html)
        h2 = p.soup.find('h2')
        tok = p._get_tokenizer(h2)
        self.assertEqual(tokenizer_name(tok), 'HindiTokenizer')

    def test_header_no_lang_falls_back_to_generic(self):
        html = '<html><body><h1>No language</h1></body></html>'
        p = make_parser(html)
        h1 = p.soup.find('h1')
        tok = p._get_tokenizer(h1)
        self.assertEqual(tokenizer_name(tok), 'GenericTokenizer')

    def test_header_lang_overrides_ancestor(self):
        # ancestor says English; header itself says Spanish
        html = (
            '<html lang="en"><body>'
            '<h1 lang="es">Hola mundo</h1>'
            '</body></html>'
        )
        p = make_parser(html)
        h1 = p.soup.find('h1')
        tok = p._get_tokenizer(h1)
        self.assertEqual(tokenizer_name(tok), 'SpanishTokenizer')


# ---------------------------------------------------------------------------
# Paragraph tests
# ---------------------------------------------------------------------------

class TestGetParagraphTokens(unittest.TestCase):

    def test_no_paragraphs(self):
        p = make_parser('<html lang="en"><body></body></html>')
        self.assertEqual(p.get_paragraph_tokens(), [])

    def test_count_paragraphs(self):
        html = (
            '<html lang="en"><body>'
            '<p>One</p><p>Two</p><p>Three</p>'
            '</body></html>'
        )
        p = make_parser(html)
        self.assertEqual(len(p.get_paragraph_tokens()), 3)

    def test_paragraph_own_lang_hindi(self):
        html = (
            '<html lang="en"><body>'
            '<p lang="hi">हिन्दी पाठ</p>'
            '</body></html>'
        )
        p = make_parser(html)
        para = p.soup.find('p')
        tok = p._get_tokenizer(para)
        self.assertEqual(tokenizer_name(tok), 'HindiTokenizer')

    def test_paragraph_inherits_lang_from_div(self):
        html = (
            '<html lang="en"><body>'
            '<div lang="zh"><p>中文段落</p></div>'
            '</body></html>'
        )
        p = make_parser(html)
        para = p.soup.find('p')
        tok = p._get_tokenizer(para)
        self.assertEqual(tokenizer_name(tok), 'ChineseTokenizer')

    def test_paragraph_no_lang_uses_generic(self):
        html = '<html><body><p>No language defined anywhere</p></body></html>'
        p = make_parser(html)
        para = p.soup.find('p')
        tok = p._get_tokenizer(para)
        self.assertEqual(tokenizer_name(tok), 'GenericTokenizer')

    def test_mixed_lang_paragraphs(self):
        html = (
            '<html lang="en"><body>'
            '<p>English paragraph</p>'
            '<p lang="ar">نص عربي</p>'
            '<p lang="es">Párrafo en español</p>'
            '</body></html>'
        )
        p = make_parser(html)
        paras = p.soup.find_all('p')
        self.assertEqual(len(paras), 3)
        self.assertEqual(tokenizer_name(p._get_tokenizer(paras[0])), 'EnglishTokenizer')
        self.assertEqual(tokenizer_name(p._get_tokenizer(paras[1])), 'ArabicTokenizer')
        self.assertEqual(tokenizer_name(p._get_tokenizer(paras[2])), 'SpanishTokenizer')

    def test_each_paragraph_is_independent_dict(self):
        html = (
            '<html lang="en"><body>'
            '<p>The cat sat</p>'
            '<p>On the mat</p>'
            '</body></html>'
        )
        p = make_parser(html)
        result = p.get_paragraph_tokens()
        self.assertEqual(len(result), 2)
        for d in result:
            self.assertIsInstance(d, dict)


# ---------------------------------------------------------------------------
# URL / anchor tests
# ---------------------------------------------------------------------------

class TestGetUrls(unittest.TestCase):

    def test_no_anchors(self):
        p = make_parser('<html><body><p>No links here</p></body></html>')
        self.assertEqual(p.get_urls(), [])

    def test_count_anchors(self):
        html = (
            '<html><body>'
            '<a href="http://a.com">A</a>'
            '<a href="http://b.com">B</a>'
            '<a href="http://c.com">C</a>'
            '</body></html>'
        )
        p = make_parser(html)
        self.assertEqual(len(p.get_urls()), 3)

    def test_absolute_url_unchanged(self):
        html = '<html><body><a href="http://example.org/page">link</a></body></html>'
        p = make_parser(html)
        urls = p.get_urls()
        self.assertIn('http://example.org/page', urls)

    def test_relative_url_converted(self):
        html = '<html><body><a href="/about">About</a></body></html>'
        p = make_parser(html)
        urls = p.get_urls()
        self.assertIn('http://example.com/about', urls)

    def test_relative_url_no_leading_slash(self):
        html = '<html><body><a href="contact.html">Contact</a></body></html>'
        p = make_parser(html)
        urls = p.get_urls()
        self.assertIn('http://example.com/contact.html', urls)

    def test_mixed_absolute_and_relative(self):
        html = (
            '<html><body>'
            '<a href="http://other.com/">External</a>'
            '<a href="/local">Local</a>'
            '</body></html>'
        )
        p = make_parser(html)
        urls = p.get_urls()
        self.assertEqual(len(urls), 2)
        self.assertIn('http://other.com/', urls)
        self.assertIn('http://example.com/local', urls)


# ---------------------------------------------------------------------------
# get_page_data tests
# ---------------------------------------------------------------------------

class TestGetPageData(unittest.TestCase):

    def test_returns_webpage_instance(self):
        html = (
            '<html lang="en"><head><title>My Page</title></head>'
            '<body><h1>Header</h1><p>A paragraph.</p>'
            '<a href="/link">Link</a></body></html>'
        )
        p = make_parser(html)
        result = p.get_page_data()
        self.assertIsInstance(result, Webpage)

    def test_url_stored_on_webpage(self):
        p = make_parser('<html lang="en"><body></body></html>')
        result = p.get_page_data()
        self.assertEqual(result.url, 'http://example.com/')

    def test_title_tokens_match_get_title_tokens(self):
        html = '<html lang="en"><head><title>Quick brown fox</title></head><body></body></html>'
        p = make_parser(html)
        self.assertEqual(p.get_page_data().title_tokens, p.get_title_tokens())

    def test_header_tokens_match_get_header_tokens(self):
        html = (
            '<html lang="en"><body>'
            '<h1>First</h1><h2>Second</h2>'
            '</body></html>'
        )
        p = make_parser(html)
        self.assertEqual(p.get_page_data().header_tokens, p.get_header_tokens())

    def test_paragraph_tokens_match_get_paragraph_tokens(self):
        html = (
            '<html lang="en"><body>'
            '<p>One</p><p>Two</p>'
            '</body></html>'
        )
        p = make_parser(html)
        self.assertEqual(p.get_page_data().paragraph_tokens, p.get_paragraph_tokens())

    def test_urls_match_get_urls(self):
        html = (
            '<html><body>'
            '<a href="http://a.com">A</a>'
            '<a href="/local">B</a>'
            '</body></html>'
        )
        p = make_parser(html)
        self.assertEqual(p.get_page_data().urls, p.get_urls())

    def test_empty_page(self):
        p = make_parser('<html><head></head><body></body></html>')
        result = p.get_page_data()
        self.assertEqual(result.title_tokens, {})
        self.assertEqual(result.header_tokens, [None, [], [], [], [], [], []])
        self.assertEqual(result.paragraph_tokens, [])
        self.assertEqual(result.urls, [])

    def test_header_tokens_structure(self):
        # Verify the 7-slot structure is preserved in the Webpage
        html = '<html lang="en"><body><h1>A</h1><h3>B</h3></body></html>'
        p = make_parser(html)
        result = p.get_page_data()
        self.assertEqual(len(result.header_tokens), 7)
        self.assertIsNone(result.header_tokens[0])
        self.assertEqual(len(result.header_tokens[1]), 1)  # one h1
        self.assertEqual(len(result.header_tokens[3]), 1)  # one h3

    def test_paragraph_count_preserved(self):
        html = (
            '<html lang="en"><body>'
            '<p>A</p><p>B</p><p>C</p>'
            '</body></html>'
        )
        p = make_parser(html)
        self.assertEqual(len(p.get_page_data().paragraph_tokens), 3)

    def test_url_count_preserved(self):
        html = (
            '<html><body>'
            '<a href="http://x.com">X</a>'
            '<a href="http://y.com">Y</a>'
            '</body></html>'
        )
        p = make_parser(html)
        self.assertEqual(len(p.get_page_data().urls), 2)


# ---------------------------------------------------------------------------
# Language resolution edge cases
# ---------------------------------------------------------------------------

class TestLanguageResolution(unittest.TestCase):

    def test_hindi_latin_tag(self):
        # A BCP-47 tag that maps to Hindi (Latin) should use HindiLatinTokenizer
        # Find an actual tag that maps to Hindi Latin via bcp47 — use the
        # language_dict directly rather than relying on a specific BCP-47 string.
        hindi_latin_tags = [
            tag for tag, lang in Parser.language_dict.items()
            if lang == 'Hindi (Latin)'
        ]
        if not hindi_latin_tags:
            self.skipTest('No Hindi (Latin) BCP-47 tag found in language_dict')
        tag_str = hindi_latin_tags[0]
        html = f'<html lang="{tag_str}"><body><p>text</p></body></html>'
        p = make_parser(html)
        para = p.soup.find('p')
        tok = p._get_tokenizer(para)
        self.assertEqual(tokenizer_name(tok), 'HindiLatinTokenizer')

    def test_unsupported_lang_tag_uses_generic(self):
        # 'ja' (Japanese) is not a supported language
        html = '<html lang="ja"><body><p>テスト</p></body></html>'
        p = make_parser(html)
        para = p.soup.find('p')
        tok = p._get_tokenizer(para)
        self.assertEqual(tokenizer_name(tok), 'GenericTokenizer')

    def test_deep_ancestor_lang_inherited(self):
        # lang is set three levels above the <p>
        html = (
            '<html lang="es"><body>'
            '<article><section><div><p>texto</p></div></section></article>'
            '</body></html>'
        )
        p = make_parser(html)
        para = p.soup.find('p')
        tok = p._get_tokenizer(para)
        self.assertEqual(tokenizer_name(tok), 'SpanishTokenizer')

    def test_closer_ancestor_wins(self):
        # html says English, but a closer div says Arabic
        html = (
            '<html lang="en"><body>'
            '<div lang="ar"><p>نص</p></div>'
            '</body></html>'
        )
        p = make_parser(html)
        para = p.soup.find('p')
        tok = p._get_tokenizer(para)
        self.assertEqual(tokenizer_name(tok), 'ArabicTokenizer')


if __name__ == '__main__':
    unittest.main()
