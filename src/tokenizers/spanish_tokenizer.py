import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SpanishStemmer
from nltk.corpus import stopwords

from .tokenizer import Tokenizer

class SpanishTokenizer(Tokenizer):
    stops = set(stopwords.words('spanish'))
    stemmer = SpanishStemmer()

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        return word_tokenize(text, 'spanish')
    
    def get_stemmed_token_list(self, text: str) -> list:
        stemmed_token_list = self.get_raw_token_list(text)
        for i in range(len(stemmed_token_list)):
            token = stemmed_token_list[i]
            stemmed_token_list[i] = self.stemmer.stem(token)
        return stemmed_token_list
    
    def get_filtered_token_list(self, text: str) -> list:
        stemmed_token_list = self.get_stemmed_token_list(text)
        filtered_token_list = []
        for token in stemmed_token_list:
            if self._is_punctuation(token) or token in self.stops:
                continue
            filtered_token_list.append(token)
        return filtered_token_list