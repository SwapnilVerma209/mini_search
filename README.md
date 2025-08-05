# mini_search

This is a work-in-progress web search engine written in Python. It is intended
to be relatively lightweight space-wise, so that the barrier to self-hosting is
low. The tradeoff is that this search engine will be barebones compared to a
more established search engine like Google.

## Special Thanks

- [NLTK](https://www.nltk.org/)
- [chinese](https://github.com/morinokami/chinese)
- [LiHiSTO](https://github.com/semicolon123/LiHiSTO) (see [citations](docs/citations.bib))
- [Indic NLP Library](https://github.com/anoopkunchukuttan/indic_nlp_library)
(see [citations](docs/citations.bib))
- [Requests](https://requests.readthedocs.io/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## Current Progress

So far, the HTML parsing, tokenization, stemming, and stopword and
punctuation filtering has been implemented. Work on the crawler and the
querying client/server still needs to be done.

The HTML parser downloads the contents of the webpage, and selects a tokenizer
based on the language attribute of the page's HTML. Then, it can generate the
title, header, and paragraph tokens on-demand. If any of those elements have a
language attribute of their own, then a tokenizer is selected for them. The
parser can also generate a list of the absolute URLs for the links on the
page.

If you find something wrong with any of the tokenizers, please let me know
(especially for the Chinese and Arabic tokenizers).

## Supported Languages
- English
- 官话/官話 (Mandarin Chinese)
- हिन्दी (Hindi)
- Español/Castellano (Spanish/Castilian)
- العربية الفصحى الحديثة (Standard Arabic)

### Note on Non-supported Languages
There is a generic tokenizer used for languages other than the supported ones.
This strips whitespace characters and generates character bigrams. While it is
expected to work with almost all languages, it is very space inefficient
compared to the specialized tokenizers for the above languages. Because of
this, it should only be used as a last resort.

## Installing
1. Clone this repository.
2. Change directory to the root of the cloned repository.
3. Create a python3 virtual environment with: `python3 -m venv <dirname>`.
4. Activate the virtual enviroment with:
    - For POSIX systems (bash/zsh): `source <dirname>/bin/activate`
    - For Windows systems:
        - cmd.exe: `C:\> <dirname>\Scripts\activate.bat`
        - PowerShell: `PS C:\> <dirname>\Scripts\Activate.ps1`
    Where dirname is the name of your virtual environment's directory (you
    created this in step 3).
5. Install dependencies with `pip install -r requirements.txt`.

## Usage

### HTML Parser
If you are using the [HTML parser](src/parser.py), be sure to have Requests and
Beautiful Soup 4 installed. In addition, have the tokenizers package in the
same directory.

You can create a new Parser object as follows:
```
from parser import Parser

p = Parser()
```

To download and parse the contents of a webpage, pass the URL into the Parser
object:
```
url = 'https://www.website.com'
p.set_url(url)
```

From there, you can get dictionaries of the token's occurrences in the title,
each header, and each paragraph:
```
title_tokens = p.get_title_tokens()
header_tokens = p.get_header_tokens()
paragraph_tokens = p.get_paragraph_tokens()
```

`title_tokens['apple']` will return the word indices for the token 'apple'
within the page's title element. `header_tokens[2][3]['apple']` will return
the word indices for the token 'apple' for the third h2 element on the page,
assuming it exists. `paragraph_tokens[3]['apple']` will return the word indices
for the token 'apple' in the third paragraph element, assuming it exists.

You can also get a list of all the URLs the page links to:
```
out_urls = p.get_urls()
```

To parse another page, just call `set_url()` on the same object with the new
URL:
```
new_url = 'https://www.secondwebsite.com'
p.set_url(new_url)
```

### Tokenizers
Included in the project is a package, tokenizers/. It contains modules for
several tokenizers. There is an abstract base tokenizer class (in
tokenizer.py). This is not meant to be instantiated. There is one tokenizer
class for every supported language, each in its own module. Finally, there is a
[generic tokenizer](src/tokenizers/generic_tokenizer.py) meant for
non-supported languages. This removes whitespaces and splits text into
character bigrams. Only use this one as a last resort, since it is space
inefficient. For the following example, only the
[English tokenizer](src/tokenizers/english_tokenizer.py) is shown, but all of
them have the same interface.

To create a new EnglishTokenizer:
```
from tokenizers.english_tokenizer import EnglishTokenizer

en_tok = EnglishTokenizer()
```

With this tokenizer, you can pass English text into its public methods to get
tokens at different levels of processing, and either as a list or a dict. The
list will simply have each token as one item in the order it appears in the
text. The dict will have each unique token as keys, and the value is a list of
the tokens' indices if they were in list form.

#### Raw Tokens
Raw tokens are tokens without any changes made to the text; no case
normalization, no stemming, no filtering of stopwords or standalone
punctuation. 

##### List form
```
sentence = 'If it looks like a duck and quacks like a duck, it is a duck.'
token_list = en_tok.get_raw_token_list(sentence)  # ['If', 'it', 'looks', \
        'like', 'a', 'duck', 'and', 'quacks', 'like', 'a', 'duck', ',', 'it', \
        'is', 'a', 'duck', '.']
```

##### Dict form
```
sentence = 'If it looks like a duck and quacks like a duck, it is a duck.'
token_dict = en_tok.get_raw_token_dict(sentence)  # {'If': [0], 'it': [1, 12], \
        'looks': [2], 'like': [3, 8], 'a': [4, 9, 14], 'duck': [5, 10, 15], \
        'and': [6], 'quacks': [7], ',': [11], 'is': [13], '.': [16]}
```

#### Stemmed Tokens
Stemmed tokens have words changed to their base form (i.e. running -> run). All
casing is normalized (changed to lowercase). No filtering of stopwords or
standalone punctuation is done.

NOTE: For Chinese, the results will be identical to the raw tokens. Chinese has
very little morphology, so stemming is not necessary.

NOTE: For the generic tokenizer, this is identical to the raw tokens.

##### List form
```
sentence = 'If it looks like a duck and quacks like a duck, it is a duck.'
token_list = en_tok.get_stemmed_token_list(sentence)  # ['if', 'it', 'look', \
        'like', 'a', 'duck', 'and', 'quack', 'like', 'a', 'duck', ',', 'it', \
        'is', 'a', 'duck', '.']
```

##### Dict form
```
sentence = 'If it looks like a duck and quacks like a duck, it is a duck.'
token_dict = en_tok.get_stem_token_dict(sentence)  # {'if': [0], \
        'it': [1, 12], 'look': [2], 'like': [3, 8], 'a': [4, 9, 14], \
        'duck': [5, 10, 15], 'and': [6], 'quack': [7], ',': [11], 'is': [13], \
        '.': [16]}
```

#### Filtered Tokens
Filtered tokens are stemmed, and have stopwords and standalone punctuation
removed. For English, stopwords include "the", "a", "and", etc. Standalone
punctuation is defined as tokens of length 1 that only contain punctuation.

NOTE: For the generic tokenizer, this is identical to the raw tokens.

##### List form
```
sentence = 'If it looks like a duck and quacks like a duck, it is a duck.'
token_list = en_tok.get_filtered_token_list(sentence)  # ['look', 'like', \
        'duck', 'quack', 'like', 'duck', 'duck']
```

##### Dict form
```
sentence = 'If it looks like a duck and quacks like a duck, it is a duck.'
token_dict = en_tok.get_stem_filtered_dict(sentence)  # {'look': [0], \
        'like': [1, 4], 'duck': [2, 5, 6], 'quack': [3]}
```