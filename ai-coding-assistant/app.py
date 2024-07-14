from flask import Flask, render_template, request
import code_commentor
import code_refactor
import debugger
import documentation_generator
import test_case_generator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/code_commentor', methods=['GET', 'POST'])
def commentor():
    if request.method == 'POST':
        code = request.form['code']
        instructions = request.form['instructions']
        commented_code = code_commentor.generate_commented_code(code, instructions)
        return render_template('code_commentor.html', commented_code=commented_code)
    return render_template('code_commentor.html')

@app.route('/code_refactor', methods=['GET', 'POST'])
def refactor():
    if request.method == 'POST':
        code = request.form['code']
        refactored_code = code_refactor.refactor_code(code)
        return render_template('code_refactor.html', refactored_code=refactored_code)
    return render_template('code_refactor.html')

@app.route('/debugger', methods=['GET', 'POST'])
def debug():
    if request.method == 'POST':
        code = request.form['code']
        syntax_error = debugger.identify_syntax_errors(code)
        if syntax_error:
            error_message = f"Syntax error(s) encountered: {syntax_error}"
            response = debugger.get_openai_fix(error_message, code)
        else:
            runtime_error = debugger.identify_runtime_errors(code)
            if runtime_error:
                error_message = runtime_error
                response = debugger.get_openai_fix(error_message, code)
            else:
                response = "No errors found."
        fixed_code, explanation = debugger.parse_openai_response(response)
        return render_template('debugger.html', fixed_code=fixed_code, explanation=explanation)
    return render_template('debugger.html')

@app.route('/documentation_generator', methods=['GET', 'POST'])
def doc_gen():
    if request.method == 'POST':
        code = request.form['code']
        documentation = documentation_generator.generate_documentation(code)
        return render_template('documentation_generator.html', documentation=documentation)
    return render_template('documentation_generator.html')

@app.route('/test_case_generator', methods=['GET', 'POST'])
def test_gen():
    if request.method == 'POST':
        code = request.form['code']
        generated_test_cases = test_case_generator.openai_generate_test_cases(code)
        return render_template('test_case_generator.html', generated_test_cases=generated_test_cases)
    return render_template('test_case_generator.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)