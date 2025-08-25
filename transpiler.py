import os

from generator import Generator
from parser import Parser
from tokenizer import Tokenizer

# Read the original code
with open("to_be_translated.js", "r") as f:
    content = f.read()
print(content)

# Tokenize the program
tokenizer = Tokenizer(content)
token_list = tokenizer.tokenize()
for token in token_list:
    print(token.print())

# Build the AST (parsing the tokens)
parser = Parser(token_list)
tree = parser.parse()

# Build Python code from the AST
generator = Generator()
code = generator.generate(tree)
print(code)
print("------------------------------")

# Write the code to a file
path = "translated_code.py"
os.remove(path)
with open(path, "w") as file:
    file.write(code)
