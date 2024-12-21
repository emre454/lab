# MAC Adresi Değiştirme Programı

Bu Python script'i, belirli bir ağ arayüzü için MAC adresini değiştirmek ve mevcut MAC adresini okumak amacıyla kullanılabilir. Aynı zamanda, script'in yönetici (root) yetkileriyle çalışmasını sağlayan bir fonksiyon da içerir.

## Özellikler

- Belirtilen ağ arayüzü için MAC adresini değiştirme
- Belirtilen ağ arayüzü için mevcut MAC adresini okuma
- Root yetkisi kontrolü ve gerektiğinde root olarak çalıştırma
- Komut satırından çalıştırılabilir ve kullanıcı dostu seçenekler

## Gereksinimler

- Python 3
- `ifconfig` komutunun sistemde yüklü olması (Linux işletim sistemlerinde genellikle varsayılan olarak bulunur)
- `sudo` erişimi (root yetkileri için)


# Mac_Degistirici - Kurulum Rehberi


## Kurulum Adımları

### 1. Kaynağı İndirin
Git kullanarak projeyi bilgisayarınıza klonlayın:
```git clone https://github.com/emre454/Mac_Degistirici.git```

2. Proje Klasörüne Geçin

Projeyi indirdikten sonra, proje klasörüne geçin:

```cd Mac_Degistirici```

3. Gereksinimleri Yükleyin

Projede kullanılan tüm Python kütüphanelerini yüklemek için requirements.txt dosyasını kullanın. Bunun için terminale şu komutu yazın:

```pip install -r requirements.txt```

4. Yardım

Eğer kullanım hakkında yardıma ihtiyaç duyarsanız, şu komutla yardım alabilirsiniz:

```python mac_degistir.py -h```
Yardım komutuyla betiğin tüm seçenekleri ve kullanımı hakkında daha fazla bilgi edinebilirsiniz.


## Kullanım

### MAC Adresi Değiştirme

Programı kullanarak belirli bir ağ arayüzü için MAC adresini değiştirebilirsiniz.

```bash
python3 mac_degisitir.py -i <ag_arayuzu> -m <yeni_mac_adresi>
