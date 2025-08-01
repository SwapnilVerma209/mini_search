"""A test program for the SpanishTokenizer.

This tests the SpanishTokenizer against some sample Spanish text. Prints the
original text, followed by three lists of tokens; the raw, stemmed, and
filtered tokens, respectively.

Imports the local context module, and the SpanishTokenizer from the local
tokenizer module.

Useage
------
python3 spanish_test.py
"""

from context import tokenizers
from tokenizers.spanish_tokenizer import SpanishTokenizer

if __name__ == '__main__':
    esp_tok = SpanishTokenizer()
    text = """
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
    print("---Original text---")
    print(text)
    print("---Raw tokens---")
    print(esp_tok.get_raw_token_list(text))
    print("---Stemmed tokens---")
    print(esp_tok.get_stemmed_token_list(text))
    print("---Filtered tokens---")
    print(esp_tok.get_filtered_token_list(text))