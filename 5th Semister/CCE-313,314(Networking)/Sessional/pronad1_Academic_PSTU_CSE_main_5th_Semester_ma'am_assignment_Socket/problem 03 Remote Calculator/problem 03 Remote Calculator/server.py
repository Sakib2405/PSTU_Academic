import socket

HOST = '127.0.0.1'
PORT = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Calculator Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    
    data = conn.recv(1024).decode()
    num1, operator, num2 = data.split()
    try:
        a = float(num1)
        b = float(num2)
    except ValueError:
        result = 'Error: Invalid numeric input'
        conn.send(str(result).encode())
        conn.close()
        continue

    if operator == '+':
        res = a + b
    elif operator == '-':
        res = a - b
    elif operator == '*':
        res = a * b
    elif operator == '/':
        res = a / b if b != 0 else 'Error: Division by zero'
    elif operator == '%':
        res = a % b if b != 0 else 'Error: Division by zero'
    else:
        res = 'Error: Invalid operator'

    # present integer results without decimal point when applicable
    if isinstance(res, float) and res.is_integer():
        result = int(res)
    else:
        result = res

    conn.send(str(result).encode())
    print(f"Calculated: {a} {operator} {b} = {result}")
    conn.close()
