koleksi_dokumen = [
  "PENGEMBANGAN MODUL PEMBELAJARAN MATA KULIAH INTERNET OF THING (IOT) BERBASIS PROYEK (PROJECT BASED LEARNING)",
  "PENGEMBANGAN MODUL PADA MATA PELAJARAN INFORMATIKA BERBASIS PROJECT BASED LEARNING UNTUK MENINGKATKAN KETERAMPILAN KOLABORASI SISWA SMAN 4 SINJAI",
  "PENGARUH PENGGUNAAN E-MODUL TERHADAP HASIL BELAJAR SISWA PADA MATA PELAJARAN INFORMATIKA KELAS VIII SMP NEGERI 1 PANGSID",
  "PENGEMBANGAN CHATBOT BERBASIS MODEL SENTENCE-BERT UNTUK PENCARIAN ARTIKEL DAN MODEL BERT2BERT UNTUK PEMBUATAN RINGKASAN ARTIKEL OTOMATIS",
  "PEMBUATAN APLIKASI PORTAL BERITA MENGGUNAKAN FITUR WIDGET RECYCLEVIEW PADA ANDROID STUDIO",
  "PERANCANGAN SISTEM INFORMASI MANAJEMEN PERPUSTAKAAN BERBASIS WEBSITE",
  "PERANCANGAN DAN PEMBUATAN SISTEM INFORMASI PERCETAKAN BARANG PADA CU.SEVEN ADVERTISING PALOPO BERBASIS ONLINE",
  "IMPLEMENTASI SISTEM INFORMASI PADA SEKOLAH MENENGAH KEJURUAN (SMK) NUSA PRIMA LAMASI",
  "PERANCANGAN DAN PEMBUATAN E-LEARNING MATA PELAJARAN TEKNOLOGI INFORMASI DAN KOMUNIKASI PADA SMP NEGERI 1 PALOPO",
  "PEMBUATAN SISTEM INFORMASI AKADEMIK PADA SEKOLAH MENENGAH PERTAMA (SMP) NEGERI 3 BAJO"
]
print("Jumlah dokumen dalam koleksi:", len(koleksi_dokumen), "\n")

def preprocessing(teks):
  teks = teks.lower()
  tokens = teks.split()
  return tokens

def cari_dokumen(query, koleksi):
  query_tokens = preprocessing(query)
  hasil = []
  for idx, doc in enumerate(koleksi):
    doc_id = idx + 1
    doc_tokens = preprocessing(doc)
    skor = len(set(query_tokens) & set(doc_tokens))
    if skor > 0:
      hasil.append((doc_id, skor, doc))
  hasil.sort(key=lambda x: x[1], reverse=True)
  return hasil

def tampilkan_hasil(query, koleksi):
  print(f"Query : {query}")
  hasil = cari_dokumen(query, koleksi)
  if not hasil:
    print("Tidak ada Dokumen Yang Cocok")
  for (doc_id, skor, doc) in hasil:
    print(f"Dokumen {doc_id} | Skor: {skor} | ({doc})")
  print()
  return hasil

def precision_at_k(hasil_ids, relevan, k):
  if k == 0:
    return 0.0
  top_k = hasil_ids[:k]
  hit = sum(1 for d in top_k if d in relevan)
  return hit / k

def recall(hasil_ids, relevan):
  if len(relevan) == 0:
    return 0.0
  hit = sum(1 for d in hasil_ids if d in relevan)
  return hit / len(relevan)

def f1_score(p, r):
  if p + r == 0:
      return 0.0
  return 2 * p * r / (p + r)

def average_precision(hasil_ids, relevan):
  if len(relevan) == 0:
    return 0.0
  hit = 0
  total = 0.0
  for i, d in enumerate(hasil_ids, start=1):
    if d in relevan:
      hit += 1
      total += hit / i
  return total / len(relevan)

def evaluasi_query(query, koleksi, relevan, k):
  hasil = cari_dokumen(query, koleksi)
  hasil_ids = [doc_id for (doc_id, skor, doc) in hasil]
  p_at_k = precision_at_k(hasil_ids, relevan, k)
  r = recall(hasil_ids, relevan)
  f1 = f1_score(p_at_k, r)
  ap = average_precision(hasil_ids, relevan)
  print(f"Query               : {query}")
  print(f"Dokumen Relevan (GT): {sorted(relevan)}")
  print(f"Ranking Hasil       : {hasil_ids}")
  print(f"Precision@{k}       : {p_at_k:.4f}")
  print(f"Recall              : {r:.4f}")
  print(f"F1-Score            : {f1:.4f}")
  print(f"Average Precision   : {ap:.4f}")
  print()

  return ap

ground_truth = {
  "Informasi": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
  "Website": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
  "Pembelajaran": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
}

tampilkan_hasil("Informasi", koleksi_dokumen)
tampilkan_hasil("Website", koleksi_dokumen)
tampilkan_hasil("Pembelajaran", koleksi_dokumen)

daftar_ap = []
for query, relevan in ground_truth.items():
  ap = evaluasi_query(query, koleksi_dokumen, relevan, 3)
  daftar_ap.append(ap)

map_score = sum(daftar_ap) / len(daftar_ap)
print(f"Mean Average Precision (MAP) untuk {len(ground_truth)} query: {map_score:.4f}")