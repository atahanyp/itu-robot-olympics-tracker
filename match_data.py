import pandas as pd
import numpy as np
import re
import os

def fetch_data(sheet_url):
    def google_sheets_to_csv_url(sheet_url):
        # Sheet ID'yi ve gid'yi yakala
        sheet_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_url)
        gid_match = re.search(r'gid=([0-9]+)', sheet_url)

        if not sheet_id_match or not gid_match:
            raise ValueError("Geçerli bir Google Sheets URL'si girilmedi.")

        sheet_id = sheet_id_match.group(1)
        gid = gid_match.group(1)

        # CSV için uygun URL formatı
        csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
        return csv_url

    def dohyo_maclari_getir(df):
        # Mini Sumo için mevcut kod
        dohyolar = df['Dohyo'].unique()
        sonuc_df = pd.DataFrame()
        
        for dohyo in dohyolar:
            dohyo_df = df[df['Dohyo'] == dohyo].copy()
            
            oynanmamis = dohyo_df[
                ((dohyo_df['Skor 1'].isna()) | (dohyo_df['Skor 1'] == 0)) &
                ((dohyo_df['Skor 2'].isna()) | (dohyo_df['Skor 2'] == 0))
            ]
            gelecek_maclar = oynanmamis.head(3)
            
            oynanmis = dohyo_df[
                (~dohyo_df['Skor 1'].isna() & (dohyo_df['Skor 1'] != 0)) |
                (~dohyo_df['Skor 2'].isna() & (dohyo_df['Skor 2'] != 0))
            ]
            son_mac = oynanmis.tail(1)
            
            sonuc_df = pd.concat([sonuc_df, gelecek_maclar, son_mac])
        
        return sonuc_df[['Dohyo', 'Tur', '1. Köşe', 'Skor 1', 'Skor 2', '2. Köşe']].reset_index(drop=True)

    def pul_maclari_getir(df):
        # Pul Toplayan için yeni kod
        oynanmamis = df[
            ((df['Skor 1'].isna()) | (df['Skor 1'] == 0)) &
            ((df['Skor 2'].isna()) | (df['Skor 2'] == 0))
        ]
        gelecek_maclar = oynanmamis.head(3)
        
        oynanmis = df[
            (~df['Skor 1'].isna() & (df['Skor 1'] != 0)) |
            (~df['Skor 2'].isna() & (df['Skor 2'] != 0))
        ]
        son_mac = oynanmis.tail(1)
        sonuc_df = pd.concat([gelecek_maclar, son_mac])
        return sonuc_df[['Tur', '1. Köşe', 'Skor 1', 'Skor 2', '2. Köşe']].reset_index(drop=True)

    try:
        df = pd.read_csv(google_sheets_to_csv_url(sheet_url))
        df['1. Köşe'] = df['1. Köşe'].fillna("Henüz belirlenmedi")
        df['2. Köşe'] = df['2. Köşe'].fillna("Henüz belirlenmedi")
        df['Skor 1'] = df['Skor 1'].fillna(0).astype(int)
        df['Skor 2'] = df['Skor 2'].fillna(0).astype(int)
        
        category = os.environ.get('CATEGORY', 'mini_sumo')
        if category == 'mini_sumo':
            return dohyo_maclari_getir(df)
        else:
            return pul_maclari_getir(df)
    except Exception as e:
        print(f"Veri çekme hatası: {str(e)}")
        return pd.DataFrame()