import os
import sys

from chinese import ChineseAnalyzer
import nltk
from nltk.corpus import stopwords

from tokenizer import Tokenizer

nltk_path = os.path.abspath('../../nltk')
if nltk_path not in nltk.data.path:
    nltk.data.path.append(nltk_path)
nltk.download('stopwords', download_dir=nltk_path)

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

if __name__ == '__main__':
    zh_tok = ChineseTokenizer()
    sentence = """
    他们在哪儿？
    你好，我叫小马。
    你的朋友在哪儿？他在看电影。
    你的儿子在哪儿？他去了商店。
    你的妈妈在哪儿？我的妈妈在我的后面。
    你的狗在哪儿？我的狗在桌子下睡觉。
    你的椅子在哪儿？我的椅子在桌子前面。
    """
    print("---Raw tokens---")
    print(zh_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(zh_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(zh_tok.get_filtered_token_list(sentence))