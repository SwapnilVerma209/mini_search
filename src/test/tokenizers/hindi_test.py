"""A test program for the HindiTokenizer.

This tests the HindiTokenizer against some sample Hindi text. Prints the
original text, followed by three lists of tokens; the raw, stemmed, and
filtered tokens, respectively.

Imports the local context module, and the HindiTokenizer from the local
tokenizer module.

Useage
------
python3 hindi_test.py
"""

from context import tokenizers
from tokenizers.hindi_tokenizer import HindiTokenizer

if __name__ == '__main__':
    hi_tok = HindiTokenizer()
    text = """
    एक बार की बात है। एक रियासत के मंत्री ने राजा को अपनी बेटी के विवाह समारोह
    में निमंत्रित किया। जब राजा अपने परिवार के साथ विवाह समारोह में पहुँचा, तो
    मंत्री उन्हें सम्मानपूर्वक विशिष्ट आसन पर बैठाने ले गयो, तो मंत्री यह देखकर
    बहुत लज्जित हुआ कि एक सफाईकर्मी वहाँ बैठा हुआ था।
    """
    print("---Original text---")
    print(text)
    print("---Raw tokens---")
    print(hi_tok.get_raw_token_list(text))
    print("---Stemmed tokens---")
    print(hi_tok.get_stemmed_token_list(text))
    print("---Filtered tokens---")
    print(hi_tok.get_filtered_token_list(text))