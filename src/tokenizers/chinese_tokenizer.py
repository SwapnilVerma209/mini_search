from chinese import ChineseAnalyzer
import nltk
from nltk.corpus import stopwords

from .tokenizer import Tokenizer

class ChineseTokenizer(Tokenizer):
    stops = set(stopwords.words('chinese'))
    analyzer = ChineseAnalyzer()

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        text = ''.join(text.split())
        return self.analyzer.parse(text).tokens()
    
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