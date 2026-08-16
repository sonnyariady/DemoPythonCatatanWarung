import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas dua-pass untuk Header dan Footer Bilingual ('Halaman X dari Y / Page X of Y')
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
        if self._pageNumber == 1:
            return
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1b4332"))
        
        # Header (Top bar)
        self.drawString(54, 805, "WARUNG MADURA DIGITAL — BILINGUAL USER MANUAL & TECHNICAL DOCS")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawRightString(541, 805, "Webinar Demo Python")
        
        self.setStrokeColor(colors.HexColor("#2d6a4f"))
        self.setLineWidth(0.75)
        self.line(54, 797, 541, 797)
        
        # Footer (Bottom bar)
        self.line(54, 52, 541, 52)
        self.drawString(54, 38, "Panduan Pengguna & Dokumentasi Teknis | User Manual & Technical Specs")
        page_text = f"Halaman / Page {self._pageNumber} dari / of {page_count}"
        self.drawRightString(541, 38, page_text)
        self.restoreState()


def build_bilingual_pdf(filename="Dokumentasi_Warung_Madura_Bilingual.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#1b4332")
    SECONDARY = colors.HexColor("#2d6a4f")
    ACCENT = colors.HexColor("#40916c")
    LIGHT_BG = colors.HexColor("#f8f9fa")
    BOX_BG = colors.HexColor("#e8f5e9")
    DARK_TEXT = colors.HexColor("#212529")
    MUTED_TEXT = colors.HexColor("#6c757d")
    EN_TEXT_COLOR = colors.HexColor("#1e3a8a")
    WARN_BG = colors.HexColor("#fff3cd")
    WARN_BORDER = colors.HexColor("#ffebaa")

    # Typography Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=30, textColor=PRIMARY, spaceAfter=8
    )

    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16, textColor=SECONDARY, spaceAfter=18
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=PRIMARY,
        spaceBefore=14, spaceAfter=6, keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=SECONDARY,
        spaceBefore=10, spaceAfter=4, keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=ACCENT,
        spaceBefore=8, spaceAfter=3, keepWithNext=True
    )

    style_id = ParagraphStyle(
        'Body_ID', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12, textColor=DARK_TEXT, spaceAfter=4
    )

    style_en = ParagraphStyle(
        'Body_EN', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=EN_TEXT_COLOR, spaceAfter=6
    )

    style_bullet_id = ParagraphStyle(
        'Bullet_ID', parent=style_id, leftIndent=12, firstLineIndent=-8, spaceAfter=2
    )

    style_bullet_en = ParagraphStyle(
        'Bullet_EN', parent=style_en, leftIndent=12, firstLineIndent=-8, spaceAfter=4
    )

    style_callout = ParagraphStyle(
        'Callout_Text', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.5, textColor=PRIMARY
    )

    style_code = ParagraphStyle(
        'Code_Text', parent=styles['Normal'],
        fontName='Courier', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#2b2b2b")
    )

    style_table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=DARK_TEXT
    )

    style_table_header = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("🏪 WARUNG MADURA DIGITAL", style_cover_title))
    story.append(Paragraph(
        "<b>DOKUMENTASI TERINTEGRASI & BILINGUAL (INDONESIA - ENGLISH)</b><br/>"
        "Panduan Pengguna Operasional & Spesifikasi Teknis Perangkat Lunak Berbasis Screenshot Nyata",
        style_cover_subtitle
    ))
    
    story.append(HRFlowable(width="100%", thickness=3, color=PRIMARY, spaceBefore=0, spaceAfter=12))
    
    # Webinar Context Box
    webinar_box_data = [[
        Paragraph(
            "<b>💡 CATATAN WEBINAR DEMO PYTHON | WEBINAR DEMO PYTHON CONTEXT:</b><br/>"
            "<b>🇮🇩 Bahasa Indonesia:</b> Aplikasi ini merupakan hasil praktik penerapan materi <b>Webinar Demo Python</b> "
            "yang membuktikan paradigma <i>'1 Aplikasi Bisa Untuk Semua'</i> (One Unified App) menggunakan Python, Streamlit, SQLite3, Pandas, & Plotly. "
            "Studi kasus <b>Warung Madura 24 Jam</b> dipilih karena membutuhkan kecepatan kasir tinggi, pencatatan stok, dan pelacakan barang kehabisan stok.<br/>"
            "<b>🇬🇧 English:</b> This application was built as a practical implementation of the <b>Python Demo Webinar</b>, "
            "proving the <i>'One Application Fits All'</i> paradigm using Python, Streamlit, SQLite3, Pandas, & Plotly. "
            "The <b>24-Hour Warung Madura</b> case study was selected due to its need for fast POS transactions, stock alerts, and out-of-stock demand tracking.",
            style_callout
        )
    ]]
    t_webinar = Table(webinar_box_data, colWidths=[487])
    t_webinar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BOX_BG),
        ('BOX', (0,0), (-1,-1), 1.2, SECONDARY),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_webinar)
    story.append(Spacer(1, 12))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Nama Aplikasi / App Name</b>", style_table_cell), Paragraph("Warung Madura Digital (Catatan Transaksi & Stok)", style_table_cell)],
        [Paragraph("<b>Technology Stack</b>", style_table_cell), Paragraph("Python 3.10+ | Streamlit | Pandas | SQLite3 | Plotly Express", style_table_cell)],
        [Paragraph("<b>Format Dokumentasi</b>", style_table_cell), Paragraph("Terintegrasi (User Manual + Technical Specs) & Bilingual", style_table_cell)],
        [Paragraph("<b>Tanggal / Date</b>", style_table_cell), Paragraph("Agustus / August 2026", style_table_cell)],
        [Paragraph("<b>Versi / Version</b>", style_table_cell), Paragraph("2.0.0 (Bilingual Document with Real UI Screenshots)", style_table_cell)],
    ]
    t_meta = Table(meta_data, colWidths=[140, 347])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>DAFTAR ISI / TABLE OF CONTENTS:</b>", style_h3))
    toc_text = """
    • <b>BAB 1 / CH. 1: LATAR BELAKANG WEBINAR & CONCEPT OVERVIEW</b><br/>
    • <b>BAB 2 / CH. 2: DASHBOARD UTAMA (MAIN DASHBOARD & OPERATIONAL METRICS)</b><br/>
    • <b>BAB 3 / CH. 3: MODUL KASIR & PENJUALAN (POS CASHIER & FAST OOS LOGGER)</b><br/>
    • <b>BAB 4 / CH. 4: DATA BARANG & KATEGORI MASTER (INVENTORY & MASTER CATEGORY)</b><br/>
    • <b>BAB 5 / CH. 5: LOG BARANG DICARI (OUT-OF-STOCK DEMAND ANALYTICS)</b><br/>
    • <b>BAB 6 / CH. 6: LAPORAN BISNIS & EKSPOR DATA (BUSINESS REPORTS & EXPORT)</b><br/>
    • <b>BAB 7 / CH. 7: SKEMA & SPESIFIKASI DATABASE SQLITE (`warung_madura.db`)</b><br/>
    • <b>BAB 8 / CH. 8: INSTALASI, DEPLOYMENT & MAINTENANCE BACKUP GUIDE</b>
    """
    story.append(Paragraph(toc_text, style_id))

    story.append(PageBreak())

    # Helper function to insert image with border
    def make_screenshot_table(img_path, caption_id, caption_en, width=470, height=240):
        elements = []
        if os.path.exists(img_path):
            img = Image(img_path, width=width, height=height)
            t_img = Table([[img]], colWidths=[width])
            t_img.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1, SECONDARY),
                ('PADDING', (0,0), (-1,-1), 2),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            elements.append(t_img)
            cap_text = f"<b>Gambar / Figure:</b> {caption_id} | <i>{caption_en}</i>"
            elements.append(Paragraph(cap_text, ParagraphStyle('Cap', parent=style_id, fontSize=7.5, textColor=MUTED_TEXT, alignment=1, spaceBefore=3, spaceAfter=8)))
        else:
            elements.append(Paragraph(f"<i>Image missing: {img_path}</i>", style_id))
        return elements

    # =========================================================================
    # CH 1: WEBINAR BACKGROUND & OVERVIEW
    # =========================================================================
    story.append(Paragraph("BAB 1 / CH. 1: LATAR BELAKANG WEBINAR & CONCEPT OVERVIEW", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Aplikasi ini dikembangkan sebagai bentuk pembuktian nyata dari <b>Webinar Demo Python</b>. "
        "Dua keunggulan utama yang dibuktikan adalah: (1) <b>1 Aplikasi Bisa Untuk Semua</b> — menggabungkan fungsi Kasir POS, Manajemen Stok, "
        "Pencatatan Barang Kehabisan, dan Analisis Bisnis ke dalam satu platform Web Streamlit; dan (2) <b>Studi Kasus Warung Madura</b> — "
        "menjawab tantangan operasional 24 jam dengan perputaran barang cepat dan kebutuhan rekap barang habis secara instan.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> This application was developed as a hands-on proof-of-concept from the <b>Python Demo Webinar</b>. "
        "Two core objectives were achieved: (1) <b>One Application Fits All</b> — integrating POS Cashier, Inventory Management, "
        "Out-of-Stock Demand Logger, and Business Intelligence into a single Streamlit platform; and (2) <b>Warung Madura Case Study</b> — "
        "addressing 24/7 operational challenges with high inventory turnover and instant restocking demand analytics.",
        style_en
    ))

    # =========================================================================
    # CH 2: DASHBOARD UTAMA
    # =========================================================================
    story.append(Paragraph("BAB 2 / CH. 2: DASHBOARD UTAMA & OPERATIONAL METRICS", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    # 1. User Manual
    story.append(Paragraph("📌 <b>PANDUAN OPERASIONAL PENGGUNA / USER OPERATING GUIDE:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Layar utama menampilkan 4 Ringkasan KPI Utama (Omset Total & Harian, Total Jenis Produk, Peringatan Stok Menipis/Habis, "
        "dan Log Barang Dicari). Di bawah metric card terdapat 2 grafik cepat Plotly yang memperlihatkan 5 Kategori Terlaris dan 5 Barang Paling Banyak Dicari.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> The main screen displays 4 Key Performance Indicators (Total & Today's Revenue, Total Product Count, Stock Warning Alerts, "
        "and Out-of-Stock Log Count). Below the metric cards are 2 interactive Plotly quick charts highlighting top selling categories and most demanded missing items.",
        style_en
    ))

    # 2. Screenshot
    story.extend(make_screenshot_table("screenshots/dashboard.png", "Tampilan Dashboard Utama Warung Madura Digital", "Main Dashboard UI View", height=230))

    # 3. Technical Implementation
    story.append(Paragraph("🛠️ <b>SPESIFIKASI & IMPLEMENTASI TEKNIS / TECHNICAL IMPLEMENTATION:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> `app.py` memangggil fungsi DAL `db.get_all_transaksi_df()`, `db.get_barang_df()`, dan `db.get_log_permintaan_df()`. "
        "Metrik omset dihitung dengan pandas filtering `tanggal_transaksi == today`. Visualisasi menggunakan `plotly.express.pie` dan `plotly.express.bar`.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> `app.py` invokes DAL functions `db.get_all_transaksi_df()`, `db.get_barang_df()`, and `db.get_log_permintaan_df()`. "
        "Today's revenue is computed via pandas date filtering. Visual charts are rendered dynamically using Plotly Express.",
        style_en
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 3: KASIR & PENJUALAN
    # =========================================================================
    story.append(Paragraph("BAB 3 / CH. 3: MODUL KASIR & PENJUALAN (POS CASHIER & FAST LOGGER)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    # 1. User Manual
    story.append(Paragraph("📌 <b>PANDUAN OPERASIONAL PENGGUNA / USER OPERATING GUIDE:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> 1. Cari produk dengan mengetik nama/kode. 2. Tentukan Qty & klik <b>➕ Tambah ke Keranjang</b>. "
        "3. Pilih metode pembayaran (Tunai/QRIS/Transfer) & input nominal uang untuk menghitung kembalian. 4. Klik <b>✅ Selesaikan Transaksi</b>. "
        "<i>Fitur Fast Logger:</i> Jika pembeli mencari barang yang habis, catat langsung di ekspander bagian bawah tanpa harus berpindah halaman.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> 1. Search products by name/SKU code. 2. Set Qty & click <b>➕ Add to Cart</b>. "
        "3. Choose payment method (Cash/QRIS/Transfer) & enter cash amount to calculate change. 4. Click <b>✅ Complete Transaction</b>. "
        "<i>Fast Logger Feature:</i> If a customer asks for an out-of-stock product, log it directly via the bottom expander form without leaving the checkout page.",
        style_en
    ))

    # 2. Screenshot
    story.extend(make_screenshot_table("screenshots/kasir.png", "Layar Kasir POS & Form Fast Out-of-Stock Logger", "POS Cashier Interface & Fast OOS Logger Form", height=230))

    # 3. Technical Implementation
    story.append(Paragraph("🛠️ <b>SPESIFIKASI & IMPLEMENTASI TEKNIS / TECHNICAL IMPLEMENTATION:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Keranjang belanja dikelola via Streamlit Session State `st.session_state.cart`. "
        "Saat checkout, `db.process_transaction()` mengeksekusi query INSERT ke `transaksi` & `detail_transaksi`, "
        "serta UPDATE stok pada `barang` dalam satu blok transaksi database atomic (`commit` / `rollback`).",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> The shopping cart is managed via Streamlit Session State `st.session_state.cart`. "
        "Upon checkout, `db.process_transaction()` executes atomic SQL INSERT statements for `transaksi` & `detail_transaksi`, "
        "and updates item quantities in `barang` inside a single database transaction block (`commit` / `rollback`).",
        style_en
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 4: DATA BARANG & KATEGORI
    # =========================================================================
    story.append(Paragraph("BAB 4 / CH. 4: DATA BARANG & KATEGORI MASTER (INVENTORY & CATEGORY)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    # 1. User Manual
    story.append(Paragraph("📌 <b>PANDUAN OPERASIONAL PENGGUNA / USER OPERATING GUIDE:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Pemilik warung dapat mengelola barang (Tambah, Edit Harga Beli/Jual, Update Stok, Hapus) "
        "dan kelola kategori master. Margin keuntungan (Harga Jual - Harga Beli) serta Badge Stok (🔴 HABIS, 🟡 MENIPIS &le;5, 🟢 AMAN) dihitung otomatis.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> Store owners can manage inventory (Add, Edit Cost/Selling Price, Update Stock, Delete) "
        "and category masters. Profit margins (Selling Price - Cost Price) and Stock Badges (🔴 OUT OF STOCK, 🟡 LOW STOCK &le;5, 🟢 SAFE) are calculated automatically.",
        style_en
    ))

    # 2. Screenshot
    story.extend(make_screenshot_table("screenshots/data_barang.png", "Kelola Inventaris Produk & Master Kategori", "Inventory Management & Master Category Tab", height=230))

    # 3. Technical Implementation
    story.append(Paragraph("🛠️ <b>SPESIFIKASI & IMPLEMENTASI TEKNIS / TECHNICAL IMPLEMENTATION:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Fungsi DAL: `add_barang()`, `update_barang()`, `delete_barang()`, `add_kategori()`, `delete_kategori()`. "
        "Fungsi `delete_kategori()` dilengkapi proteksi SQL `SELECT COUNT(*)` untuk mencegah penghapusan kategori yang masih terikat pada barang.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> DAL functions: `add_barang()`, `update_barang()`, `delete_barang()`, `add_kategori()`, `delete_kategori()`. "
        "`delete_kategori()` incorporates SQL constraint verification (`SELECT COUNT(*)`) to prevent deleting categories linked to existing products.",
        style_en
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 5: LOG BARANG DICARI
    # =========================================================================
    story.append(Paragraph("BAB 5 / CH. 5: LOG BARANG DICARI (OUT-OF-STOCK DEMAND ANALYTICS)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    # 1. User Manual
    story.append(Paragraph("📌 <b>PANDUAN OPERASIONAL PENGGUNA / USER OPERATING GUIDE:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Modul ini merekam barang apa saja yang ingin dibeli pelanggan namun stoknya habis atau belum dijual. "
        "Tabel Ranking mengurutkan pencarian terbanyak yang menjadi dasar acuan belanja grosir / kulakan.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> This module records items requested by customers that were out-of-stock or not yet offered. "
        "The Demand Ranking table sorts the most frequently requested products to guide wholesale restocking decisions.",
        style_en
    ))

    # 2. Screenshot
    story.extend(make_screenshot_table("screenshots/log_dicari.png", "Form Log Pencarian & Ranking Barang Kehabisan Stok", "Search Log Form & Out-of-Stock Demand Ranking", height=230))

    # 3. Technical Implementation
    story.append(Paragraph("🛠️ <b>SPESIFIKASI & IMPLEMENTASI TEKNIS / TECHNICAL IMPLEMENTATION:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Data disimpan di tabel `log_permintaan`. Query agregasi `db.get_report_barang_dicari_df()` "
        "menggunakan `GROUP BY l.nama_barang, k.nama_kategori` dan `SUM(jumlah_permintaan)` untuk menghasilkan rangking kebutuhan restok.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> Data is stored in `log_permintaan`. The aggregation query `db.get_report_barang_dicari_df()` "
        "uses `GROUP BY l.nama_barang, k.nama_kategori` and `SUM(jumlah_permintaan)` to generate demand restock rankings.",
        style_en
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 6: LAPORAN & EKSPOR DATA
    # =========================================================================
    story.append(Paragraph("BAB 6 / CH. 6: LAPORAN BISNIS & EKSPOR DATA (REPORTS & EXPORT)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    # 1. User Manual
    story.append(Paragraph("📌 <b>PANDUAN OPERASIONAL PENGGUNA / USER OPERATING GUIDE:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Modul Laporan memiliki 4 sub-tab: (1) Laporan Per Kategori, (2) Laporan Barang Dicari, "
        "(3) Detail Top 10 Produk Terlaris & Top 10 Penyumbang Profit, dan (4) Riwayat Penjualan beserta tombol **📄 Unduh CSV**.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> The Reports module features 4 tabs: (1) Sales by Category, (2) Out-of-Stock Analytics, "
        "(3) Top 10 Best Sellers & Top 10 Profit Contributors, and (4) Transaction History with **📄 Download CSV** buttons.",
        style_en
    ))

    # 2. Screenshot
    story.extend(make_screenshot_table("screenshots/laporan.png", "Analisis Grafik Plotly & Laporan Penjualan/Profit", "Plotly Analytics Charts & Sales/Profit Reports View", height=230))

    # 3. Technical Implementation
    story.append(Paragraph("🛠️ <b>SPESIFIKASI & IMPLEMENTASI TEKNIS / TECHNICAL IMPLEMENTATION:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Menggunakan query SQL agregasi `GROUP BY dt.kategori` dan `SUM(dt.jumlah * (dt.harga_satuan - dt.harga_beli_satuan))`. "
        "Ekspor CSV memanfaatkan `pandas.DataFrame.to_csv().encode('utf-8')` pada komponen Streamlit `st.download_button`.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> Uses SQL aggregation queries `GROUP BY dt.kategori` and `SUM(dt.jumlah * (dt.harga_satuan - dt.harga_beli_satuan))`. "
        "CSV export relies on `pandas.DataFrame.to_csv().encode('utf-8')` coupled with Streamlit's `st.download_button`.",
        style_en
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 7: SKEMA DATABASE SQLITE
    # =========================================================================
    story.append(Paragraph("BAB 7 / CH. 7: SKEMA DATABASE SQLITE (`warung_madura.db`)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Database `warung_madura.db` terdiri dari 5 tabel relasional terstruktur.<br/>"
        "<b>🇬🇧 English:</b> Database `warung_madura.db` consists of 5 structured relational tables.",
        style_id
    ))

    schema_tables = [
        [Paragraph("<b>Nama Tabel / Table Name</b>", style_table_header), Paragraph("<b>Kolom Utama / Primary Columns</b>", style_table_header), Paragraph("<b>Relasi & Deskripsi / Relations & Description</b>", style_table_header)],
        [Paragraph("<code>kategori</code>", style_table_cell), Paragraph("id (PK), nama_kategori, deskripsi", style_table_cell), Paragraph("Master kategori barang warung.", style_table_cell)],
        [Paragraph("<code>barang</code>", style_table_cell), Paragraph("id (PK), kode_barang, nama_barang, id_kategori, harga_beli, harga_jual, stok, satuan", style_table_cell), Paragraph("FK -> kategori(id). Master produk & harga modal/jual.", style_table_cell)],
        [Paragraph("<code>transaksi</code>", style_table_cell), Paragraph("id (PK), kode_transaksi, tanggal_transaksi, total_harga, metode_pembayaran, catatan", style_table_cell), Paragraph("Header transaksi penjualan kasir.", style_table_cell)],
        [Paragraph("<code>detail_transaksi</code>", style_table_cell), Paragraph("id (PK), id_transaksi, id_barang, nama_barang, kategori, jumlah, harga_satuan, harga_beli_satuan, subtotal", style_table_cell), Paragraph("FK -> transaksi(id), FK -> barang(id). Snapshot item terlaris.", style_table_cell)],
        [Paragraph("<code>log_permintaan</code>", style_table_cell), Paragraph("id (PK), tanggal, nama_barang, id_kategori, jumlah_permintaan, status, catatan", style_table_cell), Paragraph("FK -> kategori(id). Catatan barang kehabisan stok.", style_table_cell)],
    ]
    t_sch = Table(schema_tables, colWidths=[110, 180, 197])
    t_sch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sch)
    story.append(Spacer(1, 15))

    # =========================================================================
    # CH 8: INSTALASI & MAINTENANCE
    # =========================================================================
    story.append(Paragraph("BAB 8 / CH. 8: INSTALASI, DEPLOYMENT & MAINTENANCE", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("<b>1. Perintah Instalasi & Penjalanan / Execution Commands:</b>", style_h3))
    cmd_text = "pip install -r requirements.txt<br/>python -m streamlit run app.py"
    t_cmd = Table([[Paragraph(cmd_text, style_code)]], colWidths=[487])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>2. Strategi Backup Database / Database Maintenance Strategy:</b>", style_h3))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Karena SQLite bersifat *serverless* & *zero-configuration*, seluruh data bisnis tersimpan dalam file tunggal <code>warung_madura.db</code>. "
        "Lakukan copy/backup file ini ke Google Drive / Flashdisk secara berkala.<br/>"
        "<b>🇬🇧 English:</b> Because SQLite is *serverless* & *zero-configuration*, all business data resides in a single file <code>warung_madura.db</code>. "
        "Regularly copy/backup this file to external cloud storage or USB drives.",
        style_id
    ))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=10, spaceAfter=12))
    story.append(Paragraph(
        "<b>DOKUMENTASI TERINTEGRASI BILINGUAL — WARUNG MADURA DIGITAL</b><br/>"
        "<i>Hasil Praktik Webinar Demo Python | Practical Result of Python Demo Webinar</i>",
        ParagraphStyle('FooterNotice', parent=styles['Normal'], alignment=1, fontSize=8, textColor=MUTED_TEXT)
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Dokumen PDF Bilingual berhasil dibuat: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_bilingual_pdf()
