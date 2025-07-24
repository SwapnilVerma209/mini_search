from context import tokenizers
from tokenizers.generic_tokenizer import GenericTokenizer

if __name__ == '__main__':
    gen_tok = GenericTokenizer()
    sentence = """
    Les vacances d’été sont appelées « les grandes vacances » car elles durent
    deux mois entiers. C’est l’occasion pour beaucoup de familles françaises de
    partir à la mer. Et en France, on a le choix entre la mer Méditerranée au
    sud, la côte atlantique à l’ouest, la Manche et la mer du Nord. Ma tante
    apprécie beaucoup la Bretagne car il n’y fait pas trop chaud : le soleil
    tape moins fort qu’au sud.
    """
    print("---Raw tokens---")
    print(gen_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(gen_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(gen_tok.get_filtered_token_list(sentence))