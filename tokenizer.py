import re

# List of regexes
regexes = [
    ['function', r'\bfunction\b'],
    ['print', r'\bconsole.log\b'],
    ['identifier', r'\b[a-zA-Z]+\b'],
    ['integer', r'\b[0-9]+\b'],
    ['oscope', r'\{'],
    ['cscope', r'\}'],
    ['oparen', r'\('],
    ['cparen', r'\)'],
    ['semicolon', r'\;'],
    ['comma', r'\,'],
]

class Tokenizer():
    def __init__(self, text):
        self.code = text

    def tokenize(self):
        tokens = []
        while self.code != "":
            tokens.append(self.tokenize_one())
            self.code = self.code.strip()
        return tokens

    def tokenize_one(self):
        for token, regex in regexes:
            regex = rf"\A{regex}"
            match = re.match(regex, self.code)
            if match:
                value = match[0]
                self.code = self.code[len(value):]
                return Token(type=token, value=value)
        raise ValueError(f"No regex matched on code {self.code}")

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def print(self):
        return f"Token of type --{self.type}-- with value --{self.value}"
