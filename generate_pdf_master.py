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
        self.drawString(54, 805, "WARUNG MADURA DIGITAL — MASTER DOCUMENTATION (USER & TECH DOCS)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawRightString(541, 805, "Webinar Demo Python")
        
        self.setStrokeColor(colors.HexColor("#2d6a4f"))
        self.setLineWidth(0.75)
        self.line(54, 797, 541, 797)
        
        # Footer (Bottom bar)
        self.line(54, 52, 541, 52)
        self.drawString(54, 38, "Panduan Pengguna & Dokumentasi Teknis Master | Master User & Technical Documentation")
        page_text = f"Halaman / Page {self._pageNumber} dari / of {page_count}"
        self.drawRightString(541, 38, page_text)
        self.restoreState()


def build_master_pdf(filename="Dokumentasi_Warung_Madura_Master.pdf"):
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
        fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=PRIMARY, spaceAfter=8
    )

    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16, textColor=SECONDARY, spaceAfter=16
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=PRIMARY,
        spaceBefore=14, spaceAfter=6, keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=SECONDARY,
        spaceBefore=10, spaceAfter=4, keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=ACCENT,
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
        "<b>MASTER DOCUMENTATION: PANDUAN PENGGUNA & SPESIFIKASI TEKNIS LENGKAP</b><br/>"
        "Unified Bilingual Manual (Indonesia - English) with Real UI Screenshots & Deep Technical Specs",
        style_cover_subtitle
    ))
    
    story.append(HRFlowable(width="100%", thickness=3, color=PRIMARY, spaceBefore=0, spaceAfter=12))
    
    # Webinar Context Box
    webinar_box_data = [[
        Paragraph(
            "<b>💡 CATATAN LANDASAN WEBINAR DEMO PYTHON | PYTHON DEMO WEBINAR CONTEXT:</b><br/>"
            "<b>🇮🇩 Bahasa Indonesia:</b> Aplikasi ini dikembangkan sebagai bentuk pembuktian nyata dari <b>Webinar Demo Python</b> "
            "dengan paradigma <i>'1 Aplikasi Bisa Untuk Semua'</i> (One Unified App). Mengintegrasikan fungsi Kasir POS, Inventaris Stok, "
            "Pencatatan Kehabisan Barang, dan Laporan Analisis ke dalam satu platform Web Streamlit untuk studi kasus <b>Warung Madura 24 Jam</b>.<br/>"
            "<b>🇬🇧 English:</b> Built as a practical application of the <b>Python Demo Webinar</b>, proving the <i>'One Application Fits All'</i> "
            "paradigm. It unifies POS Cashier, Inventory Management, Out-of-Stock Demand Logging, and Business Intelligence into a single Streamlit platform tailored for a <b>24/7 Warung Madura</b> store.",
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
    story.append(Spacer(1, 10))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Nama Aplikasi / App Name</b>", style_table_cell), Paragraph("Warung Madura Digital (Catatan Transaksi & Stok)", style_table_cell)],
        [Paragraph("<b>Technology Stack</b>", style_table_cell), Paragraph("Python 3.10+ | Streamlit | Pandas | SQLite3 | Plotly Express", style_table_cell)],
        [Paragraph("<b>Cakupan Dokumentasi</b>", style_table_cell), Paragraph("Master Combined (User Manual + Full Technical Specs) Bilingual", style_table_cell)],
        [Paragraph("<b>Tanggal / Date</b>", style_table_cell), Paragraph("Agustus / August 2026", style_table_cell)],
        [Paragraph("<b>Versi Dokumen</b>", style_table_cell), Paragraph("3.0.0 Master Final Edition (With Code Structure & DAL API Specs)", style_table_cell)],
    ]
    t_meta = Table(meta_data, colWidths=[140, 347])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>DAFTAR ISI / TABLE OF CONTENTS:</b>", style_h3))
    toc_text = """
    • <b>CH. 1: ARSITEKTUR PERANGKAT LUNAK & STRUKTUR KODE (CODE STRUCTURE)</b><br/>
    • <b>CH. 2: DASHBOARD UTAMA (MAIN DASHBOARD & OPERATIONAL METRICS)</b><br/>
    • <b>CH. 3: MODUL KASIR & WORKFLOW TRANSAKSI (POS CASHIER & ACID CODE)</b><br/>
    • <b>CH. 4: DATA BARANG & KATEGORI MASTER (INVENTORY & MARGIN MATH)</b><br/>
    • <b>CH. 5: LOG BARANG DICARI (OUT-OF-STOCK DEMAND ANALYTICS)</b><br/>
    • <b>CH. 6: LAPORAN BISNIS & EKSPOR DATA (BUSINESS REPORTS & EXPORT)</b><br/>
    • <b>CH. 7: SPESIFIKASI LENGKAP 5 TABEL DATABASE SQLITE (`warung_madura.db`)</b><br/>
    • <b>CH. 8: REFERENSI LENGKAP FUNGSI API DATA ACCESS LAYER (`database.py`)</b><br/>
    • <b>CH. 9: INSTALASI, DEPLOYMENT & MAINTENANCE BACKUP STRATEGY</b>
    """
    story.append(Paragraph(toc_text, style_id))

    story.append(PageBreak())

    # Helper function to insert image with border
    def make_screenshot_table(img_path, caption_id, caption_en, width=470, height=220):
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
            elements.append(Paragraph(cap_text, ParagraphStyle('Cap', parent=style_id, fontSize=7.5, textColor=MUTED_TEXT, alignment=1, spaceBefore=2, spaceAfter=6)))
        return elements

    # =========================================================================
    # CH 1: CODE STRUCTURE & SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("CH. 1: ARSITEKTUR PERANGKAT LUNAK & STRUKTUR KODE (SOFTWARE ARCHITECTURE)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Aplikasi `Warung Madura Digital` mengadopsi pola arsitektur **Two-Tier Layered Architecture** "
        "yang memisahkan secara tegas antarmuka pengguna (*Presentation Layer*) di file `app.py` dan lapisan akses data (*Data Access Layer - DAL*) di file `database.py`.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> The `Warung Madura Digital` application adopts a **Two-Tier Layered Architecture** "
        "strictly separating the user interface (*Presentation Layer*) in `app.py` and the Data Access Layer (*DAL*) in `database.py`.",
        style_en
    ))

    arch_data = [
        [Paragraph("<b>File / Module</b>", style_table_header), Paragraph("<b>Peran & Komponen Utama / Primary Role</b>", style_table_header), Paragraph("<b>Deskripsi Teknis / Technical Description</b>", style_table_header)],
        [Paragraph("<code>app.py</code>", style_table_cell), Paragraph("Presentation Layer & UI Controller", style_table_cell), Paragraph("Mengelola layout Streamlit, CSS styling, session state cart, routing menu sidebar, & visualisasi Plotly charts.", style_table_cell)],
        [Paragraph("<code>database.py</code>", style_table_cell), Paragraph("Data Access Layer (DAL) & SQL Helper", style_table_cell), Paragraph("Mengelola koneksi SQLite `warung_madura.db`, inisialisasi 5 tabel, transaksi atomic, & query agregasi pandas.", style_table_cell)],
        [Paragraph("<code>warung_madura.db</code>", style_table_cell), Paragraph("SQLite Embedded Database File", style_table_cell), Paragraph("Penyimpanan file terenkapsulasi zero-server yang menyimpan 5 tabel relasional toko.", style_table_cell)],
    ]
    t_arch = Table(arch_data, colWidths=[110, 160, 217])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # =========================================================================
    # CH 2: DASHBOARD UTAMA
    # =========================================================================
    story.append(Paragraph("CH. 2: DASHBOARD UTAMA & OPERATIONAL METRICS", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Layar utama menampilkan 4 KPI Card (Omset Total/Harian, Total Jenis Produk, Peringatan Stok Menipis/Habis, "
        "dan Log Barang Dicari) serta 2 Grafik Plotly cepat.<br/>"
        "<b>🇬🇧 English:</b> The main dashboard presents 4 KPI Cards (Total/Today Revenue, Product Count, Stock Warning Alerts, "
        "and OOS Log Count) plus 2 Plotly quick charts.",
        style_id
    ))

    story.extend(make_screenshot_table("screenshots/dashboard.png", "Tampilan Dashboard Utama Warung Madura Digital", "Main Dashboard UI View", height=210))

    story.append(Paragraph("🛠️ <b>IMPLEMENTASI TEKNIS / TECHNICAL IMPLEMENTATION:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> `app.py` memanggil `db.get_all_transaksi_df()`, `db.get_barang_df()`, & `db.get_log_permintaan_df()`. "
        "Metrik harian dihitung via Pandas `df_transaksi[tanggal_only == today_str]['total_harga'].sum()`. Grafik dibuat dengan `plotly.express.pie` & `bar`.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> `app.py` queries `db.get_all_transaksi_df()`, `db.get_barang_df()`, & `db.get_log_permintaan_df()`. "
        "Daily metrics are computed via Pandas date filtering. Charts are dynamically generated using `plotly.express.pie` & `bar`.",
        style_en
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 3: KASIR & PENJUALAN
    # =========================================================================
    story.append(Paragraph("CH. 3: MODUL KASIR & WORKFLOW TRANSAKSI (POS CASHIER & ACID CODE)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Pencarian produk instan, keranjang belanja multi-item, kalkulator kembalian otomatis, "
        "dan fitur ekspander *Fast Out-of-Stock Logger* di layar kasir.<br/>"
        "<b>🇬🇧 English:</b> Instant product search, multi-item cart, automatic change calculator, and an embedded *Fast Out-of-Stock Logger* form.",
        style_id
    ))

    story.extend(make_screenshot_table("screenshots/kasir.png", "Layar Kasir POS & Form Fast Out-of-Stock Logger", "POS Cashier Interface & Fast OOS Logger Form", height=210))

    story.append(Paragraph("🛠️ <b>TRANSAKSI ATOMIC & POTONGAN KODE (`database.py`):</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Menggunakan transaksi atomic ACID (`commit` / `rollback`) saat memproses keranjang belanja.",
        style_id
    ))

    code_snippet = """
def process_transaction(items_cart, metode_pembayaran="Tunai", catatan=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Insert Header Transaksi (transaksi)
        cursor.execute("INSERT INTO transaksi VALUES (?, ?, ?, ?, ?)", (kode_tx, now, total, metode, catatan))
        id_tx = cursor.lastrowid
        # 2. Insert Detail Item & Update Stok Physical (detail_transaksi & barang)
        for item in items_cart:
            cursor.execute("INSERT INTO detail_transaksi VALUES (...)", (id_tx, item['id'], ...))
            cursor.execute("UPDATE barang SET stok = stok - ? WHERE id = ?", (item['qty'], item['id']))
        conn.commit()  # Simpan permanen jika seluruh item berhasil
        return True, "Transaksi berhasil dicatat!"
    except Exception as e:
        conn.rollback() # Batalkan seluruh perubahan jika terjadi error!
        return False, str(e)
    finally:
        conn.close()
    """

    t_code = Table([[Paragraph(code_snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code)]], colWidths=[487])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f4f4f4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#dddddd")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code)

    story.append(PageBreak())

    # =========================================================================
    # CH 4: DATA BARANG & KATEGORI
    # =========================================================================
    story.append(Paragraph("CH. 4: DATA BARANG & KATEGORI MASTER (INVENTORY & MARGIN MATH)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Pengelolaan master barang & kategori. Hitungan margin profit (Harga Jual - Harga Beli) "
        "serta Badge Status Stok (🔴 HABIS, 🟡 MENIPIS &le;5, 🟢 AMAN) dihitung otomatis.<br/>"
        "<b>🇬🇧 English:</b> Product & category master CRUD. Profit margins (Selling - Cost Price) and Stock Badges (🔴 OOS, 🟡 LOW &le;5, 🟢 SAFE) are auto-calculated.",
        style_id
    ))

    story.extend(make_screenshot_table("screenshots/data_barang.png", "Kelola Inventaris Produk & Master Kategori", "Inventory Management & Master Category Tab", height=210))

    story.append(Paragraph("🛠️ <b>FUNGSI DAL UNTUK INVENTARIS / DAL FUNCTIONS:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> `add_barang()`, `update_barang()`, `delete_barang()`, `add_kategori()`, `delete_kategori()`. "
        "Penghapusan kategori dilindungi query `SELECT COUNT(*)` untuk memastikan tidak ada barang yang kehilangan referensi FK.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> `add_barang()`, `update_barang()`, `delete_barang()`, `add_kategori()`, `delete_kategori()`. "
        "Category deletion is protected by a `SELECT COUNT(*)` check to ensure no orphaned FK references.",
        style_en
    ))

    story.append(Spacer(1, 6))

    # =========================================================================
    # CH 5: LOG BARANG DICARI
    # =========================================================================
    story.append(Paragraph("CH. 5: LOG BARANG DICARI (OUT-OF-STOCK DEMAND ANALYTICS)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Merekam barang yang dicari pelanggan tapi stoknya habis atau belum dijual. "
        "Tabel Ranking mengurutkan pencarian terbanyak sebagai acuan belanja grosir / kulakan.<br/>"
        "<b>🇬🇧 English:</b> Records items requested by customers that were out-of-stock or not offered. The Demand Ranking table guides restocking decisions.",
        style_id
    ))

    story.extend(make_screenshot_table("screenshots/log_dicari.png", "Form Log Pencarian & Ranking Barang Kehabisan Stok", "Search Log Form & Out-of-Stock Demand Ranking", height=210))

    story.append(Paragraph("🛠️ <b>AGREGASI SQL REKAP DICARI / SQL QUERY:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Query DAL `get_report_barang_dicari_df()`:<br/>"
        "<code>SELECT l.nama_barang, k.nama_kategori, l.status, SUM(l.jumlah_permintaan) AS frekuensi_dicari, COUNT(l.id) AS jumlah_kejadian "
        "FROM log_permintaan l LEFT JOIN kategori k ON l.id_kategori = k.id GROUP BY l.nama_barang, k.nama_kategori, l.status ORDER BY frekuensi_dicari DESC</code>",
        style_id
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 6: LAPORAN BISNIS & EKSPOR DATA
    # =========================================================================
    story.append(Paragraph("CH. 6: LAPORAN BISNIS & EKSPOR DATA (BUSINESS REPORTS & EXPORT)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> 4 sub-tab laporan interaktif: Analisis Kategori, Barang Kehabisan, Top 10 Terlaris & Profit, "
        "serta Riwayat Transaksi & Tombol Unduh CSV.<br/>"
        "<b>🇬🇧 English:</b> 4 interactive report tabs: Category Sales, Out-of-Stock Analytics, Top 10 Best Sellers & Profit, and History with CSV Downloads.",
        style_id
    ))

    story.extend(make_screenshot_table("screenshots/laporan.png", "Analisis Grafik Plotly & Laporan Penjualan/Profit", "Plotly Analytics Charts & Sales/Profit Reports View", height=210))

    story.append(Paragraph("🛠️ <b>AGREGASI PROFIT & EKSPOR CSV / PROFIT MATH & CSV EXPORT:</b>", style_h2))
    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Formula profit per item: `SUM(dt.jumlah * (dt.harga_satuan - dt.harga_beli_satuan))`. "
        "Ekspor CSV menggunakan `df.to_csv(index=False).encode('utf-8')` pada Streamlit `st.download_button`.",
        style_id
    ))
    story.append(Paragraph(
        "<b>🇬🇧 English:</b> Item profit formula: `SUM(dt.jumlah * (dt.harga_satuan - dt.harga_beli_satuan))`. "
        "CSV export relies on `df.to_csv(index=False).encode('utf-8')` wired to Streamlit `st.download_button`.",
        style_en
    ))

    story.append(PageBreak())

    # =========================================================================
    # CH 7: SKEMA LENGKAP 5 TABEL SQLITE
    # =========================================================================
    story.append(Paragraph("CH. 7: SPESIFIKASI LENGKAP 5 TABEL DATABASE SQLITE (`warung_madura.db`)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Detail skema struktur kolom-per-kolom untuk seluruh 5 tabel relasional pada `warung_madura.db`.<br/>"
        "<b>🇬🇧 English:</b> Column-by-column schema specification for all 5 relational tables in `warung_madura.db`.",
        style_id
    ))

    # 1. kategori
    story.append(Paragraph("<b>1. Tabel <code>kategori</code> (Master Kategori Barang / Category Master)</b>", style_h3))
    t_kat = Table([
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Description (ID / EN)", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID unik kategori / Unique Category ID", style_table_cell)],
        [Paragraph("nama_kategori", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("UNIQUE NOT NULL", style_table_cell), Paragraph("Nama kategori / Category name", style_table_cell)],
        [Paragraph("deskripsi", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NULLABLE", style_table_cell), Paragraph("Deskripsi kategori / Description", style_table_cell)],
    ], colWidths=[90, 70, 160, 167])
    t_kat.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")), ('PADDING', (0,0), (-1,-1), 3.5)]))
    story.append(t_kat)
    story.append(Spacer(1, 6))

    # 2. barang
    story.append(Paragraph("<b>2. Tabel <code>barang</code> (Master Inventaris Produk / Product Inventory Master)</b>", style_h3))
    t_brg = Table([
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Description (ID / EN)", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID unik barang / Unique product ID", style_table_cell)],
        [Paragraph("kode_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("UNIQUE NOT NULL", style_table_cell), Paragraph("Kode SKU/Barcode / SKU Code", style_table_cell)],
        [Paragraph("nama_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Nama produk / Product name", style_table_cell)],
        [Paragraph("id_kategori", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES kategori(id)", style_table_cell), Paragraph("Relasi kategori / FK to category", style_table_cell)],
        [Paragraph("harga_beli", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Harga modal / Cost price", style_table_cell)],
        [Paragraph("harga_jual", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Harga jual / Selling price", style_table_cell)],
        [Paragraph("stok", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Jumlah stok / Stock quantity", style_table_cell)],
        [Paragraph("satuan", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("DEFAULT 'pcs'", style_table_cell), Paragraph("Satuan unit / Unit (pcs, kg, etc)", style_table_cell)],
    ], colWidths=[80, 65, 165, 177])
    t_brg.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")), ('PADDING', (0,0), (-1,-1), 3)]))
    story.append(t_brg)

    story.append(PageBreak())

    # 3. transaksi
    story.append(Paragraph("<b>3. Tabel <code>transaksi</code> (Header Transaksi Penjualan / Sales Header)</b>", style_h3))
    t_tx = Table([
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Description (ID / EN)", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID transaksi / Transaction ID", style_table_cell)],
        [Paragraph("kode_transaksi", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("UNIQUE NOT NULL", style_table_cell), Paragraph("Kode TRX-YYYYMMDD-XXXX", style_table_cell)],
        [Paragraph("tanggal_transaksi", style_table_cell), Paragraph("DATETIME", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Waktu transaksi / Timestamp", style_table_cell)],
        [Paragraph("total_harga", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Total belanja / Total price", style_table_cell)],
        [Paragraph("metode_pembayaran", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("DEFAULT 'Tunai'", style_table_cell), Paragraph("Tunai/QRIS/Transfer", style_table_cell)],
        [Paragraph("catatan", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NULLABLE", style_table_cell), Paragraph("Catatan kasir / Cashier notes", style_table_cell)],
    ], colWidths=[95, 75, 155, 162])
    t_tx.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")), ('PADDING', (0,0), (-1,-1), 3.5)]))
    story.append(t_tx)
    story.append(Spacer(1, 6))

    # 4. detail_transaksi
    story.append(Paragraph("<b>4. Tabel <code>detail_transaksi</code> (Item Rincian Penjualan / Sales Line Items)</b>", style_h3))
    t_dtx = Table([
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Description (ID / EN)", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID rincian item / Line item ID", style_table_cell)],
        [Paragraph("id_transaksi", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES transaksi(id)", style_table_cell), Paragraph("FK ke header / FK to header", style_table_cell)],
        [Paragraph("id_barang", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES barang(id)", style_table_cell), Paragraph("FK ke produk / FK to product", style_table_cell)],
        [Paragraph("nama_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Snapshot nama / Product name", style_table_cell)],
        [Paragraph("kategori", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Snapshot kategori / Category", style_table_cell)],
        [Paragraph("jumlah", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Kuantitas (Qty) / Quantity", style_table_cell)],
        [Paragraph("harga_satuan", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Snapshot harga jual / Unit price", style_table_cell)],
        [Paragraph("harga_beli_satuan", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("DEFAULT 0", style_table_cell), Paragraph("Snapshot harga modal / Cost price", style_table_cell)],
        [Paragraph("subtotal", style_table_cell), Paragraph("REAL", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Subtotal (Qty * Harga Satuan)", style_table_cell)],
    ], colWidths=[95, 70, 155, 167])
    t_dtx.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")), ('PADDING', (0,0), (-1,-1), 3)]))
    story.append(t_dtx)
    story.append(Spacer(1, 6))

    # 5. log_permintaan
    story.append(Paragraph("<b>5. Tabel <code>log_permintaan</code> (Pencatatan Kehabisan Barang / Out-of-Stock Demand Log)</b>", style_h3))
    t_slog = Table([
        [Paragraph("Column Name", style_table_header), Paragraph("Data Type", style_table_header), Paragraph("Constraints", style_table_header), Paragraph("Description (ID / EN)", style_table_header)],
        [Paragraph("id", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", style_table_cell), Paragraph("ID log / Log ID", style_table_cell)],
        [Paragraph("tanggal", style_table_cell), Paragraph("DATETIME", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Waktu stempel / Timestamp", style_table_cell)],
        [Paragraph("nama_barang", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NOT NULL", style_table_cell), Paragraph("Nama barang dicari / Item name", style_table_cell)],
        [Paragraph("id_kategori", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("FK REFERENCES kategori(id)", style_table_cell), Paragraph("FK ke kategori / FK to category", style_table_cell)],
        [Paragraph("jumlah_permintaan", style_table_cell), Paragraph("INTEGER", style_table_cell), Paragraph("DEFAULT 1", style_table_cell), Paragraph("Qty ditanyakan / Requested Qty", style_table_cell)],
        [Paragraph("status", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("DEFAULT 'Habis'", style_table_cell), Paragraph("'Habis' / 'Belum Dijual'", style_table_cell)],
        [Paragraph("catatan", style_table_cell), Paragraph("TEXT", style_table_cell), Paragraph("NULLABLE", style_table_cell), Paragraph("Catatan konteks / Notes", style_table_cell)],
    ], colWidths=[95, 70, 155, 167])
    t_slog.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")), ('PADDING', (0,0), (-1,-1), 3)]))
    story.append(t_slog)

    story.append(PageBreak())

    # =========================================================================
    # CH 8: REFERENSI LENGKAP FUNGSI API DAL (database.py)
    # =========================================================================
    story.append(Paragraph("CH. 8: REFERENSI LENGKAP FUNGSI API DATA ACCESS LAYER (`database.py`)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "<b>🇮🇩 Bahasa Indonesia:</b> Tabel lengkap referensi 13+ fungsi Data Access Layer (DAL) pada modul `database.py`.<br/>"
        "<b>🇬🇧 English:</b> Complete reference table of all 13+ Data Access Layer (DAL) functions in `database.py`.",
        style_id
    ))

    dal_funcs_all = [
        [Paragraph("<b>Function Name</b>", style_table_header), Paragraph("<b>Parameters</b>", style_table_header), Paragraph("<b>Return Type</b>", style_table_header), Paragraph("<b>Description (ID / EN)</b>", style_table_header)],
        [Paragraph("<code>init_db()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("None", style_table_cell), Paragraph("Inisialisasi 5 tabel SQLite & seeder otomatis jika DB kosong.<br/><i>Initializes 5 tables & seeds sample data if DB is empty.</i>", style_table_cell)],
        [Paragraph("<code>get_connection()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("sqlite3.Connection", style_table_cell), Paragraph("Membuka koneksi ke `warung_madura.db` dengan row_factory SQLite.Row.<br/><i>Opens SQLite connection with row_factory.</i>", style_table_cell)],
        [Paragraph("<code>seed_sample_data()</code>", style_table_cell), Paragraph("conn", style_table_cell), Paragraph("None", style_table_cell), Paragraph("Seeding data awal kategori, 17 barang, transaksi 14 hari, & log permintaan.<br/><i>Seeds initial categories, products, sales history, & demand logs.</i>", style_table_cell)],
        [Paragraph("<code>get_kategori_df()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Query seluruh master kategori diurutkan A-Z.<br/><i>Fetches all master categories sorted alphabetically.</i>", style_table_cell)],
        [Paragraph("<code>get_barang_df()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Query JOIN master barang & kategori beserta margin profit (jual - beli).<br/><i>Fetches product list joined with categories & margin math.</i>", style_table_cell)],
        [Paragraph("<code>add_kategori()</code>", style_table_cell), Paragraph("nama, deskripsi", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Menambah kategori baru dengan penanganan UNIQUE constraint.<br/><i>Inserts new category with UNIQUE constraint handling.</i>", style_table_cell)],
        [Paragraph("<code>delete_kategori()</code>", style_table_cell), Paragraph("kat_id", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Hapus kategori dengan proteksi jika masih dipakai di barang.<br/><i>Deletes category with FK usage validation check.</i>", style_table_cell)],
        [Paragraph("<code>add_barang()</code>", style_table_cell), Paragraph("kode, nama, id_kat, h_beli, h_jual, stok, satuan", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Tambah barang baru dengan validasi kode barang unik.<br/><i>Inserts new product with unique SKU code check.</i>", style_table_cell)],
        [Paragraph("<code>update_barang()</code>", style_table_cell), Paragraph("id_brg, nama, id_kat, h_beli, h_jual, stok, satuan", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Memperbarui data barang & stok di database.<br/><i>Updates product info & stock levels in SQLite.</i>", style_table_cell)],
        [Paragraph("<code>delete_barang()</code>", style_table_cell), Paragraph("id_barang", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Menghapus data barang dari tabel barang.<br/><i>Deletes product entry from barang table.</i>", style_table_cell)],
        [Paragraph("<code>process_transaction()</code>", style_table_cell), Paragraph("items_cart, metode, catatan", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Eksekusi transaksi atomic ACID: insert header, insert detail, & update stok.<br/><i>Executes atomic transaction: insert header, details, & update stock.</i>", style_table_cell)],
        [Paragraph("<code>log_barang_dicari()</code>", style_table_cell), Paragraph("nama, id_kat, qty, status, catatan", style_table_cell), Paragraph("(bool, str)", style_table_cell), Paragraph("Menyimpan catatan barang yang dicari pelanggan ke log_permintaan.<br/><i>Logs customer requested missing items to log_permintaan.</i>", style_table_cell)],
        [Paragraph("<code>get_report_kategori_df()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Agregasi SQL SUM(qty), SUM(omset), & SUM(profit) per kategori.<br/><i>SQL aggregation of qty, revenue, & profit per category.</i>", style_table_cell)],
        [Paragraph("<code>get_report_item_df()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Agregasi SQL penjualan & profit margin per jenis item barang.<br/><i>SQL aggregation of sales & profit margins per item.</i>", style_table_cell)],
        [Paragraph("<code>get_report_barang_dicari_df()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Query ranking barang paling dicari (kehabisan stok) dikelompokkan A-Z.<br/><i>Queries ranking of most requested missing items.</i>", style_table_cell)],
        [Paragraph("<code>get_all_transaksi_df()</code>", style_table_cell), Paragraph("None", style_table_cell), Paragraph("pandas.DataFrame", style_table_cell), Paragraph("Query seluruh riwayat transaksi penjualan diurutkan waktu terbaru.<br/><i>Queries full sales transaction history sorted descending.</i>", style_table_cell)],
    ]
    t_dal_master = Table(dal_funcs_all, colWidths=[115, 85, 85, 202])
    t_dal_master.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_dal_master)

    story.append(PageBreak())

    # =========================================================================
    # CH 9: INSTALASI & MAINTENANCE
    # =========================================================================
    story.append(Paragraph("CH. 9: INSTALASI, DEPLOYMENT & MAINTENANCE BACKUP STRATEGY", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("<b>1. Prerequisites & Installation Commands:</b>", style_h3))
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
        "<b>🇮🇩 Bahasa Indonesia:</b> Karena SQLite bersifat *serverless* & *zero-configuration*, seluruh data bisnis tersimpan dalam file <code>warung_madura.db</code>. "
        "Lakukan copy/backup file ini ke Google Drive / Flashdisk secara berkala.<br/>"
        "<b>🇬🇧 English:</b> Because SQLite is *serverless* & *zero-configuration*, all business data resides in <code>warung_madura.db</code>. "
        "Regularly copy/backup this file to external cloud storage or USB drives.",
        style_id
    ))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=10, spaceAfter=12))
    story.append(Paragraph(
        "<b>MASTER DOCUMENTATION — WARUNG MADURA DIGITAL (COMPLETE EDITION)</b><br/>"
        "<i>Hasil Praktik Webinar Demo Python | Practical Result of Python Demo Webinar</i>",
        ParagraphStyle('FooterNotice', parent=styles['Normal'], alignment=1, fontSize=8, textColor=MUTED_TEXT)
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Dokumen PDF Master berhasil dibuat: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_master_pdf()
