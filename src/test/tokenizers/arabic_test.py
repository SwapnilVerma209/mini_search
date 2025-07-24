from context import tokenizers
from tokenizers.arabic_tokenizer import ArabicTokenizer

if __name__ == '__main__':
    arb_tok = ArabicTokenizer()
    sentence = """
    الروتين اليومي

يبدأ يومي بالاستيقاظ مبكرًا لأداء صلاة الفجر. بعد ذلك، أتناول الإفطار وأشرب القهوة قبل الذهاب إلى العمل. أعمل لمدة ثماني ساعات وأتناول الغداء في المكتب. بعد العمل، أذهب إلى النادي لممارسة الرياضة. أعود إلى المنزل لتناول العشاء مع العائلة وأقضي بعض الوقت في القراءة قبل النوم.
    """
    print("---Raw tokens---")
    print(arb_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(arb_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(arb_tok.get_filtered_token_list(sentence))