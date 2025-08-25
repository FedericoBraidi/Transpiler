class Parser():
    def __init__(self, tokens):
        self.tokens = tokens

    def parse_file(self):
        body = self.parse_body()
        return FileNode(body=body)

    def parse_def(self):
        self.consume('function')
        name = self.consume('identifier')
        arg_names = self.parse_args()
        body = self.parse_body()
        a = FunctionNode(name=name.value, args=arg_names, body=body)
        return a

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

    def parse_args_call(self):
        args = []
        self.consume('oparen')
        if not self.peek('cparen'):
            arg = self.parse_expr()
            args.append(arg)
            while self.peek('comma'):
                self.consume('comma')
                arg = self.parse_expr()
                args.append(arg)
        self.consume('cparen')
        return args

    def parse_body(self):
        statements = []
        self.consume('oscope')
        while (not self.peek('cscope')):
            statement = self.parse_statement()
            statements.append(statement)
        self.consume('cscope')
        return statements

    def parse_statement(self):
        if self.peek('function'):
            return self.parse_def()
        elif self.peek('if'):
            return self.parse_if()
        elif self.peek('print'):
            return self.parse_print()
        elif self.peek('var_decl'):
            return self.parse_var_decl()
        elif self.peek('return'):
            return self.parse_return()
        else:
            raise RuntimeError(f"Statement is not among the accepted ones. Next token is {self.tokens[0].print()}")

    def parse_var_decl(self):
        self.consume('var_decl')
        name = self.consume('identifier')
        self.consume('assign')
        expr = self.parse_expr()
        self.consume('semicolon')
        return VarDeclNode(name.value, expr)

    def parse_expr(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.peek('or'):
            op = self.consume('or')
            rhs = self.parse_logical_and()
            node = LogicalExprNode(lhs=node, rhs=rhs, op=op)
        return node

    def parse_logical_and(self):
        node = self.parse_equality_check()
        while self.peek('and'):
            op = self.consume('and')
            rhs = self.parse_equality_check()
            node = LogicalExprNode(lhs=node, rhs=rhs, op=op)
        return node

    def parse_equality_check(self):
        node = self.parse_relation()
        while self.peek(['comparequal', 'comparenotequal']):
            op = self.consume(['comparequal', 'comparenotequal'])
            rhs = self.parse_relation()
            node = BinaryExprNode(lhs=node, rhs=rhs, op=op.value)
        return node

    def parse_relation(self):
        node = self.parse_additive()
        while self.peek(['gt', 'geq', 'lt', 'leq']):
            op = self.consume(['gt', 'geq', 'lt', 'leq'])
            rhs = self.parse_additive()
            node = BinaryExprNode(lhs=node, rhs=rhs, op=op)
        return node

    def parse_additive(self):
        node = self.parse_multiplicative()
        while self.peek(['sum', 'subtract']):
            op = self.consume(['sum', 'subtract'])
            rhs = self.parse_multiplicative()
            node = AdditiveExprNode(lhs=node, rhs=rhs, op=op)
        return node

    def parse_multiplicative(self):
        node = self.parse_primary()
        while self.peek(['times', 'divide']):
            op = self.consume(['times', 'divide'])
            rhs = self.parse_primary()
            node = MultiplicativeExprNode(lhs=node, rhs=rhs, op=op)
        return node

    def parse_primary(self):
        if self.peek('integer'):
            return self.parse_integer()
        elif self.peek('string'):
            return self.parse_string()
        elif self.peek('identifier'):
            ident = self.consume('identifier')
            if self.peek('oparen'):
                return self.parse_func_call(ident)
            elif self.peek('assign'):
                op = self.consume('assign')
                value = self.parse_expr()
                self.consume('semicolon')
                return AssignmentExprNode(ident, op, value)
            else:
                return VarNode(name=ident.value)
        elif self.peek('oparen'):
            self.consume('oparen')
            expr = self.parse_expr()
            self.consume('cparen')
            return expr
        else:
            raise RuntimeError(f"Expression doesn't match supported ones. Next token is {self.tokens[0].print()}")

    def parse_integer(self):
        token = self.consume('integer')
        return IntegerNode(value=token.value)

    def parse_string(self):
        token = self.consume('string')
        return StringNode(value=token.value)

    def parse_func_call(self, iden):
        args = self.parse_args_call()
        return FuncCallNode(name=iden, args=args)

    def parse_return(self):
        self.consume('return')
        expr = self.parse_expr()
        self.consume('semicolon')
        return ReturnNode(expr=expr)

    def parse_if(self):
        self.consume('if')
        self.consume('oparen')
        condition = self.parse_expr()
        self.consume('cparen')
        ifbody = self.parse_body()
        elsebody = None
        if self.peek('else'):
            self.consume('else')
            elsebody = self.parse_body()
        return IfNode(condition=condition, ifbody=ifbody, elsebody=elsebody)

    def parse_print(self):
        self.consume('print')
        self.consume('oparen')
        if self.peek('integer'):
            value = self.parse_integer()
        elif self.peek('string'):
            value = self.parse_string()
        else:
            value = self.parse_expr()
        self.consume('cparen')
        self.consume('semicolon')
        return PrintNode(value)

    def peek(self, expected_token, offset=0):
        if not isinstance(expected_token, list):
            expected_token = [expected_token]
        if self.tokens[offset].type in expected_token:
            return True
        else:
            return False

    def consume(self, expected_token):
        token = self.tokens.pop(0)
        if not isinstance(expected_token, list):
            expected_token = [expected_token]
        if token.type in expected_token:
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

class IfNode():
    def __init__(self, condition, ifbody, elsebody):
        self.condition = condition
        self.ifbody = ifbody
        self.elsebody = elsebody

    def __str__(self):
        return f"A node representing an If statement with:\nCondition:\t{self.condition.__str__()}\nIfBody:\t{self.ifbody.__str__()}\nElseBody:\t{self.elsebody.__str__()}"

class LogicalExprNode():
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def __str__(self):
        return f"A node representing a logical expression with:\nLeft Hand Side:\t{self.lhs.__str__()}\nRight Hand Side:\t{self.rhs.__str__()}\nOperator:\t{self.op}"
class BinaryExprNode():
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def __str__(self):
        return f"A node representing a binary expression with:\nLeft Hand Side:\t{self.lhs.__str__()}\nRight Hand Side:\t{self.rhs.__str__()}\nOperator:\t{self.op}"

class AdditiveExprNode():
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def __str__(self):
        return f"A node representing an additive expression with:\nLeft Hand Side:\t{self.lhs.__str__()}\nRight Hand Side:\t{self.rhs.__str__()}\nOperator:\t{self.op}"

class MultiplicativeExprNode():
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def __str__(self):
        return f"A node representing a multiplicative expression with:\nLeft Hand Side:\t{self.lhs.__str__()}\nRight Hand Side:\t{self.rhs.__str__()}\nOperator:\t{self.op}"

class AssignmentExprNode():
    def __init__(self, iden, op, expr):
        self.iden = iden
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"A node representing an assignment expression with:\nVariable Name:\t{self.iden}\nOperation:{self.op}\nExpression:{self.expr.__str__()}"

class IntegerNode():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"A node representing an integer with:\nValue:{self.value}"

class StringNode():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"A node representing a string with:\nValue:{self.value}"

class FuncCallNode():
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return f"A node representing a function call with:\nName:\t{self.name}\nArgs:\t{self.args}"

class VarDeclNode():
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __str__(self):
        return f"A node representing the declaration of a variable with:\nName:\t{self.name}\nExpression:\t{self.expr.__str__()}"

class FileNode():
    def __init__(self, body):
        self.body = body

    def __str__(self):
        return f"A node representing the whole file whose sub-nodes are:\n{self.body}"

class VarNode():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"A node representing a reference to a variable named {self.name}"

class ReturnNode():
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"A node representing a return statement with:\nReturn Expression:{self.expr}"
