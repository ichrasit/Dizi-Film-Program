# Dizi ve ya Film girip girdiğimiz dizi ve ya filmi oylayıp izlenenler ve ya izlenmeyenler olarak ayıran bir program yazdım. 


import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog

class FilmSeriIzlemeTakipUygulamasiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Film/Seri İzleme Takip Uygulaması | Designed By ichrasit')

        self.baglanti = sqlite3.connect('film_seri_veritabani.db')
        self.cursor = self.baglanti.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS izleme_takip (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT,
                tur TEXT,
                izlendi BOOLEAN,
                puan INTEGER
            )
        ''')
        self.baglanti.commit()

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)

        self.film_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.film_tab, text='Film Ekle')

        self.dizi_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dizi_tab, text='Dizi Ekle')

        self.izlenenler_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.izlenenler_tab, text='İzlenenler')

        self.izlenmeyenler_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.izlenmeyenler_tab, text='İzlenmeyenler')

        self.notebook.pack(expand=1, fill="both")

        # Film Ekle Tab
        ttk.Label(self.film_tab, text='Film Adı:').grid(row=0, column=0, padx=10, pady=10)
        self.film_ad_entry = ttk.Entry(self.film_tab)
        self.film_ad_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.film_tab, text='Film Türü:').grid(row=1, column=0, padx=10, pady=10)
        self.film_tur_entry = ttk.Entry(self.film_tab)
        self.film_tur_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.film_tab, text='Film Ekle', command=self.film_ekle).grid(row=2, column=0, columnspan=2, pady=10)

        # Dizi Ekle Tab
        ttk.Label(self.dizi_tab, text='Dizi Adı:').grid(row=0, column=0, padx=10, pady=10)
        self.dizi_ad_entry = ttk.Entry(self.dizi_tab)
        self.dizi_ad_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.dizi_tab, text='Dizi Türü:').grid(row=1, column=0, padx=10, pady=10)
        self.dizi_tur_entry = ttk.Entry(self.dizi_tab)
        self.dizi_tur_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.dizi_tab, text='Dizi Ekle', command=self.dizi_ekle).grid(row=2, column=0, columnspan=2, pady=10)

        # İzlenenler Tab
        self.izlenenler_tree = ttk.Treeview(self.izlenenler_tab, columns=('Ad', 'Tür', 'Puan'), show='headings')
        self.izlenenler_tree.heading('Ad', text='Ad')
        self.izlenenler_tree.heading('Tür', text='Tür')
        self.izlenenler_tree.heading('Puan', text='Puan')
        self.izlenenler_tree.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(self.izlenenler_tab, text='Güncelle', command=self.izleme_durumu_guncelle_izlenenler).grid(row=1, column=0, pady=10)

        # İzlenmeyenler Tab
        self.izlenmeyenler_tree = ttk.Treeview(self.izlenmeyenler_tab, columns=('Ad', 'Tür', 'Puan'), show='headings')
        self.izlenmeyenler_tree.heading('Ad', text='Ad')
        self.izlenmeyenler_tree.heading('Tür', text='Tür')
        self.izlenmeyenler_tree.heading('Puan', text='Puan')
        self.izlenmeyenler_tree.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(self.izlenmeyenler_tab, text='Güncelle', command=self.izleme_durumu_guncelle_izlenmeyenler).grid(row=1, column=0, pady=10)

        self.load_izlenenler_tree()
        self.load_izlenmeyenler_tree()

    def film_ekle(self):
        ad = self.film_ad_entry.get()
        tur = self.film_tur_entry.get()
        self.cursor.execute('INSERT INTO izleme_takip (ad, tur, izlendi, puan) VALUES (?, ?, ?, ?)',
                            (ad, tur, False, None))
        self.baglanti.commit()
        print(f'{ad} filmi başarıyla eklendi.')
        self.film_ad_entry.delete(0, 'end')
        self.film_tur_entry.delete(0, 'end')
        self.load_izlenmeyenler_tree()  # İzlenmeyenler tabını güncelle

    def dizi_ekle(self):
        ad = self.dizi_ad_entry.get()
        tur = self.dizi_tur_entry.get()
        self.cursor.execute('INSERT INTO izleme_takip (ad, tur, izlendi, puan) VALUES (?, ?, ?, ?)',
                            (ad, tur, False, None))
        self.baglanti.commit()
        print(f'{ad} dizisi başarıyla eklendi.')
        self.dizi_ad_entry.delete(0, 'end')
        self.dizi_tur_entry.delete(0, 'end')
        self.load_izlenmeyenler_tree()  # İzlenmeyenler tabını güncelle

    def load_izlenenler_tree(self):
        self.cursor.execute('SELECT id, ad, tur, puan FROM izleme_takip WHERE izlendi = ?', (True,))
        izlenenler = self.cursor.fetchall()
        self._load_tree(self.izlenenler_tree, izlenenler)

    def load_izlenmeyenler_tree(self):
        self.cursor.execute('SELECT id, ad, tur, puan FROM izleme_takip WHERE izlendi = ?', (False,))
        izlenmeyenler = self.cursor.fetchall()
        self._load_tree(self.izlenmeyenler_tree, izlenmeyenler)

    def _load_tree(self, tree, data):
        tree.delete(*tree.get_children())
        for item in data:
            tree.insert('', 'end', values=(item[1], item[2], item[3]), iid=item[0])

    def izleme_durumu_guncelle_izlenenler(self):
        selected_item = self.izlenenler_tree.selection()
        if selected_item:
            film_id = selected_item[0]
            puan = self._get_puan_input()
            self.cursor.execute('UPDATE izleme_takip SET puan=? WHERE id=?', (puan, film_id))
            self.baglanti.commit()
            print('İzleme durumu güncellendi.')
            self.load_izlenenler_tree()
        else:
            print('Lütfen bir film seçin.')

    def izleme_durumu_guncelle_izlenmeyenler(self):
        selected_item = self.izlenmeyenler_tree.selection()
        if selected_item:
            film_id = selected_item[0]
            puan = self._get_puan_input()
            self.cursor.execute('UPDATE izleme_takip SET puan=?, izlendi=? WHERE id=?', (puan, True, film_id))
            self.baglanti.commit()
            print('İzleme durumu güncellendi.')
            self.load_izlenmeyenler_tree()
        else:
            print('Lütfen bir film seçin.')

    def _get_puan_input(self):
        puan = simpledialog.askinteger('Puan Ver', 'Puanınızı girin (1-5):', minvalue=1, maxvalue=5)
        return puan if puan else None

if __name__ == '__main__':
    root = tk.Tk()
    uygulama_gui = FilmSeriIzlemeTakipUygulamasiGUI(root)
    root.mainloop()
