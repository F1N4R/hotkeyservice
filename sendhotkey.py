import socket, sys

def send_message(msg:str):
    host = '127.0.0.1'
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(msg.encode('utf-8'))
        r = s.recv(1024).decode()
        print('Server: ' + r)
    
if __name__ == '__main__':
    for arg in sys.argv:
        if arg.startswith("-"):
            send_message(arg[1:])
