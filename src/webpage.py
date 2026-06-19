class Webpage:
    """Contains the data of a webpage.

    Attributes
    ----------
    url : str
        The url to the webpage.
    title_tokens : dict
        A dictionary of the title's tokens.
    header_tokens: list
        A 2D list of header token dicts.
    paragraph_tokens : list
        A list of paragraph token dicts.
    urls : list
        A list of the page's urls.
    """
    def __init__(self, url: str, title_tokens: dict, header_tokens: list, \
            paragraph_tokens: list, urls: list):
        self.url = url
        self.title_tokens = title_tokens
        self.header_tokens = header_tokens
        self.paragraph_tokens = paragraph_tokens
        self.urls = urls