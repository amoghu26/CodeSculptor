import ast
import traceback
import openai
import re

openai.api_key = "key"

def identify_syntax_errors(code, language):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return e

def identify_runtime_errors(code, language):
    try:
        exec(code)
        return None
    except Exception as e:
        return traceback.format_exc()

def get_openai_fix(error_message, code, language):
    prompt = f"""The following {language} code has an error:
    
Code:
{code}

Error message:
{error_message}

Please provide a corrected version of the code along with an explanation of what was fixed."""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that fixes {language} code."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.5,
    )
    return response['choices'][0]['message']['content'].strip()

def parse_openai_response(response):
    code_pattern = re.compile(r"(```.*?\n)(.*?)(\n```)", re.DOTALL)
    match = code_pattern.search(response)
    if match:
        fixed_code = match.group(2).strip()
        explanation = response.replace(match.group(0), '').strip()
    else:
        fixed_code = response.strip()
        explanation = "The entire response is considered as the fixed code."
    
    return fixed_code, explanation

def main():
    print("Enter your Python code (end with an empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    code = "\n".join(lines)
    
    syntax_error = identify_syntax_errors(code, 'python')  # Default to python for command-line usage
    if syntax_error:
        error_message = f"Syntax error(s) encountered"
        print(error_message)
        print("Fixing syntax error...")
        response = get_openai_fix(error_message, code, 'python')
    else:
        runtime_error = identify_runtime_errors(code, 'python')
        if runtime_error:
            error_message = runtime_error
            print("Runtime error(s) encountered:")
            print(runtime_error)
            print("Fixing runtime error...")
            response = get_openai_fix(error_message, code, 'python')
        else:
            print("No errors found.")
            return
    
    fixed_code, explanation = parse_openai_response(response)
    print("\nFixed code:")
    print(fixed_code)
    print("\nExplanation:")
    print(explanation)

if __name__ == "__main__":
    main()
