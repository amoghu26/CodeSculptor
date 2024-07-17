import openai
import os

openai.api_key = "key"

def generate_documentation(code, language):
    messages = [
        {"role": "system", "content": f"You are a professional technical writer specializing in {language} documentation."},
        {"role": "user", "content": (
            f"Given the following {language} code, generate comprehensive documentation. "
            "The documentation should include a high-level module overview, detailed function descriptions, "
            "parameters, return values, and any additional notes. Make sure to follow the standard documentation style for {language}.\n\n"
            f"Here is the code:\n\n"
            f"{code}\n\n"
            "Comprehensive Documentation:"
        )}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    documentation = response.choices[0].message['content'].strip()
    return documentation

def main():
    print("Enter the code you want to generate documentation for (end with an empty line):")
    code_lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            code_lines.append(line)
        except KeyboardInterrupt:
            print("\nInput interrupted. Exiting.")
            return
    
    if not code_lines:
        print("No code entered. Exiting.")
        return
    
    code_text = "\n".join(code_lines)
    
    documentation = generate_documentation(code_text, 'python')  # Default to python for command-line usage
    
    print("\nGenerated Documentation:")
    print(documentation)

if __name__ == "__main__":
    main()
