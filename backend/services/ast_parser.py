import ast

class DepthVisitor(ast.NodeVisitor):
    def __init__(self):
        self.current_depth = 0
        self.max_depth = 0

    def visit_For(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        
        # Traverse children (the body of the loop)
        self.generic_visit(node)
        
        # Backtrack as we exit the loop
        self.current_depth -= 1
        
    def visit_While(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        
        self.generic_visit(node)
        self.current_depth -= 1

def count_max_loop_depth(code_string: str) -> int:
    """
    Parses Python code and uses DFS to find the maximum depth of nested loops.
    Returns 0 if no loops, 1 for single loop, 2 for nested loops, etc.
    """
    tree = ast.parse(code_string)
    visitor = DepthVisitor()
    visitor.visit(tree)
    return visitor.max_depth