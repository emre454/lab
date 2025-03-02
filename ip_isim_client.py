import socket

server_ip = input("Sunucu IP adresini girin: ")  # Kullanıcıdan al
server_port = 2002  # Sabit port

isim = input("İsminizi girin: ")
ip_adresi = input("IP adresinizi girin: ")

mesaj = f"{isim} - {ip_adresi}:6565"  # IP'ye :6565 ekleniyor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((server_ip, server_port))
    client.sendall(mesaj.encode())

print("Bilgiler sunucuya gönderildi!")
