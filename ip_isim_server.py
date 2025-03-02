import socket
import threading

HOST = "0.0.0.0"  # Tüm ağ arayüzlerini dinle
PORT = 2002  # Sabit port

def handle_client(conn, addr):
    """Bağlanan istemciyi yönetir"""
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break  
            print(f"Yeni kayıt: {data}")
            with open("kayıtlar.txt", "a") as f:
                f.write(data + "\n")

def start_server():
    """Sunucuyu başlatır ve çoklu istemci desteği ekler"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Sunucu {PORT} portunda dinleniyor...")

        while True:
            conn, addr = server.accept()
            print(f"Bağlantı alındı: {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

start_server()
