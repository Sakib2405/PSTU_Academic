# Remote Calculator

## Files:
- `server.py` - Original sockets-based calculator server (TCP)
- `client.py` - Original sockets-based calculator client (TCP)
- `web_server.py` - Flask-based web server + API and UI
- `templates/index.html` - Web UI for the calculator
- `static/main.js` - Frontend JS that calls the API
- `requirements.txt` - Python requirements for the web server

## How to Run (CLI version):

1. Start server: `python server.py`
2. Run client: `python client.py`
3. Enter first number, operator (+, -, *, /, %), second number
4. View result

## How to Run (Web version):

1. Create a virtual environment (recommended) and install dependencies:

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. (Optional but recommended) set secure secrets in your environment:

```pwsh
# Choose strong values instead of the defaults
$env:REMOTE_CALC_SECRET = 'replace-with-a-random-secret'
$env:REMOTE_CALC_SHUTDOWN_TOKEN = 'replace-with-a-secret-token'
```

3. Start the Flask web server:

```pwsh
python web_server.py
```

4. Open a browser and visit `http://127.0.0.1:5000/` to use the web calculator.

## Operations Supported:
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- Modulus (%)

## Features
- CLI socket-based calculator (educational)
- Web UI with animations and dark theme
- Accepts integer and floating-point inputs
- Session-based history stored in signed cookies
- API endpoints: `/api/calc`, `/api/history`, `/api/history/clear`, `/shutdown`

## Notes
- The `/shutdown` endpoint is intended for local development only and is protected by `REMOTE_CALC_SHUTDOWN_TOKEN` when set; disable or remove it in production.
- For production: run behind a WSGI server (Gunicorn/uvicorn), enable HTTPS, and use a server-side session or database for persistent history.
