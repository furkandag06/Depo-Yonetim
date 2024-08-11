import tkinter as tk
from giris_ekrani import GirisEkrani
from depo_yonetim import DepoYonetimProgrami
from dosya_islemleri import KULLANICI_ADI_ADMIN  # KULLANICI_ADI_ADMIN burada tanımlı olmalı

if __name__ == "__main__":
    root = tk.Tk()
    def show_depo_yonetim(kullanici_adi, is_admin):
        # Yeni Tkinter penceresi oluştur
        depo_root = tk.Tk()
        
        # Depo yönetim programını başlat
        DepoYonetimProgrami(depo_root, is_admin, kullanici_adi)
        
        # Ana ekran penceresini kapatmayı engelle
        depo_root.protocol("WM_DELETE_WINDOW", lambda: depo_root.destroy())
        
        # Depo yönetim ekranını göster
        depo_root.mainloop()

    # GirisEkrani oluştur
    app = GirisEkrani(root, on_success=show_depo_yonetim)
    
    # Ana pencereyi göster
    root.mainloop()
