import os
import sys

import nltk
from nltk.stem.snowball import ArabicStemmer
from nltk.tokenize.regexp import wordpunct_tokenize
from nltk.corpus import stopwords

from tokenizer import Tokenizer

nltk_path = os.path.abspath('../../nltk')
if nltk_path not in nltk.data.path:
    nltk.data.path.append(nltk_path)
nltk.download('stopwords', download_dir=nltk_path)

class ArabicTokenizer(Tokenizer):
    stops = set(stopwords.words('arabic'))
    stemmer = ArabicStemmer()

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        return wordpunct_tokenize(text)
    
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

if __name__ == '__main__':
    arb_tok = ArabicTokenizer()
    sentence = """
    الروتين اليومي

يبدأ يومي بالاستيقاظ مبكرًا لأداء صلاة الفجر. بعد ذلك، أتناول الإفطار وأشرب القهوة قبل الذهاب إلى العمل. أعمل لمدة ثماني ساعات وأتناول الغداء في المكتب. بعد العمل، أذهب إلى النادي لممارسة الرياضة. أعود إلى المنزل لتناول العشاء مع العائلة وأقضي بعض الوقت في القراءة قبل النوم.
    """
    print("---Raw tokens---")
    print(arb_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(arb_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(arb_tok.get_filtered_token_list(sentence))

