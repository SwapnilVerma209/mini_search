import unicodedata
from abc import ABC, abstractmethod

class Tokenizer(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def _make_token_dict(self, token_list: list) -> dict:
        token_dict = {}
        for i in range(len(token_list)):
            token = token_list[i]
            if token in token_dict:
                token_dict[token].append(i)
            else:
                token_dict[token] = [i]
        return token_dict

    def _is_punctuation(self, text: str) -> bool:
        if len(text) != 1:
            return False
        return unicodedata.category(text[0]).startswith("P")

    @abstractmethod
    def get_raw_token_list(self, text: str) -> list:
        return None
    
    def get_raw_token_dict(self, text: str) -> dict:
        token_list = self.get_raw_token_list(text)
        return self._make_token_dict(token_list)
    
    @abstractmethod
    def get_stemmed_token_list(self, text: str) -> list:
        return None
    
    def get_stemmed_token_dict(self, text: str) -> dict:
        token_list = self.get_stemmed_token_list(text)
        return self._make_token_dict(token_list)

    @abstractmethod
    def get_filtered_token_list(self, text: str) -> list:
        return None
    
    def get_filtered_token_dict(self, text: str) -> dict:
        token_list = self.get_filtered_token_list(text)
        return self._make_token_dict(token_list)