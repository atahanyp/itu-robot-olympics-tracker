import tkinter as tk
from gui import MatchTrackerApp
import sys

def main():
    try:
        root = tk.Tk()
        root.geometry("400x500")
        root.title("Match Tracker")
        
        print("Uygulama başlatılıyor...")
        app = MatchTrackerApp(root)
        
        # Pencere kapatma olayını yakala ama hemen kapatma
        def on_closing():
            if tk.messagebox.askokcancel("Çıkış", "Uygulamayı kapatmak istiyor musunuz?"):
                app.on_closing()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        print("GUI oluşturuldu, hazır...")
        root.mainloop()
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    main()