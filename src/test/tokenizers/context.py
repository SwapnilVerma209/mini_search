"""A context file for the tokenizer tests.

Imports the python os and sys modules, and the local tokenizers package.
"""

import os
import sys
dirname = os.path.dirname(__file__)
rel_path = os.path.join(dirname, '../..')
abs_path = os.path.abspath(rel_path)
sys.path.insert(0, abs_path)

import tokenizers