import os
import sys

import nltk
from nltk import word_tokenize
from nltk.stem.snowball import ArabicStemmer
from nltk.corpus import stopwords

from tokenizer import Tokenizer

nltk_path = os.path.abspath('../../nltk')
if nltk_path not in nltk.data.path:
    nltk.data.path.append(nltk_path)
nltk.download('punkt_tab', download_dir=nltk_path)
nltk.download('stopwords', download_dir=nltk_path)

class ArabicTokenizer(Tokenizer):
    stops = set(stopwords.words('arabic'))
    stemmer = ArabicStemmer()

    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        return word_tokenize(text, 'arabic')
    
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
    eng_tok = EnglishTokenizer()
    sentence = "The FitnessGram Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly but gets faster each minute after you hear this signal bodeboop. A sing lap should be completed every time you hear this sound. ding Remember to run in a straight line and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark. Get ready!… Start. ding"
    print("---Raw tokens---")
    print(eng_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(eng_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(eng_tok.get_filtered_token_list(sentence))

