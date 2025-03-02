import socket
import json

SERVER_IP = '0.0.0.0'  # Sunucu tüm arayüzlerde dinleyecek
SERVER_PORT = int(input("Sunucu için port numarasını girin: "))  # Kullanıcıdan port numarası al

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("\n🌐 *** TCP Sunucu Başlatıldı *** 🌐")
print(f"Sunucu {SERVER_IP}:{SERVER_PORT} üzerinde sürekli dinlemede...\n")

while True:
    print("\n🎯 === Yeni bağlantı bekleniyor ===")
    
    # 1. SYN bekle
    data, addr = sock.recvfrom(1024)
    try:
        packet = json.loads(data.decode())
    except Exception as e:
        print("⚠️ Veri çözümlenemedi:", e)
        continue

    if packet.get("flag") != "SYN":
        print("❌ Hata: İlk paket 'SYN' olmalı! Gelen:", packet.get("flag"))
        continue

    print(f"✅ SYN alındı. Gönderen: {addr}")
    
    # 2. SYN-ACK gönder
    response = {
        "flag": "SYN-ACK",
        "seq": 2000,  # Sunucunun başlangıç sıra numarası
        "ack": packet["seq"] + 1
    }
    sock.sendto(json.dumps(response).encode(), addr)
    print("📤 SYN-ACK gönderildi:", response)
    
    # 3. ACK bekle
    data, addr = sock.recvfrom(1024)
    try:
        packet = json.loads(data.decode())
    except Exception as e:
        print("⚠️ ACK verisi çözümlenemedi:", e)
        continue

    if packet.get("flag") != "ACK":
        print("❌ Hata: El sıkışma ACK ile tamamlanmalı! Gelen:", packet.get("flag"))
        continue
    print("✅ ACK alındı. El sıkışma tamamlandı!")

    # 📦 **Veri iletimi başlıyor**
    complete_message = ""
    print("\n📡 *** Veri iletimi başlatıldı ***")

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            packet = json.loads(data.decode())
        except Exception as e:
            print("⚠️ Veri çözümlenemedi:", e)
            continue

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
            sock.sendto(json.dumps(ack_packet).encode(), addr)
            print(f"📤 ACK gönderildi: {ack_packet}")

        elif packet.get("flag") == "FIN":
            print("\n📩 *** Veri alımı tamamlandı ***")
            print("📜 **Tam mesaj:**", complete_message)
            break
        else:
            print("❓ Bilinmeyen bayrak:", packet.get("flag"))
    
    print("\n🔄 Bağlantı sonlandırıldı, yeni bağlantı bekleniyor...\n")
