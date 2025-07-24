from context import tokenizers
from tokenizers.english_tokenizer import EnglishTokenizer

if __name__ == '__main__':
    eng_tok = EnglishTokenizer()
    sentence = "The FitnessGram Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly but gets faster each minute after you hear this signal bodeboop. A sing lap should be completed every time you hear this sound. ding Remember to run in a straight line and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark. Get ready!… Start. ding"
    print("---Raw tokens---")
    print(eng_tok.get_raw_token_list(sentence))
    print("---Stemmed tokens---")
    print(eng_tok.get_stemmed_token_list(sentence))
    print("---Filtered tokens---")
    print(eng_tok.get_filtered_token_list(sentence))