"""A test program for the ArabicTokenizer.

This tests the ArabicTokenizer against some sample Arabic text. Prints the
original text, followed by three lists of tokens; the raw, stemmed, and
filtered tokens, respectively.

Imports the local context module, and the ArabicTokenizer from the local
tokenizer module.

Useage
------
python3 arabic_test.py
"""

from context import tokenizers
from tokenizers.arabic_tokenizer import ArabicTokenizer

if __name__ == '__main__':
    arb_tok = ArabicTokenizer()
    text = """
    غُرْفَتِي مُرَتَّبَةٌ ومُرِيحَة. في غُرْفَتِي سَرِيرٌ كَبِيرٌ وخَزَانَةٌ
    لِلْمَلابِس. بِجانِب السَّريرِ طاولةٌ صَغِيرةٌ عَلَيها مَصْباحٌ وكُتُبٌ.
    لَدَيَّ أيْضاً مَكْتَبٌ لِلدِّراسَة، حَيْثُ أقْضِي وَقْتِي في القِراءَة
    والكِتابَة. عَلَى الجِدارِ صُوَرٌ لِعائِلَتِي وأصْدِقائِي. النَّافِذَةُ
    الكَبِيرَةُ تُطِلُّ عَلَى الحَديقَة، حَيْثُ أستَمْتِعُ بِمُشاهَدَةِ
    الطَّيْورِ والأشْجارِ. أحِبُّ غُرْفَتِي كَثِيراً لأنَّها تُشْعِرُنِي
    بِالرَّاحَةِ والسَّعادَة.
    """
    print("---Original text---")
    print(text)
    print("---Raw tokens---")
    print(arb_tok.get_raw_token_list(text))
    print("---Stemmed tokens---")
    print(arb_tok.get_stemmed_token_list(text))
    print("---Filtered tokens---")
    print(arb_tok.get_filtered_token_list(text))