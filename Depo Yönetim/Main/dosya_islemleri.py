import json

KULLANICI_ADI_ADMIN = 'admin'
SIFRE_ADMIN = '1234'
KULLANICI_BILGILERI_DOSYASI = "kullanicilar.json"
URUNLER_DOSYASI = "urunler.json"

def kullanicilari_yukle(dosya_adi):
    try:
        with open(dosya_adi, 'r') as dosya:
            veriler = json.load(dosya)
            if not isinstance(veriler, dict):
                raise ValueError("JSON verisi bir sözlük olmalıdır.")
            return veriler
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {dosya_adi}")
        return {}
    except json.JSONDecodeError:
        print(f"JSON decode hatası: {dosya_adi}")
        return {}
    except ValueError as e:
        print(f"Değer hatası: {e}")
        return {}

def kullanicilari_kaydet(dosya_adi, kullanicilar):
    try:
        with open(dosya_adi, 'w') as dosya:
            json.dump(kullanicilar, dosya, indent=4)
    except IOError as e:
        print(f"Dosya yazma hatası: {e}")

def urunleri_yukle(dosya_adi):
    try:
        with open(dosya_adi, 'r') as dosya:
            veriler = json.load(dosya)
            if not isinstance(veriler, dict):
                raise ValueError("JSON verisi bir sözlük olmalıdır.")
            return veriler
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {dosya_adi}")
        return {}
    except json.JSONDecodeError:
        print(f"JSON decode hatası: {dosya_adi}")
        return {}
    except ValueError as e:
        print(f"Değer hatası: {e}")
        return {}

def urunleri_kaydet(dosya_adi, urunler):
    try:
        with open(dosya_adi, 'w') as dosya:
            json.dump(urunler, dosya, indent=4)
    except IOError as e:
        print(f"Dosya yazma hatası: {e}")
