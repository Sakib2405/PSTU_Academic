from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = 'replace-this-with-a-secure-random-key'
app.config['SHUTDOWN_TOKEN'] = 'please-change-this-token'


def calculate(num1, operator, num2):
    """Return (ok: bool, value_or_error).

    ok True -> numeric result (int/float).
    ok False -> error string.
    """
    # Basic presence check
    if num1 is None or num2 is None or operator is None:
        return False, 'Missing input(s)'

    try:
        a = int(num1)
        b = int(num2)
    except (ValueError, TypeError):
        return False, 'Invalid integer input'

    if operator == '+':
        return True, a + b
    elif operator == '-':
        return True, a - b
    elif operator == '*':
        return True, a * b
    elif operator == '/':
        if b == 0:
            return False, 'Division by zero'
        return True, a / b
    elif operator == '%':
        if b == 0:
            return False, 'Division by zero'
        return True, a % b
    else:
        return False, 'Invalid operator'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calc', methods=['POST'])
def api_calc():
    data = request.get_json() or request.form
    num1 = data.get('num1')
    operator = data.get('operator')
    num2 = data.get('num2')

    ok, value = calculate(num1, operator, num2)

    # Save to session history (simple list of strings). Record both successes and failures.
    history = session.get('history', [])
    if ok:
        entry = f"{num1} {operator} {num2} = {value}"
    else:
        entry = f"{num1} {operator} {num2} -> ERROR: {value}"
    history.insert(0, entry)
    session['history'] = history[:20]
    session.modified = True

    if ok:
        return jsonify({'ok': True, 'result': value, 'history': session['history']})
    else:
        return jsonify({'ok': False, 'error': value, 'history': session['history']})


@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify({'history': session.get('history', [])})


@app.route('/api/history/clear', methods=['POST'])
def api_history_clear():
    session['history'] = []
    session.modified = True
    return jsonify({'ok': True, 'history': []})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the Werkzeug development server.

    Call with JSON or form: {"token": "..."} or header `X-SHUTDOWN-TOKEN`.
    This is intended for local use only. Change `SHUTDOWN_TOKEN` before using.
    """
    # check token
    token = None
    if request.is_json:
        token = request.get_json().get('token')
    if not token:
        token = request.form.get('token')
    if not token:
        token = request.headers.get('X-SHUTDOWN-TOKEN')

    if token != app.config.get('SHUTDOWN_TOKEN'):
        return jsonify({'ok': False, 'error': 'Invalid shutdown token'}), 403

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        return jsonify({'ok': False, 'error': 'Not running with the Werkzeug server'}), 500
    func()
    return jsonify({'ok': True, 'message': 'Server shutting down'})
