# camera_listener.py - Saldirgan bilgisayar 
import socket
import cv2
import pickle
import struct
import time
import select

HOST = '0.0.0.0'
PORT = 4441 

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[INFO] Dinleniyor: {HOST}:{PORT}")
    while True:
        try:
            conn, addr = s.accept()
            print(f"[INFO] Baglanti saglandi: {addr}")
            conn.setblocking(0)
            return conn
        except Exception as e:
            print(f"[HATA] Dinleme hatasi: {e}. 5 saniye sonra yeniden dinleniyor...")
            time.sleep(5)

conn = start_server()
payload_size = struct.calcsize("L")
data_buffer = b""

while True:
    try:
        ready = select.select([conn], [], [], 5)
        if ready[0]:
            packet = conn.recv(4096)
            if not packet:
                raise Exception("Baglanti kesildi!")
            data_buffer += packet
        else:
            raise Exception("Veri alma zaman asimina ugradı!")
        
        while len(data_buffer) >= payload_size:
            packed_size = data_buffer[:payload_size]
            frame_size = struct.unpack("L", packed_size)[0]
            if len(data_buffer) < payload_size + frame_size:
                break
            frame_data = data_buffer[payload_size:payload_size+frame_size]
            data_buffer = data_buffer[payload_size+frame_size:]
            
            frame = pickle.loads(frame_data)
            cv2.imshow("Kamera Goruntusu", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                raise KeyboardInterrupt
    except Exception as e:
        print(f"[HATA] {e}. Baglanti yeniden kuruluyor...")
        conn.close()
        cv2.destroyAllWindows()
        time.sleep(2)
        conn = start_server()
        data_buffer = b""
        continue
    except KeyboardInterrupt:
        print("[INFO] Cikis yapiliyor...")
        break

conn.close()
cv2.destroyAllWindows()
