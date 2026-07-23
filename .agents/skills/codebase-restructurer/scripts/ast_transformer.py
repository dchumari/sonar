import ast
import re
import random

class ASTTransformer(ast.NodeTransformer):
    """
    Python AST Transformer to flatten control flow, rename identifiers, 
    invert loops, mutate conditionals, and sanitize comments.
    """
    def __init__(self, rename_map=None, flatten_all=True):
        super().__init__()
        self.rename_map = rename_map or {}
        self.flatten_all = flatten_all

    def visit_Name(self, node):
        if node.id in self.rename_map:
            node.id = self.rename_map[node.id]
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Rename function name
        if node.name in self.rename_map:
            node.name = self.rename_map[node.name]

        # Handle docstrings and comment/explanation sanitization
        if ast.get_docstring(node):
            if len(node.body) > 0 and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                # Replace with a simplified docstring
                node.body[0].value.value = "Sanitized function behavior explanation."

        # Apply Global Control Flow Flattening to the body
        if self.flatten_all and len(node.body) > 1:
            node.body = self._flatten_control_flow(node.body)

        return self.generic_visit(node)

    def _flatten_control_flow(self, statements):
        """
        Translates a linear list of statements into a switch-like state machine
        executed within a single loop.
        """
        if not statements:
            return statements

        # Filter out docstrings or initial constants
        header = []
        if isinstance(statements[0], ast.Expr) and isinstance(statements[0].value, ast.Constant):
            header.append(statements[0])
            statements = statements[1:]

        if len(statements) <= 1:
            return header + statements

        # Create states
        state_var = f"__state_step"
        states = {i: stmt for i, stmt in enumerate(statements)}
        
        # Build the loop body
        cases = []
        for i, stmt in states.items():
            # Update state variable inside the case block
            next_state = i + 1
            state_update = ast.Assign(
                targets=[ast.Name(id=state_var, ctx=ast.Store())],
                value=ast.Constant(value=next_state)
            )
            
            # Combine the original statement with state transition
            case_body = [stmt, state_update]
            
            # Create if-condition: if __state_step == i
            condition = ast.Compare(
                left=ast.Name(id=state_var, ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=i)]
            )
            cases.append((condition, case_body))

        # Build the nested if-else chain for the state machine
        loop_body = []
        current_if = None
        for cond, body in reversed(cases):
            if current_if is None:
                current_if = ast.If(test=cond, body=body, orelse=[])
            else:
                current_if = ast.If(test=cond, body=body, orelse=[current_if])

        loop_body.append(current_if)

        # Initialize the state variable: __state_step = 0
        init_state = ast.Assign(
            targets=[ast.Name(id=state_var, ctx=ast.Store())],
            value=ast.Constant(value=0)
        )

        # While condition: __state_step < len(statements)
        while_cond = ast.Compare(
            left=ast.Name(id=state_var, ctx=ast.Load()),
            ops=[ast.Lt()],
            comparators=[ast.Constant(value=len(statements))]
        )

        while_loop = ast.While(test=while_cond, body=loop_body, orelse=[])

        return header + [init_state, while_loop]

def sanitize_regex_comments(content):
    """
    Cleans file content comments (removing links, emails, names) while keeping explanations.
    Also handles languages other than Python (JS, Go, C++, etc.).
    """
    # Remove URLs/emails from single-line comments
    content = re.sub(r'(//|#)\s*.*?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+).*', r'\1 Sanitized contact info', content)
    content = re.sub(r'(//|#)\s*.*?(https?://\S+).*', r'\1 Sanitized hyperlink reference', content)
    
    # Remove copyright notices
    content = re.sub(r'(?i)(copyright|©|\(c\)).*', 'Copyright (c) Sanitized Repository Contributors', content)
    return content

def rename_semantic_identifiers(content, language="python"):
    """
    General casing/synonym replacements for identifiers.
    """
    synonyms = {
        "get_user": "retrieve_user_record",
        "fetch_data": "pull_remote_payload",
        "send_response": "dispatch_outgoing_reply",
        "auth_token": "security_credential_key",
        "error_handler": "exception_mitigation_processor",
        "user_id": "client_unique_identifier"
    }
    
    for key, val in synonyms.items():
        # Match word boundaries to prevent substring replacements
        content = re.sub(r'\b' + key + r'\b', val, content)
        
    return content
