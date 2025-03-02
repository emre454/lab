import socket
import json

SERVER_IP = '0.0.0.0'  # Sunucu tüm arayüzlerde dinleyecek
SERVER_PORT = int(input("Sunucu için port numarasını girin: "))  # Kullanıcıdan port numarası al

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP soketi oluşturuyoruz
sock.bind((SERVER_IP, SERVER_PORT))
sock.listen(5)  # Sunucu, aynı anda 5 bağlantıyı dinleyebilir

print("\n🌐 *** TCP Sunucu Başlatıldı *** 🌐")
print(f"Sunucu {SERVER_IP}:{SERVER_PORT} üzerinde sürekli dinlemede...\n")

while True:
    print("\n🎯 === Yeni bağlantı bekleniyor ===")
    
    # Bağlantıyı kabul et
    client_sock, client_addr = sock.accept()
    print(f"✅ Yeni bağlantı alındı: {client_addr}")
    
    try:
        # 1. SYN bekle
        data = client_sock.recv(1024)
        packet = json.loads(data.decode())

        if packet.get("flag") != "SYN":
            print("❌ Hata: İlk paket 'SYN' olmalı! Gelen:", packet.get("flag"))
            client_sock.close()
            continue

        print(f"✅ SYN alındı. Gönderen: {client_addr}")
        
        # 2. SYN-ACK gönder
        response = {
            "flag": "SYN-ACK",
            "seq": 2000,  # Sunucunun başlangıç sıra numarası
            "ack": packet["seq"] + 1
        }
        client_sock.send(json.dumps(response).encode())
        print("📤 SYN-ACK gönderildi:", response)
        
        # 3. ACK bekle
        data = client_sock.recv(1024)
        packet = json.loads(data.decode())

        if packet.get("flag") != "ACK":
            print("❌ Hata: El sıkışma ACK ile tamamlanmalı! Gelen:", packet.get("flag"))
            client_sock.close()
            continue
        
        print("✅ ACK alındı. El sıkışma tamamlandı!")

        # 📦 **Veri iletimi başlıyor**
        complete_message = ""
        print("\n📡 *** Veri iletimi başlatıldı ***")

        while True:
            data = client_sock.recv(1024)
            packet = json.loads(data.decode())

            if packet.get("flag") == "PSH":
                segment = packet.get("data")
                complete_message += segment
                print(f"📥 Segment alındı: {segment}")

                # ACK gönder
                ack_packet = {
                    "flag": "ACK",
                    "seq": packet["seq"] + 1,
                    "ack": packet["seq"] + 1
                }
                client_sock.send(json.dumps(ack_packet).encode())
                print(f"📤 ACK gönderildi: {ack_packet}")

            elif packet.get("flag") == "FIN":
                print("\n📩 *** Veri alımı tamamlandı ***")
                print("📜 **Tam mesaj:**", complete_message)
                break
            else:
                print("❓ Bilinmeyen bayrak:", packet.get("flag"))

        print("\n🔄 Bağlantı sonlandırıldı, yeni bağlantı bekleniyor...\n")
        client_sock.close()  # Bağlantıyı sonlandır
    except Exception as e:
        print("⚠️ Hata:", e)
        client_sock.close()  # Hata durumunda bağlantıyı sonlandır
