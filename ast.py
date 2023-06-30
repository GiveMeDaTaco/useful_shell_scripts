import ast

def extract_columns_from_lambda(fn):
    # Get the lambda function source code
    fn_source = fn.__code__.co_consts[0]
    
    # Parse the source code into an AST
    root = ast.parse(fn_source)
    
    # Define a visitor that extracts string literals from dictionary subscription
    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.columns = []

        def visit_Subscript(self, node):
            if isinstance(node.value, ast.Name) and node.value.id == 'df' and isinstance(node.slice, ast.Str):
                self.columns.append(node.slice.s)

    # Use the visitor to extract columns
    visitor = Visitor()
    visitor.visit(root)
    return visitor.columns
