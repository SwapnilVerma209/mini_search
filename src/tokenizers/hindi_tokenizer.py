import snowballstemmer
from stopwords_hindi import hindi_sw
from indicnlp.tokenize import indic_tokenize

from .tokenizer import Tokenizer

class HindiTokenizer(Tokenizer):
    stops = hindi_sw.get_hindi_sw()
    stemmer = snowballstemmer.stemmer('hindi')

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        token_list = indic_tokenize.trivial_tokenize(text)
        raw_token_list = []
        for i in range(len(token_list)):
            token = token_list[i].strip()
            if len(token) == 0:
                continue
            raw_token_list.append(token)
        return raw_token_list

    def get_stemmed_token_list(self, text: str) -> list:
        raw_token_list = self.get_raw_token_list(text)
        return self.stemmer.stemWords(raw_token_list)
    
    def get_filtered_token_list(self, text: str) -> list:
        stemmed_token_list = self.get_stemmed_token_list(text)
        filtered_token_list = []
        for token in stemmed_token_list:
            if self._is_punctuation(token) or token in self.stops:
                continue
            filtered_token_list.append(token)
        return filtered_token_list