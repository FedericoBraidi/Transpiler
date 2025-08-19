from parser import FunctionNode, PrintNode

class Generator():
    def generate(self, node):
        if isinstance(node, FunctionNode):
            name = node.name
            args = ', '.join(node.args)
            body = self.generate(node.body)
            res = f"def {name} ({args}):\n\t{body}"
            return res
        elif isinstance(node, PrintNode):
            res = f"print({node.value})"
            return res
        else:
            return
