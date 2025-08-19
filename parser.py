class Parser():
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        tree = self.parse_def()
        return tree

    def parse_def(self):
        self.consume('function')
        name = self.consume('identifier')
        arg_names = self.parse_args()
        body = self.parse_expr()
        return FunctionNode(name=name.value, args=arg_names, body=body)

    def parse_args(self):
        args = []
        self.consume('oparen')
        if self.peek('identifier'):
            arg = self.consume('identifier')
            args.append(arg.value)
            while self.peek('comma'):
                self.consume('comma')
                arg = self.consume('identifier')
                args.append(arg.value)
        self.consume('cparen')
        return args

    def parse_expr(self):
        self.consume('oscope')
        print_node = self.parse_print()
        self.consume('cscope')
        return print_node

    def parse_print(self):
        self.consume('print')
        self.consume('oparen')
        value = self.consume('integer')
        self.consume('cparen')
        self.consume('semicolon')
        return PrintNode(value.value)

    def peek(self, expected_token, offset=0):
        if self.tokens[offset].type == expected_token:
            return True
        else:
            return False

    def consume(self, expected_token):
        token = self.tokens.pop(0)
        if token.type == expected_token:
            return token
        else:
            raise RuntimeError(f"Expected token of type {expected_token} but got {token.type}.")

class FunctionNode():
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return f"A node representing a function with:\nName:\t{self.name}\nArgs:\t{self.args}\nBody:\t{self.body.__str__()}"

class PrintNode():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Print Node with print value {self.value}"
