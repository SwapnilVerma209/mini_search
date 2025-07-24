import os
import nltk

modual_dir = os.path.dirname(__file__)
nltk_path = os.path.join(modual_dir, 'nltk')
nltk.data.path.append(nltk_path)
nltk.download('punkt_tab', download_dir=nltk_path)
nltk.download('stopwords', download_dir=nltk_path)

__all__ = ['english_tokenizer', 'chinese_tokenizer', 'hindi_tokenizer', \
        'spanish_tokenizer', 'arabic_tokenizer', 'generic_tokenizer']

from . import english_tokenizer
from . import chinese_tokenizer
from . import hindi_tokenizer
from . import spanish_tokenizer
from . import arabic_tokenizer
from . import generic_tokenizer