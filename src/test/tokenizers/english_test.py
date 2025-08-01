"""A test program for the EnglishTokenizer.

This tests the EnglishTokenizer against some sample English text. Prints the
original text, followed by three lists of tokens; the raw, stemmed, and
filtered tokens, respectively.

Imports the local context module, and the EnglishTokenizer from the local
tokenizer module.

Useage
------
python3 english_test.py
"""

from context import tokenizers
from tokenizers.english_tokenizer import EnglishTokenizer

if __name__ == '__main__':
    eng_tok = EnglishTokenizer()
    text = """
    The FitnessGram Pacer Test is a multistage aerobic capacity test that
    progressively gets more difficult as it continues. The 20 meter pacer test
    will begin in 30 seconds. Line up at the start. The running speed starts
    slowly but gets faster each minute after you hear this signal bodeboop. A
    sing lap should be completed every time you hear this sound. ding Remember
    to run in a straight line and run as long as possible. The second time you
    fail to complete a lap before the sound, your test is over. The test will
    begin on the word start. On your mark. Get ready!… Start. ding
    """
    print("---Original text---")
    print(text)
    print("---Raw tokens---")
    print(eng_tok.get_raw_token_list(text))
    print("---Stemmed tokens---")
    print(eng_tok.get_stemmed_token_list(text))
    print("---Filtered tokens---")
    print(eng_tok.get_filtered_token_list(text))