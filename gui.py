import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import signal

class MatchTrackerApp:
    def __init__(self, master):
        self.master = master
        self.server_process = None
        self.selected_category = tk.StringVar()  # Kategori seçimi için
        master.title("Match Tracker")
        
        # Kategori seçimi
        self.category_label = tk.Label(
            master, 
            text="Kategori Seçimi:",
            font=("Arial", 10, "bold")
        )
        self.category_label.pack(pady=(10,5))
        
        # Radio buttons için frame
        self.category_frame = tk.Frame(master)
        self.category_frame.pack(pady=5)
        
        self.mini_sumo_rb = tk.Radiobutton(
            self.category_frame,
            text="Mini Sumo",
            value="mini_sumo",
            variable=self.selected_category
        )
        self.mini_sumo_rb.pack(side=tk.LEFT, padx=10)
        
        self.pul_toplayan_rb = tk.Radiobutton(
            self.category_frame,
            text="Pul Toplayan",
            value="pul_toplayan",
            variable=self.selected_category
        )
        self.pul_toplayan_rb.pack(side=tk.LEFT, padx=10)
        
        # URL input field
        self.url_label = tk.Label(master, text="Google Sheets URL:")
        self.url_label.pack(pady=(10,0))
        
        # Uyarı mesajı
        self.warning_label = tk.Label(
            master, 
            text="⚠️ Sheet dosyası herkese açık olmalıdır!", 
            fg="red",
            font=("Arial", 9, "italic")
        )
        self.warning_label.pack()
        
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack(pady=(5,10))
        self.url_entry.insert(0, "https://docs.google.com/spreadsheets/d/...")
        
        # Start Server button
        self.start_button = tk.Button(
            master, 
            text="Yayını Başlat", 
            command=self.start_server,
            width=20,
            height=2
        )
        self.start_button.pack(pady=10)

    def start_server(self):
        try:
            # Kategori seçimi kontrolü
            if not self.selected_category.get():
                messagebox.showwarning("Uyarı", "Lütfen bir kategori seçin!")
                return
            
            url = self.url_entry.get().strip()
            if not url or url == "https://docs.google.com/spreadsheets/d/...":
                messagebox.showwarning("Uyarı", "Lütfen geçerli bir Google Sheets URL'si girin")
                return
            
            os.environ['SHEETS_URL'] = url
            os.environ['CATEGORY'] = self.selected_category.get()  # Kategori bilgisini environment variable olarak gönder
            
            print(f"Seçilen kategori: {self.selected_category.get()}")
            print("Web sunucusu başlatılıyor...")
            
            self.server_process = subprocess.Popen(
                [sys.executable, 'webserver.py'], 
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            messagebox.showinfo("Bilgi", 
                "Web sunucusu başlatıldı!\nTarayıcınızdan http://localhost:5000 adresine gidebilirsiniz.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Sunucu başlatılırken hata oluştu: {e}")

    def on_closing(self):
        if self.server_process:
            print("Web sunucusu kapatılıyor...")
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.server_process.pid)])
            else:
                self.server_process.terminate()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MatchTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Pencere kapatıldığında on_closing çağrılır
    root.mainloop()