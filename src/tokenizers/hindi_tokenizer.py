import os
import subprocess
import sys

from stopwords_hindi import hindi_sw
from indicnlp.tokenize import indic_tokenize

from tokenizer import Tokenizer


class HindiTokenizer(Tokenizer):
    stops = hindi_sw.get_hindi_sw()

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        return trivial_tokenize(text)
    
    def get_stemmed_token_list(self, text: str) -> list:
        return self.get_raw_token_list(text)
    
    def get_filtered_token_list(self, text: str) -> list:
        stemmed_token_list = self.get_stemmed_token_list(text)
        filtered_token_list = []
        for token in stemmed_token_list:
            if self._is_punctuation(token) or token in self.stops:
                continue
            filtered_token_list.append(token)
        return filtered_token_list

if __name__ == '__main__':
    zh_tok = ChineseTokenizer()
    sentence = """
    
    """
    print("---Raw tokens---")
    print(zh_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(zh_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(zh_tok.get_filtered_token_list(sentence))