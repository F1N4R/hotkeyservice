import socket, sys, hashlib, hmac
from datetime import datetime

def generate_token(SECRET, keys):
    now = datetime.now().strftime("%Y-%m-%d-%H")
    return hmac.new(str.encode(SECRET), f"{now}_{keys}".encode(), hashlib.sha256).hexdigest()

def send_message(msg:str):
    host = '127.0.0.1'
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(msg.encode('utf-8'))
        r = s.recv(1024).decode()
        if r == "" or None : print('Server: No Response')
        else: print(f'Server: {r}')
    
if __name__ == '__main__':
    for arg in sys.argv:
        if arg.startswith("-"):
            token, keys = arg[1:].split(":", 1)
            hashed_token = generate_token(token, keys)
            try: send_message(f'{hashed_token}:{keys}')
            except: print(f'error: {hashed_token}:{keys}')
