import openai

openai.api_key = "key"

def generate_commented_code(code, instructions, language):
    prompt = f"Comment the following {language} code based on these instructions: {instructions}\n\n{code}\n\nCommented code:"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that comments {language} code."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    commented_code = response['choices'][0]['message']['content'].strip()
    return commented_code
