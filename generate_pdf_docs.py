import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas dua-pass untuk menggambar Header dan Footer dengan penomoran halaman otomatis 'Halaman X dari Y'
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Skip header/footer on cover page (Page 1)
        if self._pageNumber == 1:
            return
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1b4332"))
        
        # Header (Top bar)
        self.drawString(54, 805, "WARUNG MADURA DIGITAL — DOKUMENTASI LENGKAP SYSTEM")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawRightString(541, 805, "Hasil Praktik Webinar Demo Python")
        
        self.setStrokeColor(colors.HexColor("#2d6a4f"))
        self.setLineWidth(0.75)
        self.line(54, 797, 541, 797)
        
        # Footer (Bottom bar)
        self.line(54, 52, 541, 52)
        self.drawString(54, 38, "Panduan Pengguna & Dokumentasi Teknis  |  Konsep: 1 Aplikasi Untuk Semua")
        page_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(541, 38, page_text)
        self.restoreState()


def build_pdf(filename="Dokumentasi_Warung_Madura.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#1b4332")
    SECONDARY = colors.HexColor("#2d6a4f")
    ACCENT = colors.HexColor("#40916c")
    LIGHT_BG = colors.HexColor("#f8f9fa")
    BOX_BG = colors.HexColor("#e8f5e9")
    DARK_TEXT = colors.HexColor("#212529")
    MUTED_TEXT = colors.HexColor("#6c757d")
    WARN_BG = colors.HexColor("#fff3cd")
    WARN_BORDER = colors.HexColor("#ffebaa")

    # Custom Paragraph Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=10
    )

    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=SECONDARY,
        alignment=0,
        spaceAfter=20
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=style_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    style_callout = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY,
        spaceBefore=3,
        spaceAfter=3
    )

    style_code = ParagraphStyle(
        'Code_Text',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2b2b2b")
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=DARK_TEXT
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("🏪 WARUNG MADURA DIGITAL", style_cover_title))
    story.append(Paragraph("Panduan Pengguna (User Manual) & Dokumentasi Teknis Sistem Kasir, Stok, dan Analisis Kehabisan Barang", style_cover_subtitle))
    
    story.append(HRFlowable(width="100%", thickness=3.5, color=PRIMARY, spaceBefore=0, spaceAfter=15))
    
    # Webinar Context Box
    webinar_box_data = [[
        Paragraph(
            "<b>💡 CATATAN LANDASAN PROYEK & WEBINAR DEMO PYTHON:</b><br/>"
            "Aplikasi ini dibangun sebagai bentuk <b>praktik penerapan nyata</b> dari materi <b>Webinar Demo Python</b>. "
            "Webinar tersebut membuktikan paradigma <i>'1 Aplikasi Bisa Untuk Semua'</i> (One Unified Application Framework) menggunakan "
            "ekosistem Python (Streamlit + SQLite + Pandas + Plotly). "
            "Studi kasus yang dipilih adalah <b>Warung Madura 24 Jam</b>, sebuah model bisnis ritel tradisional "
            "yang membutuhkan fleksibilitas tinggi, transaksi kasir super cepat, alert stok otomatis, dan pelacakan permintaan "
            "barang kehabisan stok (<i>Out-of-Stock Demand Analytics</i>).",
            style_callout
        )
    ]]
    t_webinar = Table(webinar_box_data, colWidths=[487])
    t_webinar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BOX_BG),
        ('BOX', (0,0), (-1,-1), 1.5, SECONDARY),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_webinar)
    story.append(Spacer(1, 20))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Nama Aplikasi</b>", style_table_cell), Paragraph("Warung Madura Digital (Catatan Transaksi & Stok)", style_table_cell)],
        [Paragraph("<b>Bahasa / Framework</b>", style_table_cell), Paragraph("Python 3.x | Streamlit | Pandas | SQLite3 | Plotly", style_table_cell)],
        [Paragraph("<b>Versi Dokumen</b>", style_table_cell), Paragraph("1.0.0 (Dokumentasi Resmi Lengkap)", style_table_cell)],
        [Paragraph("<b>Pengembang</b>", style_table_cell), Paragraph("Tim Peserta Webinar Demo Python", style_table_cell)],
        [Paragraph("<b>Tanggal Rilis</b>", style_table_cell), Paragraph("Agustus 2026", style_table_cell)],
        [Paragraph("<b>Cakupan Dokumen</b>", style_table_cell), Paragraph("Panduan Pengguna Operasional & Dokumentasi Arsitektur Perangkat Lunak", style_table_cell)],
    ]
    t_meta = Table(meta_data, colWidths=[140, 347])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>DAFTAR ISI DOKUMEN:</b>", style_h3))
    toc_text = """
    • <b>RINGKASAN EKSEKUTIF & KONSEP 1 APLIKASI UNTUK SEMUA</b><br/>
    • <b>BAGIAN I: PANDUAN PENGGUNA (USER MANUAL)</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;1. Dashboard Utama & Statistik Operasional<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;2. Kasir (Input Penjualan & Fast Out-of-Stock Logger)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;3. Kelola Data Barang, Margin Profit, & Kategori Master<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;4. Log Barang Dicari (Kehabisan Stok & Analytics)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;5. Laporan Bisnis, Visualisasi Chart, & Ekspor CSV<br/>
    • <b>BAGIAN II: DOKUMENTASI TEKNIS (TECHNICAL DOCUMENTATION)</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;6. Arsitektur Perangkat Lunak & Technology Stack<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;7. Skema & Spesifikasi 5 Tabel Database SQLite (`warung_madura.db`)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;8. Struktur Kode (`app.py` & `database.py`) & Function Reference<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;9. Workflow Transaksi, Atomic Rollback & Manajemen Stok<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;10. Panduan Instalasi, Deployment, & Strategi Backup Database
    """
    story.append(Paragraph(toc_text, style_body))

    story.append(PageBreak())

    # =========================================================================
    # EXECUTIVE SUMMARY & WEBINAR BACKGROUND
    # =========================================================================
    story.append(Paragraph("PENDAHULUAN: KONSEP WEBINAR DEMO PYTHON", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph(
        "Aplikasi <b>Warung Madura Digital</b> berawal dari komitmen untuk merealisasikan secara langsung "
        "pengetahuan dan pembuktian teknis yang diperoleh dari <b>Webinar Demo Python</b>. "
        "Dalam dunia pengembangan perangkat lunak modern, seringkali pelaku usaha mikro harus menggunakan "
        "banyak aplikasi terpisah: satu untuk kasir POS, satu untuk pencatatan stok, satu untuk laporan spreadsheet, "
        "dan pembukuan manual untuk mencatat pelanggan yang mencari barang yang stoknya sedang habis.",
        style_body
    ))

    story.append(Paragraph(
        "<b>Filosofi '1 Aplikasi Bisa Untuk Semua' (One Unified App):</b><br/>"
        "Melalui integrasi bahasa <b>Python</b> dengan framework UI <b>Streamlit</b> dan database embeddable <b>SQLite3</b>, "
        "seluruh kebutuhan operasional tersebut berhasil disatukan ke dalam **satu aplikasi tunggal** yang ringan, "
        "interaktif, dan dapat diakses langsung melalui browser Web lokal maupun cloud deployment.",
        style_body
    ))

    story.append(Paragraph(
        "<b>Studi Kasus Karakteristik Warung Madura 24 Jam:</b>", style_h2
    ))
    story.append(Paragraph("Warung Madura dipilih sebagai studi kasus ideal karena memiliki ciri khas operasional unik:", style_body))
    story.append(Paragraph("1. <b>Operasional 24 Jam Tanpa Henti</b>: Membutuhkan sistem pencatatan transaksi yang cepat, stabil, dan bebas kerumitan.", style_bullet))
    story.append(Paragraph("2. <b>Variasi Produk Sangat Beragam</b>: Mulai dari Sembako, Rokok, Minuman, Makanan Ringan, Gas Elpiji 3kg, Galon Air, hingga Obat-obatan.", style_bullet))
    story.append(Paragraph("3. <b>Sensitivitas Stok & Kehabisan Barang</b>: Pembeli sering menanyakan barang di malam hari. Jika stok habis atau belum dijual, warung kehilangan potensi omset.", style_bullet))
    story.append(Paragraph("4. <b>Kebutuhan Keputusan Restok Cepat</b>: Pemilik warung butuh data akurat barang apa yang paling sering dicari pembeli untuk belanja grosir (kulakan) berikutnya.", style_bullet))

    story.append(Spacer(1, 10))

    # =========================================================================
    # PART I: USER MANUAL (PANDUAN PENGGUNA)
    # =========================================================================
    story.append(Paragraph("BAGIAN I: PANDUAN PENGGUNA (USER MANUAL)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    # Bab 1
    story.append(Paragraph("BAB 1. Dashboard Utama & Navigasi Operasional", style_h2))
    story.append(Paragraph(
        "Saat pertama kali membuka aplikasi di alamat <code>http://localhost:8501</code>, pengguna akan disambut oleh "
        "<b>Dashboard Utama</b>. Dashboard ini menyajikan ringkasan eksekutif secara real-time mengenai performa toko.",
        style_body
    ))

    dash_features = [
        [Paragraph("<b>Elemen Dashboard</b>", style_table_header), Paragraph("<b>Fungsi & Informasi yang Ditampilkan</b>", style_table_header)],
        [Paragraph("<b>Header Banner</b>", style_table_cell), Paragraph("Menampilkan identitas 'Warung Madura Digital' dan status aktif operasional.", style_table_cell)],
        [Paragraph("<b>Card Omset Total & Harian</b>", style_table_cell), Paragraph("Menampilkan total omset akumulasi serta akumulasi omset & jumlah transaksi khusus hari ini.", style_table_cell)],
        [Paragraph("<b>Card Total Jenis Produk</b>", style_table_cell), Paragraph("Jumlah item barang yang terdaftar aktif beserta jumlah variasi kategori.", style_table_cell)],
        [Paragraph("<b>Card Peringatan Stok</b>", style_table_cell), Paragraph("Indikator otomatis (berwarna merah/oranye) untuk barang yang stoknya HABIS (0) atau MENIPIS (&le; 5).", style_table_cell)],
        [Paragraph("<b>Card Log Barang Dicari</b>", style_table_cell), Paragraph("Total kuantitas permintaan pelanggan atas barang kehabisan stok yang berhasil dicatat.", style_table_cell)],
        [Paragraph("<b>Quick Charts (Plotly)</b>", style_table_cell), Paragraph("Grafik donut 5 Kategori Terlaris dan grafik batang 5 Barang Paling Banyak Dicari.", style_table_cell)],
    ]
    t_dash = Table(dash_features, colWidths=[150, 337])
    t_dash.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_dash)
    story.append(Spacer(1, 10))

    # Bab 2
    story.append(Paragraph("BAB 2. Modul Kasir & Pencatatan Penjualan", style_h2))
    story.append(Paragraph(
        "Modul Kasir didesain untuk memproses transaksi belanja secara instan dan efisien. "
        "Layar terbagi menjadi dua bagian: <b>Kiri (Pencarian & Pemilihan Produk)</b> dan <b>Kanan (Keranjang & Pembayaran)</b>.",
        style_body
    ))

    story.append(Paragraph("<b>Langkah-Langkah Memproses Transaksi Penjualan:</b>", style_h3))
    story.append(Paragraph("1. <b>Cari Produk</b>: Ketik nama atau kode barang pada kotak pencarian (contoh: <i>'Indomie'</i>, <i>'Surya'</i>, <i>'Beras'</i>). Gunakan filter kategori jika diperlukan.", style_bullet))
    story.append(Paragraph("2. <b>Input Qty & Tambah</b>: Masukkan jumlah barang yang dibeli (sistem otomatis membatasi maksimal sesuai stok yang tersedia), lalu klik tombol <b>➕ Tambah ke Keranjang</b>.", style_bullet))
    story.append(Paragraph("3. <b>Review Keranjang Belanja</b>: Di panel kanan, periksa daftar produk, harga satuan, dan subtotal. Jika ada barang tambahan, ulangi langkah 1-2.", style_bullet))
    story.append(Paragraph("4. <b>Pilih Pembayaran & Nominal</b>: Pilih metode pembayaran (<i>Tunai, QRIS, Transfer Bank</i>). Masukkan nominal uang yang diterima dari pembeli.", style_bullet))
    story.append(Paragraph("5. <b>Hitung Kembalian & Simpan</b>: Sistem otomatis menghitung kembalian. Klik <b>✅ Selesaikan & Simpan Transaksi</b>. Stok barang di database akan berkurang secara otomatis.", style_bullet))

    story.append(Spacer(1, 6))
    # Out of Stock Fast Logger Callout Box
    logger_box_data = [[
        Paragraph(
            "<b>⚡ FITUR UNGGULAN: Fast Out-of-Stock Logger di Layar Kasir</b><br/>"
            "Jika pembeli menanyakan barang yang stoknya <b>HABIS</b> atau <b>BELUM DIJUAL</b> saat transaksi di kasir, "
            "kasir tidak perlu berpindah halaman! Cukup buka panel ekspansi <i>'Pembeli mencari barang yang Stoknya HABIS?'</i> "
            "di bawah form kasir, ketik nama barang, dan klik <b>📝 Simpan Catatan Barang Dicari</b>. Data ini langsung masuk ke analitik restok.",
            style_callout
        )
    ]]
    t_logger = Table(logger_box_data, colWidths=[487])
    t_logger.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WARN_BG),
        ('BOX', (0,0), (-1,-1), 1, WARN_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_logger)

    story.append(PageBreak())

    # Bab 3
    story.append(Paragraph("BAB 3. Kelola Data Barang & Kategori Master", style_h2))
    story.append(Paragraph(
        "Modul ini digunakan oleh pemilik warung untuk mengelola inventaris master barang dan kategori. "
        "Terdapat dua tab utama: <b>🏷️ Daftar & Olah Barang</b> dan <b>📂 Manajemen Kategori</b>.",
        style_body
    ))

    story.append(Paragraph("<b>Pengelolaan Master Barang:</b>", style_h3))
    story.append(Paragraph("• <b>Tambah Barang Baru</b>: Masukkan Kode Barang unik (misal: <i>BRG-018</i>), Nama Barang, Kategori, Satuan (<i>pcs, kg, botol, galon</i>), Harga Beli (Modal), Harga Jual, dan Stok Awal.", style_bullet))
    story.append(Paragraph("• <b>Edit Barang</b>: Pilih nama barang yang ingin diubah. Pemilik dapat memperbarui harga modal, harga jual, maupun menambah jumlah stok saat barang baru datang.", style_bullet))
    story.append(Paragraph("• <b>Hapus Barang</b>: Menghapus data barang dari katalog warung (dengan konfirmasi keamanan).", style_bullet))
    story.append(Paragraph("• <b>Margin & Status Stok Automatis</b>: Sistem menghitung margin keuntungan (Harga Jual - Harga Beli) serta memberi badge otomatis: "
                           "<font color='#ff4d4f'><b>🔴 HABIS</b></font> (stok 0), "
                           "<font color='#faad14'><b>🟡 MENIPIS</b></font> (stok &le; 5), dan "
                           "<font color='#52c41a'><b>🟢 AMAN</b></font> (stok > 5).", style_bullet))

    story.append(Paragraph("<b>Pengelolaan Master Kategori:</b>", style_h3))
    story.append(Paragraph("Pemilik warung bebas menambah kategori baru (misal: <i>'Gas & Galon'</i>, <i>'Perlengkapan Mandi'</i>) "
                           "atau menghapus kategori yang sudah tidak terpakai (dengan proteksi jika kategori masih digunakan barang).", style_body))

    story.append(Spacer(1, 8))

    # Bab 4
    story.append(Paragraph("BAB 4. Log Barang Dicari (Kehabisan Stok & Restok Analytics)", style_h2))
    story.append(Paragraph(
        "Salah satu kelemahan warung tradisional adalah tidak terdokumentasikannya hilangnya potensi penjualan (*lost sales*) "
        "akibat stok habis. Modul <b>Log Barang Dicari</b> memecahkan masalah ini secara elegan.",
        style_body
    ))

    story.append(Paragraph("<b>Keunggulan & Fungsi Modul Log Barang Dicari:</b>", style_h3))
    story.append(Paragraph("1. <b>Merekam Permintaan Pelanggan</b>: Setiap kali ada pelanggan mencari barang yang kosong, catat nama barang, kategori, jumlah permintaan, dan catatan (misal: <i>'tanya bensin eceran malam hari'</i>).", style_bullet))
    story.append(Paragraph("2. <b>Tabel Ranking Kebutuhan Restok</b>: Sistem mengelompokkan dan mengurutkan secara otomatis barang apa yang memiliki frekuensi pencarian tertinggi.", style_bullet))
    story.append(Paragraph("3. <b>Bahan Acuan Kulakan / Belanja Grosir</b>: Sebelum berangkat ke pasar induk/grosir, pemilik warung cukup membuka laporan ini untuk menentukan barang apa saja yang wajib dibeli.", style_bullet))

    story.append(Spacer(1, 8))

    # Bab 5
    story.append(Paragraph("BAB 5. Laporan & Analisis Data Bisnis", style_h2))
    story.append(Paragraph(
        "Modul Laporan memberikan analisis bisnis mendalam melalui 4 sub-tab interaktif yang dilengkapi grafik Plotly visual:",
        style_body
    ))

    lap_tabs = [
        [Paragraph("<b>Tab Laporan</b>", style_table_header), Paragraph("<b>Fokus Analisis & Visualisasi</b>", style_table_header)],
        [Paragraph("<b>📊 Per Kategori Terbanyak Dibeli</b>", style_table_cell), Paragraph("Grafik batang kuantitas terjual & pie chart proporsi omset nominal per kategori barang.", style_table_cell)],
        [Paragraph("<b>⚡ Barang Paling Dicari (Habis)</b>", style_table_cell), Paragraph("Grafik bar horizontal permintaan barang kehabisan stok & pie chart distribusi kategori hilang.", style_table_cell)],
        [Paragraph("<b>🏷️ Detail Per Jenis Item Barang</b>", style_table_cell), Paragraph("Ranking Top 10 Produk Terlaris (Qty) dan Top 10 Produk Penyumbang Profit Keuntungan Terbesar.", style_table_cell)],
        [Paragraph("<b>📜 Riwayat & Ekspor Data</b>", style_table_cell), Paragraph("Tabel seluruh transaksi historical & tombol unduh laporan transaksi lengkap dalam format CSV.", style_table_cell)],
    ]
    t_lap = Table(lap_tabs, colWidths=[160, 327])
    t_lap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_lap)

    story.append(PageBreak())

    # =========================================================================
    # PART II: TECHNICAL DOCUMENTATION (DOKUMENTASI TEKNIS)
    # =========================================================================
    story.append(Paragraph("BAGIAN II: DOKUMENTASI TEKNIS (TECHNICAL DOCUMENTATION)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    # Bab 6
    story.append(Paragraph("BAB 6. Arsitektur Perangkat Lunak & Technology Stack", style_h2))
    story.append(Paragraph(
        "Aplikasi <b>Warung Madura Digital</b> menggunakan pola arsitektur **Two-Tier Desktop/Web Application** "
        "yang memisahkan antara *Presentation Layer* (Streamlit UI) dan *Data Access Layer* (Database SQLite3 via Python standard library).",
        style_body
    ))

    tech_stack = [
        [Paragraph("<b>Komponen Stack</b>", style_table_header), Paragraph("<b>Teknologi</b>", style_table_header), Paragraph("<b>Peran & Deskripsi</b>", style_table_header)],
        [Paragraph("<b>Programming Language</b>", style_table_cell), Paragraph("Python 3.10+", style_table_cell), Paragraph("Bahasa utama logika bisnis, pemrosesan data, dan komunikasi database.", style_table_cell)],
        [Paragraph("<b>Web Application Framework</b>", style_table_cell), Paragraph("Streamlit 1.x", style_table_cell), Paragraph("Framework UI responsif berbasis deklaratif tanpa perlu HTML/JS kompleks.", style_table_cell)],
        [Paragraph("<b>Database Engine</b>", style_table_cell), Paragraph("SQLite3", style_table_cell), Paragraph("Relational Database embedded yang ringan, cepat, dan zero-configuration.", style_table_cell)],
        [Paragraph("<b>Data Processing</b>", style_table_cell), Paragraph("Pandas", style_table_cell), Paragraph("Manipulasi DataFrame, agregasi SQL ke Pandas, dan format ekspor CSV.", style_table_cell)],
        [Paragraph("<b>Data Visualization</b>", style_table_cell), Paragraph("Plotly Express", style_table_cell), Paragraph("Renderer grafik interaktif (Pie chart, Bar chart, Donut chart).", style_table_cell)],
    ]
    t_tech = Table(tech_stack, colWidths=[120, 100, 267])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # Bab 7
    story.append(Paragraph("BAB 7. Skema & Spesifikasi Database SQLite (`warung_madura.db`)", style_h2))
    story.append(Paragraph(
        "Database SQLite terdiri dari 5 tabel relasional yang dinormalisasi untuk menjaga integritas data transaksi dan inventaris:",
        style_body
    ))

    # Table Schema Summary
    story.append(Paragraph("<b>1. Tabel <code>kategori</code> (Master Kategori Barang)</b>", style_h3))
    schema_kat = [
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Keterangan", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID unik kategori", style_table_cell)],
        [Paragraph("nama_kategori", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("UNIQUE NOT NULL", style_table_cell), Paragraph("Nama kelompok barang", style_table_cell)],
        [Paragraph("deskripsi", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NULLABLE", style_table_cell), Paragraph("Penjelasan tambahan", style_table_cell)],
    ]
    t_skat = Table(schema_kat, colWidths=[100, 80, 160, 147])
    t_skat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_skat)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Tabel <code>barang</code> (Master Inventaris Produk)</b>", style_h3))
    schema_brg = [
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Keterangan", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID unik barang", style_table_cell)],
        [Paragraph("kode_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("UNIQUE NOT NULL", style_table_cell), Paragraph("Kode SKU/Barcode", style_table_cell)],
        [Paragraph("nama_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Nama produk warung", style_table_cell)],
        [Paragraph("id_kategori", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES kategori(id)", style_table_cell), Paragraph("Relasi ke tabel kategori", style_table_cell)],
        [Paragraph("harga_beli", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Harga modal (kulakan)", style_table_cell)],
        [Paragraph("harga_jual", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Harga jual ke konsumen", style_table_cell)],
        [Paragraph("stok", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Sisa jumlah fisik barang", style_table_cell)],
        [Paragraph("satuan", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("DEFAULT 'pcs'", style_table_cell), Paragraph("Satuan unit (pcs, kg, dll)", style_table_cell)],
    ]
    t_sbrg = Table(schema_brg, colWidths=[90, 75, 170, 152])
    t_sbrg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sbrg)

    story.append(PageBreak())

    story.append(Paragraph("<b>3. Tabel <code>transaksi</code> (Header Transaksi Penjualan)</b>", style_h3))
    schema_tx = [
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Keterangan", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID unik transaksi", style_table_cell)],
        [Paragraph("kode_transaksi", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("UNIQUE NOT NULL", style_table_cell), Paragraph("Format: TRX-YYYYMMDD-XXXX", style_table_cell)],
        [Paragraph("tanggal_transaksi", style_table_cell), Paragraph("DATETIME", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Waktu stempel transaksi", style_table_cell)],
        [Paragraph("total_harga", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Total nominal belanja", style_table_cell)],
        [Paragraph("metode_pembayaran", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("DEFAULT 'Tunai'", style_table_cell), Paragraph("Tunai / QRIS / Transfer", style_table_cell)],
        [Paragraph("catatan", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NULLABLE", style_table_cell), Paragraph("Catatan tambahan kasir", style_table_cell)],
    ]
    t_stx = Table(schema_tx, colWidths=[105, 80, 160, 142])
    t_stx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_stx)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>4. Tabel <code>detail_transaksi</code> (Item Rincian Penjualan)</b>", style_h3))
    schema_dtx = [
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Keterangan", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID rincian item", style_table_cell)],
        [Paragraph("id_transaksi", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES transaksi(id)", style_table_cell), Paragraph("Relasi ke header transaksi", style_table_cell)],
        [Paragraph("id_barang", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES barang(id)", style_table_cell), Paragraph("Relasi ke master barang", style_table_cell)],
        [Paragraph("nama_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Snapshot nama barang", style_table_cell)],
        [Paragraph("kategori", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Snapshot kategori barang", style_table_cell)],
        [Paragraph("jumlah", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Kuantitas dibeli (qty)", style_table_cell)],
        [Paragraph("harga_satuan", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Snapshot harga jual per unit", style_table_cell)],
        [Paragraph("harga_beli_satuan", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Snapshot harga modal per unit", style_table_cell)],
        [Paragraph("subtotal", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Jumlah * Harga Satuan", style_table_cell)],
    ]
    t_sdtx = Table(schema_dtx, colWidths=[105, 75, 160, 147])
    t_sdtx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sdtx)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>5. Tabel <code>log_permintaan</code> (Pencatatan Kehabisan Barang)</b>", style_h3))
    schema_log = [
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Keterangan", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID log", style_table_cell)],
        [Paragraph("tanggal", style_table_cell), Paragraph("DATETIME", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Waktu stempel pencarian", style_table_cell)],
        [Paragraph("nama_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Nama barang yang dicari", style_table_cell)],
        [Paragraph("id_kategori", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES kategori(id)", style_table_cell), Paragraph("Kategori barang", style_table_cell)],
        [Paragraph("jumlah_permintaan", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("DEFAULT 1", style_table_cell), Paragraph("Qty yang ditanyakan", style_table_cell)],
        [Paragraph("status", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("DEFAULT 'Habis'", style_table_cell), Paragraph("'Habis' / 'Belum Dijual'", style_table_cell)],
        [Paragraph("catatan", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NULLABLE", style_table_cell), Paragraph("Catatan konteks pembeli", style_table_cell)],
    ]
    t_slog = Table(schema_log, colWidths=[105, 75, 160, 147])
    t_slog.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_slog)

    story.append(Spacer(1, 10))

    # Bab 8
    story.append(Paragraph("BAB 8. Struktur Kode & API Function Reference (`database.py`)", style_h2))
    story.append(Paragraph(
        "Modul <code>database.py</code> bertindak sebagai Data Access Layer (DAL) yang mengisolasi seluruh SQL Query "
        "dari komponen antarmuka antarmuka <code>app.py</code>. Berikut adalah daftar fungsi utama:",
        style_body
    ))

    dal_funcs = [
        [Paragraph("<b>Nama Fungsi Python</b>", style_table_header), Paragraph("<b>Parameter Input</b>", style_table_header), Paragraph("<b>Output / Return Value</b>", style_table_header), Paragraph("<b>Deskripsi Fungsi DAL</b>", style_table_header)],
        [Paragraph("<code>init_db()</code>", style_table_cell), Paragraph("Tidak ada", style_table_cell), Paragraph("None", style_table_cell), Paragraph("Inisialisasi 5 tabel SQLite & seeder data otomatis jika DB kosong.", style_table_cell)],
        [Paragraph("<code>get_barang_df()</code>", style_table_cell), Paragraph("Tidak ada", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Query join master barang & kategori beserta kalkulasi margin profit.", style_table_cell)],
        [Paragraph("<code>process_transaction()</code>", style_table_cell), Paragraph("cart (list), metode, catatan", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Eksekusi transaksi atomic: insert header, insert detail, & update stok barang.", style_table_cell)],
        [Paragraph("<code>log_barang_dicari()</code>", style_table_cell), Paragraph("nama, id_kat, qty, status, notes", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Menyimpan log pencarian produk kehabisan stok ke tabel log_permintaan.", style_table_cell)],
        [Paragraph("<code>get_report_kategori_df()</code>", style_table_cell), Paragraph("Tidak ada", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Agregasi SUM(jumlah), SUM(subtotal), & SUM(profit) dikelompokkan per kategori.", style_table_cell)],
        [Paragraph("<code>get_report_barang_dicari_df()</code>", style_table_cell), Paragraph("Tidak ada", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Agregasi ranking pencarian barang kehabisan stok yang sering ditanyakan.", style_table_cell)],
    ]
    t_dal = Table(dal_funcs, colWidths=[120, 95, 95, 177])
    t_dal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_dal)

    story.append(PageBreak())

    # Bab 9
    story.append(Paragraph("BAB 9. Workflow Transaksi, Atomic Rollback & Manajemen Stok", style_h2))
    story.append(Paragraph(
        "Untuk menjamin konsistensi data penjualan di tengah transaksi berkecepatan tinggi, fungsi "
        "<code>process_transaction()</code> menerapkan prinsip <b>ACID Transactions</b> (Atomicity, Consistency, Isolation, Durability).",
        style_body
    ))

    code_snippet = """
def process_transaction(items_cart, metode_pembayaran="Tunai", catatan=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Generate Kode Transaksi Unik (TRX-YYYYMMDD-XXXX)
        # 2. INSERT INTO transaksi (Header)
        # 3. Loop items_cart:
        #    a. INSERT INTO detail_transaksi
        #    b. UPDATE barang SET stok = stok - qty WHERE id = item_id
        conn.commit()  # Simpan permanen jika seluruh item berhasil
        return True, "Transaksi berhasil dicatat!"
    except Exception as e:
        conn.rollback() # Batalkan seluruh perubahan jika terjadi error!
        return False, f"Gagal menyimpan transaksi: {str(e)}"
    finally:
        conn.close()
    """

    t_code = Table([[Paragraph(code_snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code)]], colWidths=[487])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f4f4f4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#dddddd")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)
    story.append(Spacer(1, 10))

    # Bab 10
    story.append(Paragraph("BAB 10. Panduan Instalasi, Deployment, & Pemeliharaan Database", style_h2))
    
    story.append(Paragraph("<b>1. Persyaratan Sistem & Dependensi (Prerequisites):</b>", style_h3))
    story.append(Paragraph("• Python 3.10 atau versi yang lebih baru installed di Windows / Linux / macOS.", style_bullet))
    story.append(Paragraph("• File `requirements.txt` yang memuat dependensi minimal:", style_bullet))

    req_text = "streamlit>=1.28.0<br/>pandas>=2.0.0<br/>plotly>=5.15.0"
    t_req = Table([[Paragraph(req_text, style_code)]], colWidths=[487])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_req)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Perintah Penjalankan Aplikasi:</b>", style_h3))
    story.append(Paragraph("Buka Terminal / Command Prompt pada direktori proyek, lalu jalankan perintah berikut:", style_body))

    cmd_text = "pip install -r requirements.txt<br/>python -m streamlit run app.py"
    t_cmd = Table([[Paragraph(cmd_text, style_code)]], colWidths=[487])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3. Strategi Pemeliharaan & Backup Database SQLite (`warung_madura.db`):</b>", style_h3))
    story.append(Paragraph("• <b>Zero Installation Server</b>: SQLite menyimpan seluruh data pada satu file <code>warung_madura.db</code>.", style_bullet))
    story.append(Paragraph("• <b>Prosedur Backup Rutin</b>: Cukup salin/copy file <code>warung_madura.db</code> ke media penyimpanan eksternal (Flashdisk / Google Drive) secara berkala (misal: setiap akhir pekan).", style_bullet))
    story.append(Paragraph("• <b>Pemulihan Data (Restore)</b>: Jika terjadi kegagalan hardware, cukup timpa file <code>warung_madura.db</code> dengan file cadangan backup.", style_bullet))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=10, spaceAfter=12))
    story.append(Paragraph(
        "<font color='#1b4332'><b>DOKUMEN INI DIBUAT DENGAN OTOMATISASI PYTHON REPORTLAB</b></font><br/>"
        "<i>Dokumentasi Lengkap User Manual & Teknis Warung Madura Digital — Hasil Praktik Webinar Demo Python</i>",
        ParagraphStyle('FooterNotice', parent=styles['Normal'], alignment=1, fontSize=8.5, textColor=MUTED_TEXT)
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Dokumen PDF berhasil dibuat: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_pdf()

