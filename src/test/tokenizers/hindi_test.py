from context import tokenizers
from tokenizers.hindi_tokenizer import HindiTokenizer

if __name__ == '__main__':
    hi_tok = HindiTokenizer()
    sentence = """
    एक बार की बात है। एक रियासत के मंत्री ने राजा को अपनी बेटी के विवाह समारोह
    में निमंत्रित किया। जब राजा अपने परिवार के साथ विवाह समारोह में पहुँचा, तो
    मंत्री उन्हें सम्मानपूर्वक विशिष्ट आसन पर बैठाने ले गयो, तो मंत्री यह देखकर
    बहुत लज्जित हुआ कि एक सफाईकर्मी वहाँ बैठा हुआ था।
    """
    print("---Raw tokens---")
    print(hi_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(hi_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(hi_tok.get_filtered_token_list(sentence))