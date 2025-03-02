import socket
import json

# Kullanıcıdan alıcının IP adresini ve portunu al
SERVER_IP = input("Alıcının IP adresini girin: ")
SERVER_PORT = int(input("Bağlanılacak port numarasını girin: "))

# UDP soketi oluştur
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

def udp_handshake():
    print("\n🚀 TCP El Sıkışması Başlatılıyor...")
    
    # 1. SYN gönder
    syn_packet = {"flag": "SYN", "seq": 1000}
    sock.sendto(json.dumps(syn_packet).encode(), (SERVER_IP, SERVER_PORT))
    print("📤 [SYN] Gönderildi ->", syn_packet)
    
    # 2. SYN-ACK bekle
    try:
        data, addr = sock.recvfrom(1024)
        synack_packet = json.loads(data.decode())
        if synack_packet.get("flag") == "SYN-ACK":
            print("📥 [SYN-ACK] Alındı ->", synack_packet)
            
            # 3. ACK gönder
            ack_packet = {"flag": "ACK", "seq": syn_packet["seq"] + 1, "ack": synack_packet["seq"] + 1}
            sock.sendto(json.dumps(ack_packet).encode(), (SERVER_IP, SERVER_PORT))
            print("📤 [ACK] Gönderildi ->", ack_packet)
            print("✅ El sıkışma tamamlandı!\n")
            return True
    except socket.timeout:
        print("⚠️ Zaman aşımı: SYN-ACK alınamadı.\n")
    return False

while True:
    if udp_handshake():
        # Veri iletimi
        message = input("Mesajınızı yazın: ")
        print("\n📡 Veri gönderimine başlıyoruz...")

        for i, segment in enumerate(message):
            packet = {"flag": "PSH", "seq": 2001 + i, "data": segment}
            sock.sendto(json.dumps(packet).encode(), (SERVER_IP, SERVER_PORT))
            print(f"📤 [PSH] Segment gönderildi: {segment}")
            
            # ACK bekle
            try:
                data, addr = sock.recvfrom(1024)
                ack_packet = json.loads(data.decode())
                if ack_packet.get("flag") == "ACK" and ack_packet.get("ack") == packet["seq"] + 1:
                    print(f"✅ [ACK] Segment {segment} için onay alındı.")
                else:
                    print("⚠️ Onay hatası:", ack_packet)
            except socket.timeout:
                print(f"⏳ [TIMEOUT] Segment {segment} için ACK alınamadı!")

        # Veri sonlandırma: FIN bayrağı gönder
        fin_packet = {"flag": "FIN", "seq": 2001 + len(message), "ack": 2001 + len(message)}
        sock.sendto(json.dumps(fin_packet).encode(), (SERVER_IP, SERVER_PORT))
        print("📤 [FIN] Bağlantıyı sonlandırma isteği gönderildi ->", fin_packet)
    else:
        print("⚠️ El sıkışma başarısız oldu, tekrar denemek istiyor musunuz?")
    
    # Tekrar el sıkışma isteği soruluyor
    yeniden = input("🔄 Tekrar el sıkışma isteği gönderilsin mi? (E/H): ")
    if yeniden.lower() != 'e':
        print("👋 Bağlantı sonlandırılıyor...")
        break

print("🏁 Program kapatılıyor...")
sock.close()
