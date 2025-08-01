"""A test program for the ChineseTokenizer.

This tests the ChineseTokenizer against some sample Chinese text. Prints the
original text, followed by three lists of tokens; the raw, stemmed, and
filtered tokens, respectively.

Imports the local context module, and the ChineseTokenizer from the local
tokenizer module.

Useage
------
python3 chinese_test.py
"""

from context import tokenizers
from tokenizers.chinese_tokenizer import ChineseTokenizer

if __name__ == '__main__':
    zh_tok = ChineseTokenizer()
    text = """
    他们在哪儿？
    你好，我叫小马。
    你的朋友在哪儿？他在看电影。
    你的儿子在哪儿？他去了商店。
    你的妈妈在哪儿？我的妈妈在我的后面。
    你的狗在哪儿？我的狗在桌子下睡觉。
    你的椅子在哪儿？我的椅子在桌子前面。
    """
    print("---Original text---")
    print(text)
    print("---Raw tokens---")
    print(zh_tok.get_raw_token_list(text))
    print("---Stemmed tokens---")
    print(zh_tok.get_stemmed_token_list(text))
    print("---Filtered tokens---")
    print(zh_tok.get_filtered_token_list(text))