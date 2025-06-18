import socket
import time
import keyboard
import pythoncom
import hashlib
import hmac
import win32com.client
from datetime import datetime
from threading import Thread

BLOCKED_HOTKEYS = {
    "win+l", "win+r", "ctrl+alt+del", "alt+f4", "win+d", "win+tab",
    "win+e", "win+x", "ctrl+shift+esc",
    
    "win+r cmd enter", "win+r powershell enter", "win+r regedit enter",
    "win+r msconfig enter", "ctrl+`", "ctrl+shift+p",
    
    "ctrl+t", "ctrl+w", "ctrl+shift+n", "alt+d",
    
    "ctrl+a", "ctrl+x", "ctrl+c", "ctrl+v", "del", "shift+del",
    
    "f5", "f11", "alt+enter", "~",
}

SECRET = "Super_Geheimes_Secret"

def generate_token(keys):
    now = datetime.now().strftime("%Y-%m-%d-%H")
    return hmac.new(str.encode(SECRET), f"{now}_{keys}".encode(), hashlib.sha256).hexdigest()

def is_valid_token(client_token, keys):
    return hmac.compare_digest(client_token, generate_token(keys))

def send_hotkey(hotkey_sequence):
    if hotkey_sequence in BLOCKED_HOTKEYS:
        print(f"Blocked dangerous hotkey: {hotkey_sequence}")
        return
    try:
        keyboard.send(hotkey_sequence)
        print(f"Sent hotkey: {hotkey_sequence}")
    except Exception as e:
        print(f"Error sending hotkey: {e}")

def listen_for_commands():
    HOST = '127.0.0.1'  # Lokaler Host
    PORT = 65432        # Port für die Kommunikation

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Hotkey-Service listening on {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            if addr[0] != '127.0.0.1':  # Explizit nur localhost erlauben
                print(f"Blocked non-local connection attempt from {addr[0]}")
                conn.close()
                continue

            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode('utf-8')
                if data:
                    token, keys = data.split(":", 1)
                    if not is_valid_token(token, keys):
                        print(f"Invalid Token: {token}")
                        conn.close()
                        continue
                    print(f"Received command: {data}")
                    send_hotkey(keys.strip().lower())
                conn.sendall(b"ACK")  # Bestätigung senden
                conn.close()

if __name__ == "__main__":
    pythoncom.CoInitialize()
    
    # Starte den Befehl-Listener in einem Thread
    command_thread = Thread(target=listen_for_commands, daemon=True)
    command_thread.start()
    
    try:
        while True:
            time.sleep(100)  # keepalive
    except KeyboardInterrupt:
        print("Service stopped.")
