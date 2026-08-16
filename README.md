# 🏪 Aplikasi Catatan Transaksi & Stok Warung Madura

Aplikasi Web Kasir, Pencatatan Transaksi, Pengelolaan Stok, dan Laporan Analisis Kategori Terlaris & Barang Kehabisan Stok untuk Warung Madura berbasis **Python**, **Streamlit**, **Pandas**, dan **SQLite3**.

> 💡 **Keterangan Proyek**: Aplikasi ini merupakan hasil praktik penerapan materi dari mengikuti **Webinar Demo Python**, yang kemudian diaplikasikan dan dikembangkan lebih lanjut menjadi aplikasi nyata untuk pencatatan usaha Warung Madura.

---

## 🛠️ Teknologi yang Digunakan
- **Python 3** (Backend & Logic)
- **Streamlit** (Web UI Framework)
- **Pandas** (Pengolahan & Analisis Data)
- **SQLite3** (Database Lokal)
- **Plotly Express** (Visualisasi Grafik Interaktif)

---

## 🚀 Fitur Utama
1. **📊 Dashboard Utama**: Ringkasan omset harian, keuntungan, total transaksi, dan alert stok menipis/habis.
2. **🛒 Kasir & Input Transaksi**: Pencatatan transaksi penjualan multi-item cepat dengan kembalian otomatis & tombol catat barang kehabisan.
3. **📦 Data Barang & Kategori**: Manajemen inventaris produk (stok, harga beli, harga jual, satuan) dan kategori barang.
4. **🔍 Log Barang Dicari (Kehabisan)**: Pencatatan khusus barang yang dicari/ditanyakan pembeli tetapi stoknya sedang habis/kosong (*Out of Stock Demand Analytics*).
5. **📈 Laporan & Analisis Data**:
   - Laporan Kategori Paling Banyak Dibeli (Tabel + Chart).
   - Laporan Barang Paling Banyak Dicari / Kehabisan Stok.
   - Laporan Detail Per Jenis Item Barang (Profit margin & top selling products).
   - Ekspor Laporan ke format CSV.

---

## 💻 Cara Menjalankan Secara Lokal

1. Clone repositori ini:
   ```bash
   git clone https://github.com/sonnyariady/DemoPythonCatatanWarung.git
   cd DemoPythonCatatanWarung
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi Streamlit:
   ```bash
   python -m streamlit run app.py
   ```

4. Buka browser di `http://localhost:8501`.
