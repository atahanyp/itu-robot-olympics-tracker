from flask import Flask, jsonify, render_template
import sys
import os
from match_data import fetch_data
import threading
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, 
           template_folder=resource_path('templates'),
           static_folder=resource_path('static'))

latest_data = []

def update_data():
    global latest_data
    sheets_url = os.environ.get('SHEETS_URL')
    if not sheets_url:
        print("HATA: SHEETS_URL environment variable bulunamadı!")
        return
        
    while True:
        try:
            print("Veriler güncelleniyor...")
            latest_data = fetch_data(sheets_url)
            print("Veriler güncellendi!")
            time.sleep(60)
        except Exception as e:
            print(f"Veri güncelleme hatası: {e}")
            time.sleep(10)

@app.route('/')
def index():
    category = os.environ.get('CATEGORY', 'mini_sumo')
    if category == 'mini_sumo':
        return render_template('index.html')
    else:
        return render_template('pul_toplayan.html')

@app.route('/api/matches')
def get_matches():
    sheet_url = os.environ.get('SHEETS_URL')
    data = fetch_data(sheet_url)
    return jsonify(data.to_dict('records'))

if __name__ == '__main__':
    # Debug modunu kapatalım ve daha fazla log ekleyelim
    print("Web sunucusu başlatılıyor...")
    threading.Thread(target=update_data, daemon=True).start()
    app.run(debug=True, port=5000)
    print("Web sunucusu başlatıldı: http://localhost:5000")
