import csv
import json

def csv_to_groups(csv_filepath, json_filepath):
    with open(csv_filepath, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    
    # Baris 0: nama-nama kelompok (dengan banyak kolom kosong di antaranya)
    header_groups = reader[0]
    # Baris 1: Kakak Pembina: Nama
    header_pembina = reader[1]
    
    # Tentukan indeks kolom setiap kelompok: kelompok adalah segmen kolom non-empty yang dipisah minimal 1 kolom kosong
    group_indices = []
    i = 0
    n_cols = len(header_groups)
    while i < n_cols:
        if header_groups[i].strip():  # awal segmen
            start = i
            while i < n_cols and header_groups[i].strip():
                i += 1
            end = i  # exclusive
            group_indices.append((start, end))
        else:
            i += 1
    
    result = {}
    for start, end in group_indices:
        # Nama kelompok (misal "KELOMPOK 1.1") → ubah menjadi "Kelompok 1.1"
        raw_group = header_groups[start].strip().title()
        
        # Ambil nama kakak pembina: split setelah ":" lalu strip
        raw_pembina = header_pembina[start].split(":", 1)[1].strip()
        
        result[raw_group] = {
            "kakak_pembina": raw_pembina,
            "peserta": []
        }
    
    # Baris selanjutnya: data peserta. Setiap baris memuat satu peserta per kelompok di segmennya masing-masing
    for row in reader[3:]:  # mulai dari baris ke-3 (0-based), karena baris 2 adalah header kolom No./Nama/L/P
        for start, end in group_indices:
            # Di setiap segmen, kolom 0 adalah no., kolom 1 nama, kolom 2 gender (kita abaikan gender)
            # Pastikan ada cukup kolom di row
            if start+1 < len(row) and row[start+1].strip():
                nama = row[start+1].strip()
                # Hilangkan spasi ekstra ganda
                nama = " ".join(nama.split())
                group_key = header_groups[start].strip().title()
                result[group_key]["peserta"].append(nama)
    
    # Tulis ke JSON dengan indentasi 2 spasi
    with open(json_filepath, 'w', encoding='utf-8') as j:
        json.dump(result, j, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    num = 14
    csv_path = f"kelompok{num}.csv"     # ganti dengan path file CSV Anda
    json_path = f"kelompok{num}.json"  # ganti dengan path output yang diinginkan
    csv_to_groups(csv_path, json_path)
    print(f"Berhasil menulis JSON ke {json_path}")
