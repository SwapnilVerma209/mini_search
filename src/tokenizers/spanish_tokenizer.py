import os
import sys

import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SpanishStemmer
from nltk.corpus import stopwords

from tokenizer import Tokenizer

nltk_path = os.path.abspath('../../nltk')
if nltk_path not in nltk.data.path:
    nltk.data.path.append(nltk_path)
nltk.download('punkt_tab', download_dir=nltk_path)
nltk.download('stopwords', download_dir=nltk_path)

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

if __name__ == '__main__':
    esp_tok = SpanishTokenizer()
    sentence = """
    Yo vivo en Granada, una ciudad pequeña que tiene monumentos muy importantes
    como la Alhambra. Aquí la comida es deliciosa y son famosos el gazpacho, el
    rebujito y el salmorejo.

    Mi nueva casa está en una calle ancha que tiene muchos árboles. El piso de
    arriba de mi casa tiene tres dormitorios y un despacho para trabajar. El
    piso de abajo tiene una cocina muy grande, un comedor con una mesa y seis
    sillas, un salón con dos sofás verdes, una televisión y cortinas. Además,
    tiene una pequeña terraza con piscina donde puedo tomar el sol en verano.

    Me gusta mucho mi casa porque puedo invitar a mis amigos a cenar o a ver el
    fútbol en mi televisión. Además, cerca de mi casa hay muchas tiendas para
    hacer la compra, como panadería, carnicería y pescadería.
    """
    print("---Raw tokens---")
    print(esp_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(esp_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(esp_tok.get_filtered_token_list(sentence))

