"""A test program for the GenericTokenizer.

This tests the GenericTokenizer against some sample text of an unsupported
language (in this case, French). Prints the original text, followed by three
lists of tokens; the raw, stemmed, and filtered tokens, respectively.

Imports the local context module, and the GenericTokenizer from the local
tokenizer module.

Useage
------
python3 generic_test.py
"""

from context import tokenizers
from tokenizers.generic_tokenizer import GenericTokenizer

if __name__ == '__main__':
    gen_tok = GenericTokenizer()
    text = """
    Les vacances d’été sont appelées « les grandes vacances » car elles durent
    deux mois entiers. C’est l’occasion pour beaucoup de familles françaises de
    partir à la mer. Et en France, on a le choix entre la mer Méditerranée au
    sud, la côte atlantique à l’ouest, la Manche et la mer du Nord. Ma tante
    apprécie beaucoup la Bretagne car il n’y fait pas trop chaud : le soleil
    tape moins fort qu’au sud.
    """
    print("---Original text---")
    print(text)
    print("---Raw tokens---")
    print(gen_tok.get_raw_token_list(text))
    print("---Stemmed tokens---")
    print(gen_tok.get_stemmed_token_list(text))
    print("---Filtered tokens---")
    print(gen_tok.get_filtered_token_list(text))