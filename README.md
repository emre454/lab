# emre454

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

## Kullanım

### MAC Adresi Değiştirme

Programı kullanarak belirli bir ağ arayüzü için MAC adresini değiştirebilirsiniz.

```bash
python3 mac_degisitir.py -i <ag_arayuzu> -m <yeni_mac_adresi>
