"""Tokenizers

Imports the Python os library, nltk, and downloads the nltk tokenizer and
stopword data as dependencies. Also clones Anoop Kunchukuttan's Indic NLP
Resources.

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
import subprocess
import sys
import nltk
from indicnlp import common
from indicnlp import loader

# Download NLTK resources
module_dir = os.path.dirname(__file__)
nltk_path = os.path.join(module_dir, 'nltk')
nltk_path = os.path.abspath(nltk_path)
nltk.data.path.append(nltk_path)
nltk.download('punkt_tab', download_dir=nltk_path)
nltk.download('stopwords', download_dir=nltk_path)

# Download and load NLTK resources
tokenizers_path = os.path.abspath(module_dir)
INDIC_RESOURCES_PATH = os.path.join(tokenizers_path, 'indic_nlp_resources')
command = os.path.join(tokenizers_path, 'download_indic_resources')
match os.name:
    case "posix":
        command = command + '.sh %s' % tokenizers_path
    case "nt":
        command = command + '.cmd %s' % tokenizers_path
    case _:
        sys.stderr.write('ERROR: Unknown operating system\n')
        exit(1)
sub_proc = subprocess.Popen(command, shell=True)
sub_proc.wait()
common.set_resources_path(INDIC_RESOURCES_PATH)
loader.load()

# Import submodules
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