import ast
import openai

openai.api_key = "key"

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node)
        self.generic_visit(node)

def analyze_code(code):
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.functions

def generate_edge_cases(params):
    edge_cases = []
    for param in params:
        edge_cases.append({param.arg: [None, "", 0, -1, 1, 10**6]})
    return edge_cases

def generate_test_cases(functions):
    test_cases = {}
    for func in functions:
        params = func.args.args
        edge_cases = generate_edge_cases(params)
        test_cases[func.name] = edge_cases
    return test_cases

def openai_generate_test_cases(code, language):
    prompt = (
        f"Analyze the following {language} code and generate test cases that fully test the limits of the program:\n\n"
        f"{code}\n\n"
        "Identify edge cases and generate relevant test cases."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a highly skilled assistant that helps with generating test cases for {language} code."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message['content'].strip()

if __name__ == "__main__":
    print("Please enter the code to analyze (end with a blank line):")
    code_lines = []
    while True:
        line = input()
        if line == "":
            break
        code_lines.append(line)
    code = "\n".join(code_lines)

    functions = analyze_code(code)
    test_cases = generate_test_cases(functions)

    for func, cases in test_cases.items():
        print(f"Function: {func}")
        for case in cases:
            print(f"  Test Case: {case}")

    generated_test_cases = openai_generate_test_cases(code, 'python')  # Default to python for command-line usage
    print("\nGenerated Test Cases:")
    print(generated_test_cases)
