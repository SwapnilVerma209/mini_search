from .tokenizer import Tokenizer

class GenericTokenizer(Tokenizer):
    def __init__(self):
        pass

    def get_raw_token_list(self, text: str) -> list:
        text = "".join(text.split())
        raw_token_list = []
        for i in range(len(text) - 1):
            token = text[i:i+2].lower()
            raw_token_list.append(token)
        return raw_token_list
    
    def get_stemmed_token_list(self, text: str) -> list:
        return self.get_raw_token_list(text)
    
    def get_filtered_token_list(self, text: str) -> list:
        return self.get_raw_token_list(text)