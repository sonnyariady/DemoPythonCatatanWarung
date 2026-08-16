import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

DB_FILE = "warung_madura.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Tabel Kategori
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kategori (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_kategori TEXT UNIQUE NOT NULL,
        deskripsi TEXT
    )
    ''')

    # 2. Tabel Barang
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS barang (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kode_barang TEXT UNIQUE NOT NULL,
        nama_barang TEXT NOT NULL,
        id_kategori INTEGER NOT NULL,
        harga_beli REAL NOT NULL DEFAULT 0,
        harga_jual REAL NOT NULL DEFAULT 0,
        stok INTEGER NOT NULL DEFAULT 0,
        satuan TEXT DEFAULT 'pcs',
        FOREIGN KEY (id_kategori) REFERENCES kategori(id)
    )
    ''')

    # 3. Tabel Transaksi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kode_transaksi TEXT UNIQUE NOT NULL,
        tanggal_transaksi DATETIME NOT NULL,
        total_harga REAL NOT NULL,
        metode_pembayaran TEXT DEFAULT 'Tunai',
        catatan TEXT
    )
    ''')

    # 4. Tabel Detail Transaksi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detail_transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_transaksi INTEGER NOT NULL,
        id_barang INTEGER NOT NULL,
        nama_barang TEXT NOT NULL,
        kategori TEXT NOT NULL,
        jumlah INTEGER NOT NULL,
        harga_satuan REAL NOT NULL,
        harga_beli_satuan REAL NOT NULL DEFAULT 0,
        subtotal REAL NOT NULL,
        FOREIGN KEY (id_transaksi) REFERENCES transaksi(id),
        FOREIGN KEY (id_barang) REFERENCES barang(id)
    )
    ''')

    # 5. Tabel Log Permintaan / Barang Dicari (Kehabisan Stok)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS log_permintaan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal DATETIME NOT NULL,
        nama_barang TEXT NOT NULL,
        id_kategori INTEGER,
        jumlah_permintaan INTEGER DEFAULT 1,
        status TEXT DEFAULT 'Habis',
        catatan TEXT,
        FOREIGN KEY (id_kategori) REFERENCES kategori(id)
    )
    ''')

    conn.commit()

    # Check if database has initial categories
    cursor.execute("SELECT COUNT(*) FROM kategori")
    if cursor.fetchone()[0] == 0:
        seed_sample_data(conn)

    conn.close()

def seed_sample_data(conn):
    cursor = conn.cursor()

    # Seed Kategori
    kategori_data = [
        ("Sembako", "Beras, Minyak, Telur, Gula, Terigu"),
        ("Rokok", "Aneka Merk Rokok"),
        ("Minuman", "Air Mineral, Kopi, Es Teh, Minuman Kemasan"),
        ("Makanan Ringan", "Snack, Biskuit, Mie Instan"),
        ("Gas & Galon", "Elpiji 3kg, Galon Aqua/Le Minerale"),
        ("Perlengkapan Mandi & Cuci", "Sabun, Shampo, Detergen"),
        ("Obat & Kesehatan", "Obat Bebas, Tolak Angin, Minyak Kayu Putih")
    ]
    cursor.executemany("INSERT INTO kategori (nama_kategori, deskripsi) VALUES (?, ?)", kategori_data)
    conn.commit()

    # Get Kategori IDs
    cursor.execute("SELECT id, nama_kategori FROM kategori")
    kat_dict = {row['nama_kategori']: row['id'] for row in cursor.fetchall()}

    # Seed Barang
    barang_data = [
        ("BRG-001", "Beras Ramos 5kg", kat_dict["Sembako"], 62000, 68000, 15, "karung"),
        ("BRG-002", "Minyak Goreng Bimoli 1L", kat_dict["Sembako"], 17500, 20000, 24, "pouch"),
        ("BRG-003", "Telur Ayam Ras (1 kg)", kat_dict["Sembako"], 25000, 28000, 30, "kg"),
        ("BRG-004", "Gula Pasir Gulaku 1kg", kat_dict["Sembako"], 14500, 17000, 20, "kg"),
        ("BRG-005", "Indomie Goreng Original", kat_dict["Makanan Ringan"], 2800, 3500, 120, "pcs"),
        ("BRG-006", "Indomie Kuah Ayam Bawang", kat_dict["Makanan Ringan"], 2700, 3300, 90, "pcs"),
        ("BRG-007", "Rokok Gudang Garam Surya 16", kat_dict["Rokok"], 31000, 34000, 40, "bungkus"),
        ("BRG-008", "Rokok Sampoerna Mild 16", kat_dict["Rokok"], 30000, 33500, 35, "bungkus"),
        ("BRG-009", "Le Minerale 600ml", kat_dict["Minuman"], 2500, 4000, 48, "botol"),
        ("BRG-010", "Kopi Kapal Api Special 165g", kat_dict["Minuman"], 12500, 15000, 15, "pcs"),
        ("BRG-011", "Teh Pucuk Harum 350ml", kat_dict["Minuman"], 2700, 4000, 36, "botol"),
        ("BRG-012", "Gas Elpiji 3kg (Melon)", kat_dict["Gas & Galon"], 17000, 21000, 8, "tabung"),
        ("BRG-013", "Galon Aqua (Isi Ulang Resmi)", kat_dict["Gas & Galon"], 16000, 20000, 5, "galon"),
        ("BRG-014", "Sabun Lifebuoy Red 110g", kat_dict["Perlengkapan Mandi & Cuci"], 3500, 5000, 25, "pcs"),
        ("BRG-015", "Deterjen Rinso Anti Noda 770g", kat_dict["Perlengkapan Mandi & Cuci"], 18000, 22000, 10, "pcs"),
        ("BRG-016", "Tolak Angin Cair (Pack)", kat_dict["Obat & Kesehatan"], 20000, 24000, 12, "pack"),
        ("BRG-017", "Minyak Kayu Putih Cap Lang 60ml", kat_dict["Obat & Kesehatan"], 21000, 25000, 3, "botol")
    ]
    cursor.executemany("""
    INSERT INTO barang (kode_barang, nama_barang, id_kategori, harga_beli, harga_jual, stok, satuan)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, barang_data)
    conn.commit()

    # Fetch barang list with categories for generating historical sales transactions
    cursor.execute("""
    SELECT b.id, b.nama_barang, b.harga_beli, b.harga_jual, k.nama_kategori
    FROM barang b
    JOIN kategori k ON b.id_kategori = k.id
    """)
    all_barang = cursor.fetchall()

    # Seed Transaksi (Penjualan 14 hari terakhir)
    now = datetime.now()
    metode_list = ["Tunai", "Tunai", "Tunai", "QRIS", "Transfer"]

    tr_counter = 1001
    for day_offset in range(14, -1, -1):
        tgl_base = now - timedelta(days=day_offset)
        # 3-7 transaksi per hari
        num_tx = random.randint(3, 7)
        for _ in range(num_tx):
            tx_time = tgl_base.replace(hour=random.randint(7, 22), minute=random.randint(0, 59), second=random.randint(0, 59))
            kode_tx = f"TRX-{tx_time.strftime('%Y%m%d')}-{tr_counter}"
            tr_counter += 1

            # Pick 1 - 4 items
            items_in_tx = random.sample(all_barang, random.randint(1, min(4, len(all_barang))))
            total_tx = 0
            details = []

            for item in items_in_tx:
                qty = random.randint(1, 4)
                subtotal = qty * item["harga_jual"]
                total_tx += subtotal
                details.append((
                    item["id"], item["nama_barang"], item["nama_kategori"],
                    qty, item["harga_jual"], item["harga_beli"], subtotal
                ))

            cursor.execute("""
            INSERT INTO transaksi (kode_transaksi, tanggal_transaksi, total_harga, metode_pembayaran, catatan)
            VALUES (?, ?, ?, ?, ?)
            """, (kode_tx, tx_time.strftime('%Y-%m-%d %H:%M:%S'), total_tx, random.choice(metode_list), "Transaksi regular"))

            tx_id = cursor.lastrowid

            for det in details:
                cursor.execute("""
                INSERT INTO detail_transaksi (id_transaksi, id_barang, nama_barang, kategori, jumlah, harga_satuan, harga_beli_satuan, subtotal)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (tx_id, det[0], det[1], det[2], det[3], det[4], det[5], det[6]))

    # Seed Log Permintaan Barang (Yang Kehabisan / Banyak Dicari)
    log_data = [
        ("Minyak Kayu Putih Cap Lang 60ml", kat_dict["Obat & Kesehatan"], 5, "Habis", "Stok cepat habis di malam hari"),
        ("Gas Elpiji 3kg (Melon)", kat_dict["Gas & Galon"], 12, "Habis", "Pengiriman dari agen terlambat"),
        ("Es Batu Kristal 1kg", kat_dict["Minuman"], 18, "Belum Dijual", "Banyak anak muda cari es batu malam hari"),
        ("Rokok Sampoerna Mild 16", kat_dict["Rokok"], 8, "Habis", "Dicari saat jam pulang kerja"),
        ("Galon Aqua (Isi Ulang Resmi)", kat_dict["Gas & Galon"], 7, "Habis", "Minta restok secepatnya"),
        ("Obat Paracetamol Bodrex", kat_dict["Obat & Kesehatan"], 4, "Belum Dijual", "Pembeli tanya obat pusing saset"),
        ("Rokok Gudang Garam Surya 16", kat_dict["Rokok"], 9, "Habis", "Pembeli langganan kehabisan"),
        ("Telur Ayam Ras (1 kg)", kat_dict["Sembako"], 6, "Habis", "Ibu-ibu borong pagi hari"),
        ("Bensin Eceran 1L", kat_dict["Sembako"], 15, "Belum Dijual", "Banyak pengendara motor tanya bensin eceran"),
        ("Susu Beruang Bear Brand", kat_dict["Minuman"], 10, "Belum Dijual", "Sering ditanyakan saat musim hujan")
    ]

    for item in log_data:
        tgl_log = now - timedelta(days=random.randint(0, 10), hours=random.randint(1, 12))
        cursor.execute("""
        INSERT INTO log_permintaan (tanggal, nama_barang, id_kategori, jumlah_permintaan, status, catatan)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (tgl_log.strftime('%Y-%m-%d %H:%M:%S'), item[0], item[1], item[2], item[3], item[4]))

    conn.commit()


# Helper Functions for UI CRUD
def get_kategori_df():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM kategori ORDER BY nama_kategori ASC", conn)
    conn.close()
    return df

def get_barang_df():
    conn = get_connection()
    query = """
    SELECT b.id, b.kode_barang, b.nama_barang, k.nama_kategori, b.id_kategori,
           b.harga_beli, b.harga_jual, (b.harga_jual - b.harga_beli) AS margin,
           b.stok, b.satuan
    FROM barang b
    JOIN kategori k ON b.id_kategori = k.id
    ORDER BY b.nama_barang ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_kategori(nama, deskripsi):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO kategori (nama_kategori, deskripsi) VALUES (?, ?)", (nama, deskripsi))
        conn.commit()
        return True, "Kategori berhasil ditambahkan!"
    except sqlite3.IntegrityError:
        return False, "Nama kategori sudah ada!"
    finally:
        conn.close()

def delete_kategori(kat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM barang WHERE id_kategori = ?", (kat_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False, "Kategori tidak bisa dihapus karena masih digunakan oleh barang!"
    cursor.execute("DELETE FROM kategori WHERE id = ?", (kat_id,))
    conn.commit()
    conn.close()
    return True, "Kategori berhasil dihapus!"

def add_barang(kode, nama, id_kategori, harga_beli, harga_jual, stok, satuan):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO barang (kode_barang, nama_barang, id_kategori, harga_beli, harga_jual, stok, satuan)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (kode, nama, id_kategori, harga_beli, harga_jual, stok, satuan))
        conn.commit()
        return True, "Barang berhasil ditambahkan!"
    except sqlite3.IntegrityError:
        return False, "Kode barang sudah terdaftar!"
    finally:
        conn.close()

def update_barang(id_barang, nama, id_kategori, harga_beli, harga_jual, stok, satuan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE barang 
    SET nama_barang = ?, id_kategori = ?, harga_beli = ?, harga_jual = ?, stok = ?, satuan = ?
    WHERE id = ?
    """, (nama, id_kategori, harga_beli, harga_jual, stok, satuan, id_barang))
    conn.commit()
    conn.close()
    return True, "Data barang berhasil diperbarui!"

def delete_barang(id_barang):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM barang WHERE id = ?", (id_barang,))
    conn.commit()
    conn.close()
    return True, "Barang berhasil dihapus!"

def process_transaction(items_cart, metode_pembayaran="Tunai", catatan=""):
    """
    items_cart is a list of dicts: [{'id': 1, 'nama_barang': '...', 'kategori': '...', 'harga_jual': 1000, 'harga_beli': 800, 'qty': 2, 'subtotal': 2000}]
    """
    if not items_cart:
        return False, "Keranjang belanja kosong!"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        now = datetime.now()
        cursor.execute("SELECT COUNT(*) FROM transaksi")
        tr_count = cursor.fetchone()[0] + 1
        kode_tx = f"TRX-{now.strftime('%Y%m%d')}-{tr_count:04d}"
        total_harga = sum(item['subtotal'] for item in items_cart)

        cursor.execute("""
        INSERT INTO transaksi (kode_transaksi, tanggal_transaksi, total_harga, metode_pembayaran, catatan)
        VALUES (?, ?, ?, ?, ?)
        """, (kode_tx, now.strftime('%Y-%m-%d %H:%M:%S'), total_harga, metode_pembayaran, catatan))

        id_tx = cursor.lastrowid

        for item in items_cart:
            cursor.execute("""
            INSERT INTO detail_transaksi (id_transaksi, id_barang, nama_barang, kategori, jumlah, harga_satuan, harga_beli_satuan, subtotal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_tx, item['id'], item['nama_barang'], item['kategori'], item['qty'], item['harga_jual'], item['harga_beli'], item['subtotal']))

            # Update stok barang
            cursor.execute("UPDATE barang SET stok = stok - ? WHERE id = ?", (item['qty'], item['id']))

        conn.commit()
        return True, f"Transaksi berhasil dicatat! Kode: {kode_tx}"
    except Exception as e:
        conn.rollback()
        return False, f"Gagal menyimpan transaksi: {str(e)}"
    finally:
        conn.close()

def log_barang_dicari(nama_barang, id_kategori, jumlah, status, catatan):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
    INSERT INTO log_permintaan (tanggal, nama_barang, id_kategori, jumlah_permintaan, status, catatan)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (now.strftime('%Y-%m-%d %H:%M:%S'), nama_barang, id_kategori, jumlah, status, catatan))
    conn.commit()
    conn.close()
    return True, "Permintaan barang kehabisan berhasil dicatat!"

def get_log_permintaan_df():
    conn = get_connection()
    query = """
    SELECT l.id, l.tanggal, l.nama_barang, k.nama_kategori, l.id_kategori, l.jumlah_permintaan, l.status, l.catatan
    FROM log_permintaan l
    LEFT JOIN kategori k ON l.id_kategori = k.id
    ORDER BY l.tanggal DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_report_kategori_df():
    conn = get_connection()
    query = """
    SELECT dt.kategori AS nama_kategori,
           SUM(dt.jumlah) AS total_qty_terjual,
           SUM(dt.subtotal) AS total_omset,
           SUM(dt.jumlah * (dt.harga_satuan - dt.harga_beli_satuan)) AS total_profit
    FROM detail_transaksi dt
    JOIN transaksi t ON dt.id_transaksi = t.id
    GROUP BY dt.kategori
    ORDER BY total_qty_terjual DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_report_item_df():
    conn = get_connection()
    query = """
    SELECT dt.nama_barang,
           dt.kategori AS nama_kategori,
           dt.harga_satuan AS harga_jual,
           dt.harga_beli_satuan AS harga_beli,
           (dt.harga_satuan - dt.harga_beli_satuan) AS profit_per_unit,
           SUM(dt.jumlah) AS total_qty_terjual,
           SUM(dt.subtotal) AS total_omset,
           SUM(dt.jumlah * (dt.harga_satuan - dt.harga_beli_satuan)) AS total_profit
    FROM detail_transaksi dt
    JOIN transaksi t ON dt.id_transaksi = t.id
    GROUP BY dt.nama_barang, dt.kategori
    ORDER BY total_qty_terjual DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_report_barang_dicari_df():
    conn = get_connection()
    query = """
    SELECT l.nama_barang,
           k.nama_kategori,
           l.status,
           SUM(l.jumlah_permintaan) AS frekuensi_dicari,
           COUNT(l.id) AS jumlah_kejadian,
           GROUP_CONCAT(DISTINCT l.catatan) AS daftar_catatan
    FROM log_permintaan l
    LEFT JOIN kategori k ON l.id_kategori = k.id
    GROUP BY l.nama_barang, k.nama_kategori, l.status
    ORDER BY frekuensi_dicari DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_all_transaksi_df():
    conn = get_connection()
    query = """
    SELECT t.id, t.kode_transaksi, t.tanggal_transaksi, t.total_harga, t.metode_pembayaran, t.catatan,
           COUNT(dt.id) AS jumlah_item_berbeda,
           SUM(dt.jumlah) AS total_qty
    FROM transaksi t
    LEFT JOIN detail_transaksi dt ON t.id = dt.id_transaksi
    GROUP BY t.id
    ORDER BY t.tanggal_transaksi DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
