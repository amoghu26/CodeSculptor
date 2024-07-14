import openai
import os

openai.api_key = "KEY"

def refactor_code(code):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that refactors code to improve its structure and readability without changing its functionality."
            },
            {
                "role": "user",
                "content": f"Refactor the following code to improve its structure and readability without changing its functionality:\n\n{code}"
            }
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    refactored_code = response['choices'][0]['message']['content'].strip()
    return refactored_code

def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def write_code_to_file(file_path, code):
    with open(file_path, 'w') as file:
        file.write(code)

def main():
    print("Enter the code you want to refactor (end with an empty line):")
    code_lines = []
    while True:
        line = input()
        if line == "":
            break
        code_lines.append(line)
    
    code_text = "\n".join(code_lines)
    
    refactored_code = refactor_code(code_text)
    
    print("\nOriginal Code:")
    print(code_text)
    print("\nRefactored Code:")
    print(refactored_code)

if __name__ == "__main__":
    main()
