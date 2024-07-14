import openai

openai.api_key = "KEY"

def get_code_input():
    print("Please enter your code (end with a blank line):")
    code_lines = []
    while True:
        line = input()
        if line == "":
            break
        code_lines.append(line)
    code = "\n".join(code_lines)
    return code

def get_comment_instructions():
    instructions = input("Please provide any specific instructions for commenting the code: ")
    return instructions

def generate_commented_code(code, instructions):
    prompt = f"Comment the following code based on these instructions: {instructions}\n\n{code}\n\nCommented code:"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that comments code."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    commented_code = response['choices'][0]['message']['content'].strip()
    return commented_code

def main():
    code = get_code_input()
    instructions = get_comment_instructions()
    commented_code = generate_commented_code(code, instructions)
    
    print("\nCommented Code:\n")
    print(commented_code)

if __name__ == "__main__":
    main()
