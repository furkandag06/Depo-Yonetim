import tkinter as tk
from tkinter import messagebox
from depo_yonetim import DepoYonetimProgrami
from dosya_islemleri import kullanicilari_yukle, KULLANICI_BILGILERI_DOSYASI, KULLANICI_ADI_ADMIN, SIFRE_ADMIN

class GirisEkrani:
    def __init__(self, root, on_success=None):
        self.root = root
        self.on_success = on_success
        self.root.title("Giriş Ekranı")
        self.root.geometry("350x220")
        
        # Hoş geldiniz mesajı
        tk.Label(root, text="Depo Yönetim Sistemine Hoşgeldiniz", font=("Arial", 14)).pack(pady=10)

        tk.Label(root, text="Kullanıcı Adı").pack(pady=5)
        self.entry_kullanici_adi = tk.Entry(root)
        self.entry_kullanici_adi.pack(pady=5)

        tk.Label(root, text="Şifre").pack(pady=5)
        self.entry_sifre = tk.Entry(root, show="*")
        self.entry_sifre.pack(pady=5)

        tk.Button(root, text="Giriş Yap", command=self.giris_yap).pack(pady=10)

    def giris_yap(self):
        kullanici_adi = self.entry_kullanici_adi.get()
        sifre = self.entry_sifre.get()
        kullanicilar = kullanicilari_yukle(KULLANICI_BILGILERI_DOSYASI)

        if kullanici_adi == KULLANICI_ADI_ADMIN and sifre == SIFRE_ADMIN:
            messagebox.showinfo("Başarı", "Admin olarak giriş başarılı!")
            self.root.destroy()  # Giriş başarılıysa giriş ekranını kapat
            if self.on_success:
                self.on_success(kullanici_adi, True)  # Callback fonksiyonunu çağır ve admin olarak işaretle
            return

        for kullanici in kullanicilar.values():
            if kullanici["ad"] == kullanici_adi and kullanici["sifre"] == sifre:
                is_admin = kullanici.get("rol") == "admin"
                if is_admin:
                    messagebox.showinfo("Başarı", "Admin olarak giriş başarılı!")
                else:
                    messagebox.showinfo("Başarı", "Kullanıcı olarak giriş başarılı!")
                
                self.root.destroy()  # Giriş başarılıysa giriş ekranını kapat
                if self.on_success:
                    self.on_success(kullanici_adi, is_admin)  # Callback fonksiyonunu çağır ve rolü ilet
                return
        
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")
