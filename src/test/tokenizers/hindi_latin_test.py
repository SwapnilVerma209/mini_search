"""A test program for the HindiLatinTokenizer.

This tests the HindiLatinTokenizer against some sample Hindi text. Prints the
original text, followed by three lists of tokens; the raw, stemmed, and
filtered tokens, respectively.

Imports the local context module, and the HindiLatinTokenizer from the local
tokenizer module.

Useage
------
python3 hindi_latin_test.py
"""

from context import tokenizers
from tokenizers.hindi_latin_tokenizer import HindiLatinTokenizer

if __name__ == '__main__':
    hi_tok = HindiLatinTokenizer()
    text = """
    Ek baar kee baat hai. Ek riyaasat ke mantree ne raaja ko apanee betee ke
    vivaah samaaroh mein nimantrit kiya. Jab raaja apane parivaar ke saath
    vivaah samaaroh mein pahuncha, to mantree unhen sammaanapoorvak vishisht
    aasan par baithaane le gayo, to mantree yah dekhakar bahut lajjit hua ki ek
    saphaeekarmee vahaan baitha hua tha.
    """
    print("---Original text---")
    print(text)
    print("---Raw tokens---")
    print(hi_tok.get_raw_token_list(text))
    print("---Stemmed tokens---")
    print(hi_tok.get_stemmed_token_list(text))
    print("---Filtered tokens---")
    print(hi_tok.get_filtered_token_list(text))