import sys
from context import parser
from parser import Parser

site_dict = {
    'en': 'https://en.wikipedia.org/wiki/English_language',
    'zh': 'https://zh.wikipedia.org/wiki/%E6%B1%89%E8%AF%AD',
    'hi': 'https://hi.wikipedia.org/wiki/%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80',
    'es': 'https://es.wikipedia.org/wiki/Idioma_espa%C3%B1ol',
    'ar': 'https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%84%D8%BA%D8%A9_%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9_%D8%A7%D9%84%D9%81%D8%B5%D8%AD%D9%89_%D8%A7%D9%84%D8%AD%D8%AF%D9%8A%D8%AB%D8%A9'
}
default_url = 'https://fr.wikipedia.org/wiki/Fran%C3%A7ais'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s <language code>\n")
        sys.exit(1)
    lang_code = sys.argv[1]
    url = default_url
    if lang_code in site_dict:
        url = site_dict[lang_code]
    parser = Parser()
    parser.set_url(url)
    title_tokens = parser.get_title_tokens()
    print()
    print('---Title Tokens---')
    print(title_tokens)
    print()
    header_tokens = parser.get_header_tokens()
    print('---Header Tokens---')
    print(header_tokens)
    print()
    paragraph_tokens = parser.get_paragraph_tokens()
    print('---Paragraph Tokens---')
    print(paragraph_tokens)
    print()
    urls = parser.get_urls()
    print('---URLs---')
    print(urls)
    print()
    sys.exit(0)