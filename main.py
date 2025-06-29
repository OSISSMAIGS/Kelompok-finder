from flask import Flask, render_template, request, jsonify
import json
import os
from difflib import SequenceMatcher

app = Flask(__name__)

# Fungsi untuk memuat data dari file JSON
def load_data():
    try:
        with open('kelompok.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return "data tidak ditemukan"

# Load data kelompok
data_kelompok = load_data()

def similarity(a, b):
    """Menghitung similarity antara dua string"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def cari_siswa(nama_input):
    """Mencari siswa berdasarkan input nama"""
    hasil = []
    
    for kelompok, info in data_kelompok.items():
        for peserta in info['peserta']:
            # Cek apakah input cocok dengan nama (case insensitive)
            if nama_input.lower() in peserta.lower():
                hasil.append({
                    'nama_lengkap': peserta,
                    'kelompok': kelompok,
                    'kakak_pembina': info['kakak_pembina'],
                    'similarity': similarity(nama_input, peserta)
                })
    
    # Urutkan berdasarkan similarity tertinggi, lalu alphabet
    hasil.sort(key=lambda x: (-x['similarity'], x['nama_lengkap']))
    
    return hasil

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cari', methods=['POST'])
def cari():
    nama = request.form.get('nama', '').strip()
    
    if not nama:
        return jsonify({'error': 'Nama tidak boleh kosong'})
    
    hasil = cari_siswa(nama)
    
    if not hasil:
        return jsonify({'error': f'Tidak ditemukan siswa dengan nama "{nama}"'})
    
    return jsonify({'hasil': hasil})

if __name__ == '__main__':
    app.run(debug=True)