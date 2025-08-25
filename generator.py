from parser import BinaryExprNode, FunctionNode, IfNode, PrintNode, LogicalExprNode, AdditiveExprNode, MultiplicativeExprNode, AssignmentExprNode, IntegerNode, StringNode, FuncCallNode, VarDeclNode, FileNode, VarNode, ReturnNode

class Generator():
    def generate(self, node, depth=0):
        indentation = "\t"*depth
        if isinstance(node, FunctionNode):
            name = node.name
            args = ', '.join(node.args)
            res = f"{indentation}def {name} ({args}):\n"
            for statement in node.body:
                statement_string = self.generate(statement, depth=depth+1)
                res+=f"{indentation}{statement_string}"
            res+="\n"
            return res
        elif isinstance(node, PrintNode):
            print_value = self.generate(node.value)
            res = f"{indentation}print({print_value})\n"
            return res
        elif isinstance(node, IfNode):
            condition = self.generate(node.condition)
            res = f"{indentation}if ({condition}):\n"
            for statement in node.ifbody:
                statement_string = self.generate(statement, depth=depth+1)
                res+=f"{statement_string}"
            if node.elsebody:
                res+=f"{indentation}else:\n"
                for statement in node.elsebody:
                    statement_string = self.generate(statement, depth=depth+1)
                    res+=f"{statement_string}"
            return res
        elif isinstance(node, LogicalExprNode):
            if node.op == '&&':
                op = 'and'
            elif node.op == '||':
                op = 'or'
            lhs = self.generate(node.lhs)
            rhs = self.generate(node.rhs)
            res = f"{lhs} {op} {rhs}"
            return res
        elif isinstance(node, BinaryExprNode):
            op = node.op
            if op == '===':
                op = '=='
            elif op == '!==':
                op = '!='
            lhs = node.lhs
            if not isinstance(node.lhs, str):
                lhs = self.generate(node.lhs)
            rhs = self.generate(node.rhs)
            res = f"{lhs} {op} {rhs}"
            return res
        elif isinstance(node, AdditiveExprNode):
            op = node.op
            lhs = self.generate(node.lhs)
            rhs = self.generate(node.rhs)
            res = f"{lhs} {op} {rhs}"
            return res
        elif isinstance(node, MultiplicativeExprNode):
            op = node.op
            lhs = self.generate(node.lhs)
            rhs = self.generate(node.rhs)
            res = f"{lhs} {op} {rhs}"
            return res
        elif isinstance(node, AssignmentExprNode):
            name = node.iden
            expr = self.generate(node.expr)
            res = f"{indentation}{name} = {expr}\n"
            return res
        elif isinstance(node, IntegerNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, FuncCallNode):
            name = node.name.value
            args = ', '.join([self.generate(arg) for arg in node.args])
            res = f"{indentation}{name}({args})"
            return res
        elif isinstance(node, VarDeclNode):
            name = node.name
            expr = self.generate(node.expr)
            res = f"{indentation}{name} = {expr}\n"
            return res
        elif isinstance(node, FileNode):
            res=""
            for statement in node.body:
                statement_string = self.generate(statement)
                res+=f"{statement_string}"
            return res
        elif isinstance(node, VarNode):
            return node.name
        elif isinstance(node, ReturnNode):
            expr = self.generate(node.expr, depth=depth+1)
            res = f"{indentation}return {expr}"
            return res
        else:
            raise RuntimeError(f"Non supported Node {type(node)}")
