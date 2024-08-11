import tkinter as tk
from tkinter import ttk, messagebox
import json

# Fonksiyonlar
def urunleri_yukle(dosya_adi):
    """Ürünleri JSON dosyasından yükler."""
    try:
        with open(dosya_adi, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def urunleri_kaydet(dosya_adi, urunler):
    """Ürünleri JSON dosyasına kaydeder."""
    with open(dosya_adi, 'w') as f:
        json.dump(urunler, f, indent=4)

def kullanicilari_yukle(dosya_adi):
    """Kullanıcıları JSON dosyasından yükler."""
    try:
        with open(dosya_adi, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def kullanicilari_kaydet(dosya_adi, kullanicilar):
    """Kullanıcıları JSON dosyasına kaydeder."""
    with open(dosya_adi, 'w') as f:
        json.dump(kullanicilar, f, indent=4)

class DepoYonetimProgrami:
    def __init__(self, root, admin, aktif_kullanici):
        self.root = root
        self.admin = admin
        self.aktif_kullanici = aktif_kullanici
        self.root.title("Depo Yönetim Programı")
        self.root.geometry("800x620")
        self.urun_dosya_adi = "urunler.json"
        self.kullanici_dosya_adi = "kullanicilar.json"

        # Ürünleri yükleme
        self.urunler = urunleri_yukle(self.urun_dosya_adi)

        # Kullanıcıları yükleme
        self.kullanicilar = kullanicilari_yukle(self.kullanici_dosya_adi)

        # Ürün listesi göstergesi
        self.label_urunler = tk.Label(root, text="Depodaki Ürünler", font=("Arial", 12, "bold"))
        self.label_urunler.pack(pady=10)

        self.tree_urunler = ttk.Treeview(root, columns=("Ürün ID", "Ürün Adı", "Miktar", "Fiyat", "Açıklama", "Ekleyen", "Düzenle"), show="headings")
        self.setup_treeview_columns()
        self.tree_urunler.pack()

        self.guncelle_urun_listesi()
        self.tree_urunler.bind("<Double-1>", self.on_double_click)

        if self.admin:
            self.setup_admin_controls()

        # Yeni ürün ekleme
        self.frame_yeni_urun = self.create_frame(root, "Yeni Ürün Ekle")
        self.setup_yeni_urun_widgets()

        # Ürün silme
        self.button_urun_sil = tk.Button(root, text="Sil", command=self.urun_sil)
        self.button_urun_sil.pack(pady=5)

    def setup_treeview_columns(self):
        """Treeview için sütun başlıklarını ayarlar."""
        self.tree_urunler.heading("Ürün ID", text="Ürün ID")
        self.tree_urunler.heading("Ürün Adı", text="Ürün Adı")
        self.tree_urunler.heading("Miktar", text="Miktar")
        self.tree_urunler.heading("Fiyat", text="Fiyat")
        self.tree_urunler.heading("Açıklama", text="Açıklama")
        self.tree_urunler.heading("Ekleyen", text="Ekleyen")
        self.tree_urunler.heading("Düzenle", text="Düzenle")
        self.tree_urunler.column("Düzenle", width=80, anchor='center')

    def setup_admin_controls(self):
        """Admin kullanıcıları için kontrol butonlarını oluşturur."""
        self.frame_kullanici_islemleri = tk.Frame(self.root)
        self.frame_kullanici_islemleri.pack(pady=10, fill=tk.X)

        self.button_kullanici_ekle = tk.Button(self.frame_kullanici_islemleri, text="Kullanıcı Ekle", command=self.kullanici_ekle_ekrani)
        self.button_kullanici_ekle.pack(side=tk.LEFT, padx=5)

        self.button_kullanici_listesi = tk.Button(self.frame_kullanici_islemleri, text="Kullanıcı Listesi", command=self.kullanici_listesi_ekrani)
        self.button_kullanici_listesi.pack(side=tk.LEFT, padx=5)

    def create_frame(self, parent, label_text):
        """Yeni bir frame oluşturur ve başlık ekler."""
        frame = tk.Frame(parent)
        frame.pack(pady=10, fill=tk.X)
        tk.Label(frame, text=label_text, font=("Arial", 10, "bold")).pack(pady=5)
        return frame

    def setup_yeni_urun_widgets(self):
        """Yeni ürün ekleme için widget'ları oluşturur."""
        self.entry_urun_adi = self.create_entry(self.frame_yeni_urun, "Ürün Adı")
        self.entry_urun_miktari = self.create_entry(self.frame_yeni_urun, "Miktar")
        self.entry_urun_fiyati = self.create_entry(self.frame_yeni_urun, "Fiyat")
        self.entry_urun_aciklama = self.create_entry(self.frame_yeni_urun, "Açıklama")

        self.button_yeni_urun_ekle = tk.Button(self.frame_yeni_urun, text="Ürün Ekle", command=self.urun_ekle)
        self.button_yeni_urun_ekle.pack(pady=10)

    def create_entry(self, parent, placeholder):
        """Yeni bir Entry widget'ı oluşturur ve varsayılan değer ekler."""
        entry = tk.Entry(parent)
        entry.pack(pady=5)
        entry.insert(0, placeholder)
        return entry

    def guncelle_urun_listesi(self):
        """Ürünleri Treeview widget'ında günceller."""
        self.tree_urunler.delete(*self.tree_urunler.get_children())
        for urun_id, urun_bilgisi in self.urunler.items():
            self.tree_urunler.insert("", "end", values=(urun_id, urun_bilgisi["urun_adi"], urun_bilgisi["miktar"], urun_bilgisi["fiyat"], urun_bilgisi["aciklama"], urun_bilgisi["ekleyen"], "Düzenle"))

    def urun_ekle(self):
        """Yeni ürün ekler."""
        urun_adi = self.entry_urun_adi.get()
        miktar = self.entry_urun_miktari.get()
        fiyat = self.entry_urun_fiyati.get()
        aciklama = self.entry_urun_aciklama.get()

        if self.urunler:
            urun_ids = [int(key) for key in self.urunler.keys()]
            urun_id = max(urun_ids) + 1
        else:
            urun_id = 1

        if urun_adi and miktar.isdigit() and fiyat and aciklama:
            miktar = int(miktar)
            self.urunler[str(urun_id)] = {
                "urun_adi": urun_adi,
                "miktar": miktar,
                "fiyat": fiyat,
                "aciklama": aciklama,
                "ekleyen": self.aktif_kullanici
            }
            urunleri_kaydet(self.urun_dosya_adi, self.urunler)
            self.guncelle_urun_listesi()
            self.clear_entries()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurduğunuzdan emin olun.")

    def clear_entries(self):
        """Tüm giriş alanlarını temizler."""
        self.entry_urun_adi.delete(0, tk.END)
        self.entry_urun_miktari.delete(0, tk.END)
        self.entry_urun_fiyati.delete(0, tk.END)
        self.entry_urun_aciklama.delete(0, tk.END)

    def on_double_click(self, event):
        """Treeview'da çift tıklama olayını işler."""
        item = self.tree_urunler.selection()[0]
        urun_id = self.tree_urunler.item(item, "values")[0]
    
        if urun_id in self.urunler:
            urun = self.urunler[urun_id]
            urun_detay = (
                f"ID: {urun_id}\n"
                f"Ürün Adı: {urun.get('urun_adi', 'Bilinmiyor')}\n"
                f"Miktar: {urun.get('miktar', 'Bilinmiyor')}\n"
                f"Fiyat: {urun.get('fiyat', 'Bilinmiyor')}\n"
                f"Açıklama: {urun.get('aciklama', 'Bilinmiyor')}\n"
                f"Ekleyen: {urun.get('ekleyen', 'Bilinmiyor')}"
            )
        if messagebox.askyesno("Düzenleme", f"Ürün bilgileri:\n{urun_detay}\n\nBu ürünü düzenlemek istiyor musunuz?"):
            self.duzenleme_ekrani(urun_id)
        else:
            messagebox.showerror("Hata", "Seçilen ürün bulunamadı.")

    def duzenleme_ekrani(self, urun_id):
        """Ürün düzenleme ekranını oluşturur."""
        urun_bilgisi = self.urunler.get(urun_id, {})
        
        ekrana = tk.Toplevel(self.root)
        ekrana.title(f"Ürün Düzenleme: {urun_id}")

        tk.Label(ekrana, text="Ürün Adı").pack(pady=5)
        entry_urun_adi = tk.Entry(ekrana)
        entry_urun_adi.insert(0, urun_bilgisi.get("urun_adi", ""))
        entry_urun_adi.pack(pady=5)

        tk.Label(ekrana, text="Miktar").pack(pady=5)
        entry_miktar = tk.Entry(ekrana)
        entry_miktar.insert(0, urun_bilgisi.get("miktar", ""))
        entry_miktar.pack(pady=5)

        tk.Label(ekrana, text="Fiyat").pack(pady=5)
        entry_fiyat = tk.Entry(ekrana)
        entry_fiyat.insert(0, urun_bilgisi.get("fiyat", ""))
        entry_fiyat.pack(pady=5)

        tk.Label(ekrana, text="Açıklama").pack(pady=5)
        entry_aciklama = tk.Entry(ekrana)
        entry_aciklama.insert(0, urun_bilgisi.get("aciklama", ""))
        entry_aciklama.pack(pady=5)

        button_guncelle = tk.Button(ekrana, text="Güncelle", command=lambda: self.urun_guncelle(urun_id, entry_urun_adi.get(), entry_miktar.get(), entry_fiyat.get(), entry_aciklama.get(), ekrana))
        button_guncelle.pack(pady=10)

    def urun_guncelle(self, urun_id, urun_adi, miktar, fiyat, aciklama, ekrana):
        """Ürün bilgilerini günceller."""
        if urun_adi and miktar.isdigit() and fiyat and aciklama:
            miktar = int(miktar)
            self.urunler[urun_id] = {
                "urun_adi": urun_adi,
                "miktar": miktar,
                "fiyat": fiyat,
                "aciklama": aciklama,
                "ekleyen": self.aktif_kullanici
            }
            urunleri_kaydet(self.urun_dosya_adi, self.urunler)
            ekrana.destroy()
            self.guncelle_urun_listesi()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurduğunuzdan emin olun.")

    def urun_sil(self):
        """Seçili ürünü siler."""
        selected_item = self.tree_urunler.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen silmek için bir ürün seçin.")
            return
        
        urun_id = self.tree_urunler.item(selected_item[0], "values")[0]
        if urun_id in self.urunler:
            urun = self.urunler[urun_id]
            urun_detay = (
                f"ID: {urun_id}\n"
                f"Ürün Adı: {urun.get('urun_adi', 'Bilinmiyor')}\n"
                f"Miktar: {urun.get('miktar', 'Bilinmiyor')}\n"
                f"Fiyat: {urun.get('fiyat', 'Bilinmiyor')}\n"
                f"Açıklama: {urun.get('aciklama', 'Bilinmiyor')}\n"
                f"Ekleyen: {urun.get('ekleyen', 'Bilinmiyor')}"
            )
            if messagebox.askyesno("Silme Onayı", f"Ürün bilgileri:\n{urun_detay}\n\nBu ürünü silmek istiyor musunuz?"):
                del self.urunler[urun_id]
                urunleri_kaydet(self.urun_dosya_adi, self.urunler)
                self.guncelle_urun_listesi()
        else:
            messagebox.showerror("Hata", "Seçilen ürün bulunamadı.")

    def kullanici_ekle_ekrani(self):
        """Yeni kullanıcı ekleme ekranını oluşturur."""
        ekrana = tk.Toplevel(self.root)
        ekrana.title("Kullanıcı Ekle")

        tk.Label(ekrana, text="Ad").pack(pady=5)
        entry_ad = tk.Entry(ekrana)
        entry_ad.pack(pady=5)

        tk.Label(ekrana, text="E-posta").pack(pady=5)
        entry_email = tk.Entry(ekrana)
        entry_email.pack(pady=5)

        tk.Label(ekrana, text="Şifre").pack(pady=5)
        entry_sifre = tk.Entry(ekrana, show="*")
        entry_sifre.pack(pady=5)

        tk.Label(ekrana, text="Telefon").pack(pady=5)
        entry_telefon = tk.Entry(ekrana)
        entry_telefon.pack(pady=5)

        tk.Label(ekrana, text="Adres").pack(pady=5)
        entry_adres = tk.Entry(ekrana)
        entry_adres.pack(pady=5)

        tk.Label(ekrana, text="Rol").pack(pady=5)
        roles = ["admin", "user"]
        role_var = tk.StringVar(value=roles[1])
        role_menu = tk.OptionMenu(ekrana, role_var, *roles)
        role_menu.pack(pady=5)

        button_ekle = tk.Button(ekrana, text="Ekle", command=lambda: self.kullanici_ekle(entry_ad.get(), entry_email.get(), entry_sifre.get(), entry_telefon.get(), entry_adres.get(), role_var.get(), ekrana))
        button_ekle.pack(pady=10)

    def kullanici_ekle(self, ad, email, sifre, telefon, adres, rol, ekrana):
        """Yeni kullanıcı ekler."""
        if ad and email and sifre and telefon and adres and rol:
            kullanici_id = len(self.kullanicilar) + 1
            self.kullanicilar[str(kullanici_id)] = {
                "ad": ad,
                "email": email,
                "sifre": sifre,
                "telefon": telefon,
                "adres": adres,
                "rol": rol
            }
            kullanicilari_kaydet(self.kullanici_dosya_adi, self.kullanicilar)
            ekrana.destroy()
            self.kullanici_listesi_ekrani()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurduğunuzdan emin olun.")

    def kullanici_listesi_ekrani(self):
        """Kullanıcı listesi ekranını oluşturur."""
        ekrana = tk.Toplevel(self.root)
        ekrana.title("Kullanıcı Listesi")

        columns = ['Kullanıcı ID', 'Ad', 'E-posta', 'Telefon', 'Adres', 'Rol', 'Düzenle']
        tree = ttk.Treeview(ekrana, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for kullanici_id, kullanici_bilgisi in self.kullanicilar.items():
            tree.insert("", "end", values=(kullanici_id, kullanici_bilgisi["ad"], kullanici_bilgisi["email"], kullanici_bilgisi["telefon"], kullanici_bilgisi["adres"], kullanici_bilgisi["rol"], "Düzenle"))

        tree.pack(fill=tk.BOTH, expand=True)
        tree.bind("<Double-1>", self.kullanici_duzenle)

    def kullanici_duzenle(self, event):
        """Kullanıcı düzenleme ekranını açar."""
        item = event.widget.selection()[0]
        kullanici_id = event.widget.item(item, "values")[0]
        self.kullanici_guncelle_ekrani(kullanici_id)

    def kullanici_guncelle_ekrani(self, kullanici_id):
        """Kullanıcı güncelleme ekranını oluşturur."""
        kullanici_bilgisi = self.kullanicilar.get(kullanici_id, {})

        ekrana = tk.Toplevel(self.root)
        ekrana.title(f"Kullanıcı Düzenleme: {kullanici_id}")

        tk.Label(ekrana, text="Ad").pack(pady=5)
        entry_ad = tk.Entry(ekrana)
        entry_ad.insert(0, kullanici_bilgisi.get("ad", ""))
        entry_ad.pack(pady=5)

        tk.Label(ekrana, text="E-posta").pack(pady=5)
        entry_email = tk.Entry(ekrana)
        entry_email.insert(0, kullanici_bilgisi.get("email", ""))
        entry_email.pack(pady=5)

        tk.Label(ekrana, text="Şifre").pack(pady=5)
        entry_sifre = tk.Entry(ekrana, show="*")
        entry_sifre.insert(0, kullanici_bilgisi.get("sifre", ""))
        entry_sifre.pack(pady=5)

        tk.Label(ekrana, text="Telefon").pack(pady=5)
        entry_telefon = tk.Entry(ekrana)
        entry_telefon.insert(0, kullanici_bilgisi.get("telefon", ""))
        entry_telefon.pack(pady=5)

        tk.Label(ekrana, text="Adres").pack(pady=5)
        entry_adres = tk.Entry(ekrana)
        entry_adres.insert(0, kullanici_bilgisi.get("adres", ""))
        entry_adres.pack(pady=5)

        tk.Label(ekrana, text="Rol").pack(pady=5)
        roles = ["admin", "user"]
        role_var = tk.StringVar(value=kullanici_bilgisi.get("rol", roles[1]))
        role_menu = tk.OptionMenu(ekrana, role_var, *roles)
        role_menu.pack(pady=5)

        button_guncelle = tk.Button(ekrana, text="Güncelle", command=lambda: self.kullanici_guncelle(kullanici_id, entry_ad.get(), entry_email.get(), entry_sifre.get(), entry_telefon.get(), entry_adres.get(), role_var.get(), ekrana))
        button_guncelle.pack(pady=10)

    def kullanici_guncelle(self, kullanici_id, ad, email, sifre, telefon, adres, rol, ekrana):
        """Kullanıcı bilgilerini günceller."""
        if ad and email and sifre and telefon and adres and rol:
            self.kullanicilar[kullanici_id] = {
                "ad": ad,
                "email": email,
                "sifre": sifre,
                "telefon": telefon,
                "adres": adres,
                "rol": rol
            }
            kullanicilari_kaydet(self.kullanici_dosya_adi, self.kullanicilar)
            ekrana.destroy()
            self.kullanici_listesi_ekrani()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurduğunuzdan emin olun.")
    def kullanici_listesi_ekrani(self):
        """Kullanıcı listesi ekranını oluşturur."""
        ekrana = tk.Toplevel(self.root)
        ekrana.title("Kullanıcı Listesi")

        columns = ['Kullanıcı ID', 'Ad', 'E-posta', 'Telefon', 'Adres', 'Rol', 'Düzenle', 'Sil']
        tree = ttk.Treeview(ekrana, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for kullanici_id, kullanici_bilgisi in self.kullanicilar.items():
            tree.insert("", "end", values=(kullanici_id, kullanici_bilgisi["ad"], kullanici_bilgisi["email"], kullanici_bilgisi["telefon"], kullanici_bilgisi["adres"], kullanici_bilgisi["rol"], "Düzenle", "Sil"))

        tree.pack(fill=tk.BOTH, expand=True)
        tree.bind("<Double-1>", self.kullanici_duzenle)
        tree.bind("<Button-3>", self.kullanici_sil)

    def kullanici_duzenle(self, event):
        """Kullanıcı düzenleme ekranını açar."""
        widget = event.widget
        if not widget.selection():
            messagebox.showwarning("Seçim Hatası", "Lütfen düzenlemek için bir kullanıcı seçin.")
            return

        item = widget.selection()[0]
        kullanici_id = widget.item(item, "values")[0]
        kullanici_bilgisi = self.kullanicilar.get(kullanici_id, {})

        # Kullanıcı bilgilerini formatla
        kullanici_bilgileri_str = (
            f"ID: {kullanici_id}\n"
            f"Ad: {kullanici_bilgisi.get('ad', '')}\n"
            f"E-posta: {kullanici_bilgisi.get('email', '')}\n"
            f"Telefon: {kullanici_bilgisi.get('telefon', '')}\n"
            f"Adres: {kullanici_bilgisi.get('adres', '')}\n"
            f"Rol: {kullanici_bilgisi.get('rol', '')}"
        )

        # Onay penceresi oluştur
        if messagebox.askyesno("Düzenleme Onayı", f"Aşağıdaki kullanıcıyı düzenlemek istediğinize emin misiniz?\n\n{kullanici_bilgileri_str}"):
            self.kullanici_guncelle_ekrani(kullanici_id)
            
    def kullanici_sil(self, event):
        """Kullanıcı silme işlemini yapar."""
        widget = event.widget
        if not widget.selection():
            messagebox.showwarning("Seçim Hatası", "Lütfen silmek için bir kullanıcı seçin.")
            return

        item = widget.selection()[0]
        kullanici_id = widget.item(item, "values")[0]
        kullanici_bilgisi = self.kullanicilar.get(kullanici_id, {})

        # Kullanıcı bilgilerini formatla
        mesaj = (
            f"ID: {kullanici_id}\n"
            f"Ad: {kullanici_bilgisi.get('ad', '')}\n"
            f"E-posta: {kullanici_bilgisi.get('email', '')}\n"
            f"Telefon: {kullanici_bilgisi.get('telefon', '')}\n"
            f"Adres: {kullanici_bilgisi.get('adres', '')}\n"
            f"Rol: {kullanici_bilgisi.get('rol', '')}\n\n"
            "Bu kullanıcıyı silmek istediğinize emin misiniz?"
        )

        if messagebox.askyesno("Silme Onayı", mesaj):
            del self.kullanicilar[kullanici_id]
            self.kullanicilari_kaydet(self.kullanici_dosya_adi, self.kullanicilar)
            self.kullanici_listesi_ekrani()

    def kullanici_guncelle_ekrani(self, kullanici_id):
        """Kullanıcı güncelleme ekranını oluşturur."""
        kullanici_bilgisi = self.kullanicilar.get(kullanici_id, {})

        ekrana = tk.Toplevel(self.root)
        ekrana.title(f"Kullanıcı Düzenleme: {kullanici_id}")

        tk.Label(ekrana, text="Ad").pack(pady=5)
        entry_ad = tk.Entry(ekrana)
        entry_ad.insert(0, kullanici_bilgisi.get("ad", ""))
        entry_ad.pack(pady=5)

        tk.Label(ekrana, text="E-posta").pack(pady=5)
        entry_email = tk.Entry(ekrana)
        entry_email.insert(0, kullanici_bilgisi.get("email", ""))
        entry_email.pack(pady=5)

        tk.Label(ekrana, text="Şifre").pack(pady=5)
        entry_sifre = tk.Entry(ekrana, show="*")
        entry_sifre.insert(0, kullanici_bilgisi.get("sifre", ""))
        entry_sifre.pack(pady=5)

        tk.Label(ekrana, text="Telefon").pack(pady=5)
        entry_telefon = tk.Entry(ekrana)
        entry_telefon.insert(0, kullanici_bilgisi.get("telefon", ""))
        entry_telefon.pack(pady=5)

        tk.Label(ekrana, text="Adres").pack(pady=5)
        entry_adres = tk.Entry(ekrana)
        entry_adres.insert(0, kullanici_bilgisi.get("adres", ""))
        entry_adres.pack(pady=5)

        tk.Label(ekrana, text="Rol").pack(pady=5)
        roles = ["admin", "user"]
        role_var = tk.StringVar(value=kullanici_bilgisi.get("rol", roles[1]))
        role_menu = tk.OptionMenu(ekrana, role_var, *roles)
        role_menu.pack(pady=5)

        button_guncelle = tk.Button(ekrana, text="Güncelle", command=lambda: self.kullanici_guncelle(kullanici_id, entry_ad.get(), entry_email.get(), entry_sifre.get(), entry_telefon.get(), entry_adres.get(), role_var.get(), ekrana))
        button_guncelle.pack(pady=10)

    def kullanici_guncelle(self, kullanici_id, ad, email, sifre, telefon, adres, rol, ekrana):
        """Kullanıcı bilgilerini günceller."""
        if ad and email and sifre and telefon and adres and rol:
            self.kullanicilar[kullanici_id] = {
                "ad": ad,
                "email": email,
                "sifre": sifre,
                "telefon": telefon,
                "adres": adres,
                "rol": rol
            }
            self.kullanicilari_kaydet(self.kullanici_dosya_adi, self.kullanicilar)
            ekrana.destroy()
            self.kullanici_listesi_ekrani()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurduğunuzdan emin olun.")