"""Tokenizers

Imports the Python os library, nltk, and downloads the nltk tokenizer and
stopword data as dependencies.

Also imports the tokenizer modules:
    tokenizer
    english_tokenizer
    chinese_tokenizer
    hindi_tokenizer
    hindi_latin_tokenizer
    spanish_tokenizer
    arabic_tokenizer
    generic_tokenizer
"""

import os
import nltk

modual_dir = os.path.dirname(__file__)
nltk_path = os.path.join(modual_dir, 'nltk')
nltk.data.path.append(nltk_path)
nltk.download('punkt_tab', download_dir=nltk_path)
nltk.download('stopwords', download_dir=nltk_path)

__all__ = ['tokenizer', 'english_tokenizer', 'chinese_tokenizer', \
        'hindi_tokenizer', 'hindi_latin_tokenizer', 'spanish_tokenizer',
        'arabic_tokenizer', 'generic_tokenizer']

from . import tokenizer
from . import english_tokenizer
from . import chinese_tokenizer
from . import hindi_tokenizer
from . import hindi_latin_tokenizer
from . import spanish_tokenizer
from . import arabic_tokenizer
from . import generic_tokenizer