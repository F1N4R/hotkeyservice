import socket
import time
import keyboard
import pythoncom
import win32com.client
from threading import Thread

def send_hotkey(hotkey_sequence):
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
                    print(f"Received command: {data}")
                    send_hotkey(data.strip().lower())
                conn.sendall(b"ACK")  # Bestätigung senden
                conn.close()

if __name__ == "__main__":
    # Stelle sicher, dass COM für win32 funktioniert
    pythoncom.CoInitialize()
    
    # Starte den Befehl-Listener in einem Thread
    command_thread = Thread(target=listen_for_commands, daemon=True)
    command_thread.start()
    
    try:
        while True:
            time.sleep(10)  # Hauptthread am Laufen halten
    except KeyboardInterrupt:
        print("Service stopped.")
