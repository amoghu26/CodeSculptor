import openai

openai.api_key = "key"

def refactor_code(code, language):
    prompt = f"Refactor the following {language} code to enhance its readability, structure, and efficiency without changing its current functionality:\n\n{code}\n\nRefactored code:"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that refactors {language} code."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    refactored_code = response['choices'][0]['message']['content'].strip()
    explanation_prompt = f"Explain the changes made to the following {language} code:\n\n{code}\n\nRefactored code:\n\n{refactored_code}\n\nExplanation:"
    
    explanation_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that explains {language} code changes."},
            {"role": "user", "content": explanation_prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    explanation = explanation_response['choices'][0]['message']['content'].strip()
    return refactored_code, explanation
