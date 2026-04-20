from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


def calculate(num1, operator, num2):
    try:
        a = int(num1)
        b = int(num2)
    except ValueError:
        return 'Error: Invalid integers'

    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b if b != 0 else 'Error: Division by zero'
    elif operator == '%':
        return a % b if b != 0 else 'Error: Division by zero'
    else:
        return 'Error: Invalid operator'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calc', methods=['POST'])
def api_calc():
    data = request.get_json() or request.form
    num1 = data.get('num1')
    operator = data.get('operator')
    num2 = data.get('num2')

    result = calculate(num1, operator, num2)
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
