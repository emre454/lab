#!usr/bin/env python
import optparse
import subprocess
import os
import sys
import re

#mac değiştirmek için fonksiyon
def mac_degistir(ag, yeni_mac):
    subprocess.call(["ifconfig", ag ,"down"])
    subprocess.call(["ifconfig", ag ,"hw","ether", yeni_mac])
    subprocess.call(["ifconfig", ag ,"up"])
# Komut satırından giriş almak için fonksiyon
def  girdi():
    parser=optparse.OptionParser()
     # Komut satırından gelen parametreleri almak için bir fonksiyon tanımlıyoruz
    parser.add_option("-i","--interface",dest="ag", help="Ağ kartı arayüzünü belirtin. "
        "Bu seçenek, MAC adresini değiştirmek istediğiniz ağ kartını seçmek içindir. "
        "Ağ kartınızın ismini yazın, örneğin: 'wlo1', 'enp2s0', 'wlan0'. "
        "Ağ kartı adını bilmiyorsanız, terminalde 'ifconfig' veya 'ip a' komutunu kullanarak öğrenebilirsiniz. "
        "Bu seçenek zorunludur ve doğru bir ağ kartı adı girmelisiniz.")
    parser.add_option("-m","--mac",dest="yeni_mac", help="Yeni MAC adresini girin. "
        "MAC adresi, 6 çift hexadecimal sayıdan oluşur ve her çift arasında ':' karakteri bulunur. "
        "Örnek bir MAC adresi: 'b4:85:74:65:78:25'. "
        "Bu adresi değiştirmek için doğru formatta bir MAC adresi yazmalısınız. "
        "MAC adresinizi değiştirmek için ağ kartınızın arayüzünü belirlediğinizden emin olun.")
    (secenekler,girdiler)= parser.parse_args()
    if not secenekler.ag:

        parser.error("(x_x) Ooops, ağ kartı arayüzünü belirtmediniz! Lütfen '-i' veya '--interface' seçeneğiyle ağ kartınızı girin. Yardım için '--help' veya '-h' komutunu kullanabilirsiniz.")
    elif not secenekler.yeni_mac:
        print("(x_x) Ooops! Yeni MAC adresinizi unuttunuz gibi görünüyor! Lütfen '-m' veya '--mac' ile MAC adresinizi belirtin. Yardım için '--help' komutunu kullanmayı unutmayın!")
    return secenekler



# Root yetkileri kontrol eden fonksiyon
def root():

    if os.getuid() != 0:

        print("(｀・ω・´) Lütfen root olarak çalıştırın")
        subprocess.call(["sudo", "python3"] + sys.argv)  
        sys.exit()  
    

# MAC adresini okumak için fonksiyon
def mac_adresoku(ag):
    # ifconfig komutunu kullanarak ağ arayüzü bilgilerini alıyoruz
    ifconfig = subprocess.check_output(["ifconfig", ag]).decode("utf-8")
    # MAC adresini aramak için düzenli ifade (regex) kullanıyoruz
    mac_adress = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w" ,ifconfig)

    if mac_adress:
        # Bulunan MAC adresini döndürüyoruz
        return mac_adress.group(0)


    else:
        
        print("Üzgünüm... Seçtiğiniz ağ adaptöründe MAC adresi bulamadık. (╥﹏╥)")


root()
secenekler = girdi()

eski_mac=mac_adresoku(secenekler.ag)
print(f"Bu ağda kullandığınız {secenekler.ag} arayüzü ile mevcut MAC adresiniz: {eski_mac} (•̀ᴗ•́)و ̑̑")

mac_degistir(secenekler.ag,secenekler.yeni_mac)
eski_mac=mac_adresoku(secenekler.ag)
if eski_mac == secenekler.yeni_mac:
    print(f"(*^▽^*) MAC adresiniz başarıyla değişti. {secenekler.ag} için yeni MAC adresiniz -> {eski_mac}")
else:
    print("(・_・)Yeni MAC adresi okunamadı... Hmm, bu tür küçük sorunlar hiç beklenmezdi, değil mi? (Belki de MAC adresiniz doğru formatta girilmemiştir?)")
