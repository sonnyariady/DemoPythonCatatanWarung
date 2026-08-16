import streamlit as st
import pandas as pd
from datetime import datetime, date
import database as db

# Safe import for Plotly
HAS_PLOTLY = True
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    HAS_PLOTLY = False


# Config
st.set_page_config(
    page_title="Warung Madura Digital",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Main Background & Font */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header Styling */
    .header-banner {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 24px;
    }
    .header-banner h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .header-banner p {
        margin: 6px 0 0 0;
        opacity: 0.9;
        font-size: 1.05rem;
    }

    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 5px solid #2d6a4f;
    }
    .metric-card.warning {
        border-left-color: #e76f51;
    }
    .metric-card.info {
        border-left-color: #2a9d8f;
    }
    .metric-card.purple {
        border-left-color: #7209b7;
    }
    
    /* Custom Badges */
    .badge-habis {
        background-color: #ff4d4f;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .badge-menipis {
        background-color: #faad14;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .badge-aman {
        background-color: #52c41a;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Database
db.init_db()

# Session State for Shopping Cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

def format_rupiah(nominal):
    return f"Rp {nominal:,.0f}".replace(",", ".")

# Header UI
st.markdown("""
<div class="header-banner">
    <h1>🏪 Warung Madura Digital</h1>
    <p>Aplikasi Pencatatan Transaksi, Stok Barang, dan Laporan Kategori & Kehabisan Stok</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/isometric/100/grocery-store.png", width=70)
st.sidebar.title("Menu Utama")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    [
        "📊 Dashboard Utama",
        "🛒 Kasir (Penjualan)",
        "📦 Data Barang & Kategori",
        "🔍 Log Barang Dicari (Kehabisan)",
        "📈 Laporan & Analisis Data"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Warung Madura 24 Jam**\nCatat cepat transaksi, stok menipis, dan permintaan barang kehabisan.")


# ==========================================
# 📊 1. DASHBOARD UTAMA
# ==========================================
if menu == "📊 Dashboard Utama":
    st.subheader("📊 Ringkasan Usaha Hari Ini & Statistik Utama")

    df_transaksi = db.get_all_transaksi_df()
    df_barang = db.get_barang_df()
    df_log = db.get_log_permintaan_df()
    df_report_item = db.get_report_item_df()

    # Calculate summary metrics
    today_str = date.today().strftime('%Y-%m-%d')
    if not df_transaksi.empty:
        df_transaksi['tanggal_only'] = pd.to_datetime(df_transaksi['tanggal_transaksi']).dt.strftime('%Y-%m-%d')
        tx_today = df_transaksi[df_transaksi['tanggal_only'] == today_str]
        omset_today = tx_today['total_harga'].sum() if not tx_today.empty else 0
        total_tx_today = len(tx_today)
        omset_total = df_transaksi['total_harga'].sum()
    else:
        omset_today = 0
        total_tx_today = 0
        omset_total = 0

    stok_habis = df_barang[df_barang['stok'] == 0]
    stok_menipis = df_barang[(df_barang['stok'] > 0) & (df_barang['stok'] <= 5)]
    total_permintaan = df_log['jumlah_permintaan'].sum() if not df_log.empty else 0

    # Layout Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0; color:#6c757d; font-size:0.9rem;">Omset Penjualan Total</h4>
            <h2 style="margin:4px 0; color:#1b4332;">{format_rupiah(omset_total)}</h2>
            <p style="margin:0; font-size:0.85rem; color:#40916c;">Hari Ini: <b>{format_rupiah(omset_today)}</b> ({total_tx_today} TRX)</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card info">
            <h4 style="margin:0; color:#6c757d; font-size:0.9rem;">Total Jenis Produk</h4>
            <h2 style="margin:4px 0; color:#2a9d8f;">{len(df_barang)} Item</h2>
            <p style="margin:0; font-size:0.85rem; color:#2a9d8f;">Dari <b>{df_barang['nama_kategori'].nunique()}</b> Kategori</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card warning">
            <h4 style="margin:0; color:#6c757d; font-size:0.9rem;">Peringatan Stok Menipis/Habis</h4>
            <h2 style="margin:4px 0; color:#e76f51;">{len(stok_habis) + len(stok_menipis)} Item</h2>
            <p style="margin:0; font-size:0.85rem; color:#e76f51;">Habis: <b>{len(stok_habis)}</b> | Menipis: <b>{len(stok_menipis)}</b></p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card purple">
            <h4 style="margin:0; color:#6c757d; font-size:0.9rem;">Log Barang Dicari (Kehabisan)</h4>
            <h2 style="margin:4px 0; color:#7209b7;">{total_permintaan} Kali Ditanyakan</h2>
            <p style="margin:0; font-size:0.85rem; color:#7209b7;">Permintaan Pembeli Tak Terpenuhi</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Quick Charts
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🏆 5 Kategori Paling Banyak Dibeli")
        df_kat = db.get_report_kategori_df()
        if not df_kat.empty:
            if HAS_PLOTLY:
                fig_kat = px.pie(
                    df_kat.head(5),
                    values='total_qty_terjual',
                    names='nama_kategori',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_kat.update_traces(textinfo='percent+label')
                fig_kat.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
                st.plotly_chart(fig_kat, use_container_width=True)
            else:
                st.bar_chart(df_kat.head(5).set_index('nama_kategori')['total_qty_terjual'])
        else:
            st.info("Belum ada data penjualan.")

    with c2:
        st.markdown("### ⚡ 5 Barang Paling Banyak Dicari (Kehabisan Stok)")
        df_dicari = db.get_report_barang_dicari_df()
        if not df_dicari.empty:
            if HAS_PLOTLY:
                fig_dicari = px.bar(
                    df_dicari.head(5),
                    x='frekuensi_dicari',
                    y='nama_barang',
                    orientation='h',
                    color='status',
                    color_discrete_map={'Habis': '#ff4d4f', 'Belum Dijual': '#faad14'},
                    labels={'frekuensi_dicari': 'Jumlah Pembeli Menanyakan', 'nama_barang': 'Nama Barang'}
                )
                fig_dicari.update_layout(yaxis={'categoryorder': 'total ascending'}, margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig_dicari, use_container_width=True)
            else:
                st.bar_chart(df_dicari.head(5).set_index('nama_barang')['frekuensi_dicari'])
        else:
            st.info("Belum ada catatan barang dicari.")



# ==========================================
# 🛒 2. KASIR (INPUT TRANSAKSI)
# ==========================================
elif menu == "🛒 Kasir (Penjualan)":
    st.subheader("🛒 Input Transaksi Penjualan")

    df_barang = db.get_barang_df()
    
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("##### 🔍 Pilih & Tambahkan Barang ke Keranjang")
        
        # Filter & Search
        search_term = st.text_input("Cari nama atau kode barang:", placeholder="Ketik nama indomie, rokok, beras, dll...")
        kat_list = ["Semua Kategori"] + list(df_barang['nama_kategori'].unique())
        selected_kat = st.selectbox("Filter Kategori:", kat_list)

        df_filtered = df_barang.copy()
        if selected_kat != "Semua Kategori":
            df_filtered = df_filtered[df_filtered['nama_kategori'] == selected_kat]
        if search_term:
            df_filtered = df_filtered[
                df_filtered['nama_barang'].str.contains(search_term, case=False, na=False) |
                df_filtered['kode_barang'].str.contains(search_term, case=False, na=False)
            ]

        # Display Available Items Selection
        if not df_filtered.empty:
            # Option list format
            items_options = {}
            for _, row in df_filtered.iterrows():
                stok_status = f"(Stok: {row['stok']} {row['satuan']})"
                label = f"{row['nama_barang']} - {format_rupiah(row['harga_jual'])} {stok_status}"
                items_options[label] = row

            selected_label = st.selectbox("Pilih Produk:", list(items_options.keys()))
            selected_row = items_options[selected_label]

            c_qty, c_add = st.columns([2, 1])
            with c_qty:
                qty_input = st.number_input("Jumlah Qty:", min_value=1, max_value=max(1, int(selected_row['stok'])), value=1, step=1)
            with c_add:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("➕ Tambah ke Keranjang", use_container_width=True, type="primary"):
                    if selected_row['stok'] < qty_input:
                        st.error("Stok barang tidak mencukupi!")
                    else:
                        # Check if already in cart
                        exist = False
                        for item in st.session_state.cart:
                            if item['id'] == selected_row['id']:
                                if item['qty'] + qty_input > selected_row['stok']:
                                    st.error("Jumlah melampaui stok yang tersedia!")
                                else:
                                    item['qty'] += qty_input
                                    item['subtotal'] = item['qty'] * item['harga_jual']
                                    st.success(f"Jumlah {selected_row['nama_barang']} diperbarui!")
                                exist = True
                                break
                        if not exist:
                            st.session_state.cart.append({
                                'id': selected_row['id'],
                                'nama_barang': selected_row['nama_barang'],
                                'kategori': selected_row['nama_kategori'],
                                'harga_jual': selected_row['harga_jual'],
                                'harga_beli': selected_row['harga_beli'],
                                'qty': qty_input,
                                'subtotal': qty_input * selected_row['harga_jual'],
                                'satuan': selected_row['satuan']
                            })
                            st.success(f"{selected_row['nama_barang']} dimasukkan ke keranjang!")
                        st.rerun()

            # Stock Alert & Fast Out-of-Stock Logger
            if selected_row['stok'] <= 3:
                st.warning(f"⚠️ Stok {selected_row['nama_barang']} menipis/habis ({selected_row['stok']} {selected_row['satuan']})!")
                
        else:
            st.warning("Barang tidak ditemukan.")
        
        # Quick Out of Stock Demand Button
        st.markdown("---")
        with st.expander("⚡ Pembeli mencari barang yang Stoknya HABIS / BELUM DIJUAL?"):
            st.info("Catat langsung permintaan pembeli agar masuk ke **Laporan Barang Paling Dicari**.")
            with st.form("quick_log_form"):
                log_nama = st.text_input("Nama Barang yang Dicari:", value=search_term if search_term else "")
                df_kategori = db.get_kategori_df()
                kat_opts = dict(zip(df_kategori['nama_kategori'], df_kategori['id']))
                log_kat_nama = st.selectbox("Kategori Barang:", list(kat_opts.keys()))
                log_qty = st.number_input("Jumlah Pencarian/Permintaan:", min_value=1, value=1)
                log_status = st.radio("Status:", ["Habis", "Belum Dijual"], horizontal=True)
                log_catatan = st.text_input("Catatan Tambahan (opsional):", placeholder="Misal: minta restok merk X")
                
                btn_log_submit = st.form_submit_button("📝 Simpan Catatan Barang Dicari")
                if btn_log_submit:
                    if log_nama.strip():
                        db.log_barang_dicari(log_nama.strip(), kat_opts[log_kat_nama], log_qty, log_status, log_catatan)
                        st.success(f"Catatan '{log_nama}' berhasil disimpan!")
                    else:
                        st.error("Nama barang harus diisi!")

    with col_right:
        st.markdown("##### 🛍️ Rincian Keranjang Belanja")
        if st.session_state.cart:
            cart_df = pd.DataFrame(st.session_state.cart)
            
            # Table display
            display_cart = cart_df[['nama_barang', 'qty', 'harga_jual', 'subtotal']].copy()
            display_cart['harga_jual'] = display_cart['harga_jual'].apply(format_rupiah)
            display_cart['subtotal'] = display_cart['subtotal'].apply(format_rupiah)
            display_cart.columns = ['Produk', 'Qty', 'Harga', 'Subtotal']
            
            st.dataframe(display_cart, use_container_width=True, hide_index=True)

            total_bayar = sum(item['subtotal'] for item in st.session_state.cart)
            st.markdown(f"### Total: <span style='color:#1b4332;'>{format_rupiah(total_bayar)}</span>", unsafe_allow_html=True)

            c_clear, c_pay = st.columns([1, 1])
            with c_clear:
                if st.button("🗑️ Kosongkan Keranjang", use_container_width=True):
                    st.session_state.cart = []
                    st.rerun()

            st.markdown("---")
            metode = st.selectbox("Metode Pembayaran:", ["Tunai", "QRIS", "Transfer Bank"])
            nominal_uang = st.number_input("Uang Diterima (Rp):", min_value=0.0, value=float(total_bayar), step=5000.0)
            kembalian = nominal_uang - total_bayar

            if kembalian >= 0:
                st.success(f"💰 Kembalian: **{format_rupiah(kembalian)}**")
            else:
                st.error(f"⚠️ Uang pembayaran kurang {format_rupiah(abs(kembalian))}")

            catatan_tx = st.text_input("Catatan Pembayaran (Opsional):")

            if st.button("✅ Selesaikan & Simpan Transaksi", type="primary", use_container_width=True):
                if nominal_uang < total_bayar:
                    st.error("Uang yang diterima kurang!")
                else:
                    success, msg = db.process_transaction(st.session_state.cart, metode, catatan_tx)
                    if success:
                        st.balloons()
                        st.success(msg)
                        st.session_state.cart = []
                    else:
                        st.error(msg)
        else:
            st.info("Keranjang belanja masih kosong. Silakan pilih produk di sebelah kiri.")


# ==========================================
# 📦 3. DATA BARANG & KATEGORI
# ==========================================
elif menu == "📦 Data Barang & Kategori":
    st.subheader("📦 Kelola Inventaris Produk & Kategori")

    tab_barang, tab_kategori = st.tabs(["🏷️ Daftar & Olah Barang", "📂 Manajemen Kategori"])

    with tab_barang:
        st.markdown("### Daftar Barang Warung")
        df_barang = db.get_barang_df()
        
        # Display data
        df_display = df_barang.copy()
        df_display['harga_beli_fmt'] = df_display['harga_beli'].apply(format_rupiah)
        df_display['harga_jual_fmt'] = df_display['harga_jual'].apply(format_rupiah)
        df_display['margin_fmt'] = df_display['margin'].apply(format_rupiah)

        def badge_stok(val):
            if val == 0:
                return '🔴 HABIS'
            elif val <= 5:
                return '🟡 MENIPIS'
            return '🟢 AMAN'

        df_display['Status Stok'] = df_display['stok'].apply(badge_stok)

        cols_show = ['kode_barang', 'nama_barang', 'nama_kategori', 'harga_beli_fmt', 'harga_jual_fmt', 'margin_fmt', 'stok', 'satuan', 'Status Stok']
        df_display_clean = df_display[cols_show].rename(columns={
            'kode_barang': 'Kode',
            'nama_barang': 'Nama Barang',
            'nama_kategori': 'Kategori',
            'harga_beli_fmt': 'Harga Beli',
            'harga_jual_fmt': 'Harga Jual',
            'margin_fmt': 'Margin/Untung',
            'stok': 'Stok',
            'satuan': 'Satuan'
        })
        st.dataframe(df_display_clean, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### ➕ / ✏️ Tambah atau Edit Barang")

        df_kategori = db.get_kategori_df()
        kat_map = dict(zip(df_kategori['nama_kategori'], df_kategori['id']))

        action = st.radio("Aksi:", ["Tambah Barang Baru", "Edit Barang", "Hapus Barang"], horizontal=True)

        if action == "Tambah Barang Baru":
            with st.form("form_add_barang"):
                c1, c2 = st.columns(2)
                with c1:
                    kode = st.text_input("Kode Barang (Unik):", value=f"BRG-0{len(df_barang)+1:02d}")
                    nama = st.text_input("Nama Barang:")
                    kat_nama = st.selectbox("Kategori:", list(kat_map.keys()))
                    satuan = st.text_input("Satuan:", value="pcs", help="pcs, kg, bungkus, botol, galon, dll.")
                with c2:
                    h_beli = st.number_input("Harga Beli (Modal):", min_value=0.0, step=500.0)
                    h_jual = st.number_input("Harga Jual:", min_value=0.0, step=500.0)
                    stok_init = st.number_input("Jumlah Stok Awal:", min_value=0, step=1, value=10)

                submitted = st.form_submit_button("💾 Simpan Barang Baru", type="primary")
                if submitted:
                    if nama.strip():
                        success, msg = db.add_barang(kode, nama, kat_map[kat_nama], h_beli, h_jual, stok_init, satuan)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Nama barang tidak boleh kosong!")

        elif action == "Edit Barang":
            selected_edit = st.selectbox("Pilih Barang yang Akan Diubah:", df_barang['nama_barang'].tolist())
            row_edit = df_barang[df_barang['nama_barang'] == selected_edit].iloc[0]

            with st.form("form_edit_barang"):
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Kode Barang:", value=row_edit['kode_barang'], disabled=True)
                    nama_ed = st.text_input("Nama Barang:", value=row_edit['nama_barang'])
                    kat_idx = list(kat_map.keys()).index(row_edit['nama_kategori']) if row_edit['nama_kategori'] in kat_map else 0
                    kat_nama_ed = st.selectbox("Kategori:", list(kat_map.keys()), index=kat_idx)
                    satuan_ed = st.text_input("Satuan:", value=row_edit['satuan'])
                with c2:
                    h_beli_ed = st.number_input("Harga Beli:", min_value=0.0, value=float(row_edit['harga_beli']), step=500.0)
                    h_jual_ed = st.number_input("Harga Jual:", min_value=0.0, value=float(row_edit['harga_jual']), step=500.0)
                    stok_ed = st.number_input("Stok Saat Ini:", min_value=0, value=int(row_edit['stok']), step=1)

                submitted_ed = st.form_submit_button("✏️ Perbarui Barang", type="primary")
                if submitted_ed:
                    success, msg = db.update_barang(row_edit['id'], nama_ed, kat_map[kat_nama_ed], h_beli_ed, h_jual_ed, stok_ed, satuan_ed)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        elif action == "Hapus Barang":
            selected_del = st.selectbox("Pilih Barang yang Akan Dihapus:", df_barang['nama_barang'].tolist())
            row_del = df_barang[df_barang['nama_barang'] == selected_del].iloc[0]
            st.warning(f"Apakah Anda yakin ingin menghapus '{row_del['nama_barang']}'?")
            if st.button("🗑️ Konfirmasi Hapus Barang", type="primary"):
                success, msg = db.delete_barang(row_del['id'])
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with tab_kategori:
        st.markdown("### Daftar Kategori Barang")
        df_kat = db.get_kategori_df()
        st.dataframe(df_kat, use_container_width=True, hide_index=True)

        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.markdown("#### ➕ Tambah Kategori Baru")
            with st.form("form_add_kat"):
                nama_kat_new = st.text_input("Nama Kategori Baru:")
                desc_kat_new = st.text_input("Deskripsi Kategori:")
                if st.form_submit_button("Simpan Kategori"):
                    if nama_kat_new.strip():
                        success, msg = db.add_kategori(nama_kat_new.strip(), desc_kat_new.strip())
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Nama kategori harus diisi!")
        with col_k2:
            st.markdown("#### 🗑️ Hapus Kategori")
            kat_to_del = st.selectbox("Pilih Kategori:", df_kat['nama_kategori'].tolist())
            kat_id_del = df_kat[df_kat['nama_kategori'] == kat_to_del].iloc[0]['id']
            if st.button("Hapus Kategori Ditunjuk"):
                success, msg = db.delete_kategori(kat_id_del)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


# ==========================================
# 🔍 4. LOG BARANG DICARI (KEHABISAN STOK)
# ==========================================
elif menu == "🔍 Log Barang Dicari (Kehabisan)":
    st.subheader("🔍 Catatan Barang yang Sering Dicari Pembeli (Kehabisan / Tidak Ada)")
    st.info("""
    💡 **Fitur Istimewa Warung Madura**: Catatan ini merekam barang apa saja yang ingin dibeli pelanggan namun **stoknya kehabisan** atau **belum dijual di warung**. 
    Gunakan laporan ini untuk referensi belanja grosir / kulakan berikutnya!
    """)

    df_log = db.get_log_permintaan_df()

    # Form to input search log
    with st.expander("➕ Form Input Catatan Barang Kehabisan / Dicari Pembeli", expanded=True):
        df_kategori = db.get_kategori_df()
        kat_map = dict(zip(df_kategori['nama_kategori'], df_kategori['id']))

        with st.form("form_log_permintaan"):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                log_nama_brg = st.text_input("Nama Barang:", placeholder="Contoh: Gas 3kg, Es Batu, Rokok X")
                log_kat = st.selectbox("Kategori Barang:", list(kat_map.keys()))
            with c2:
                log_status_opt = st.selectbox("Status Barang:", ["Habis", "Belum Dijual"])
                log_catatan_opt = st.text_input("Catatan Pembeli:", placeholder="Misal: 3 orang tanya berturut-turut")
            with c3:
                log_qty_opt = st.number_input("Jumlah Pencarian:", min_value=1, value=1)
                st.markdown("<br>", unsafe_allow_html=True)

            sub_log = st.form_submit_button("📝 Catat Permintaan Pembeli", type="primary", use_container_width=True)
            if sub_log:
                if log_nama_brg.strip():
                    db.log_barang_dicari(log_nama_brg.strip(), kat_map[log_kat], log_qty_opt, log_status_opt, log_catatan_opt)
                    st.success(f"Permintaan untuk '{log_nama_brg}' berhasil dicatat!")
                    st.rerun()
                else:
                    st.error("Nama barang wajib diisi!")

    st.markdown("---")
    st.markdown("### 📋 Riwayat Log Pencarian Barang")

    if not df_log.empty:
        # Ranking analysis
        df_rank = db.get_report_barang_dicari_df()
        
        st.markdown("#### 🥇 Ranking Barang Paling Dicari & Kehabisan")
        st.dataframe(
            df_rank.rename(columns={
                'nama_barang': 'Nama Barang',
                'nama_kategori': 'Kategori',
                'status': 'Status Stok',
                'frekuensi_dicari': 'Total Kuantitas Dicari',
                'jumlah_kejadian': 'Frekuensi Ditanyakan (Kali)',
                'daftar_catatan': 'Catatan Pembeli'
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")
        st.markdown("#### 📜 Rincian Seluruh Transaksi Pencarian")
        st.dataframe(
            df_log[['tanggal', 'nama_barang', 'nama_kategori', 'jumlah_permintaan', 'status', 'catatan']].rename(columns={
                'tanggal': 'Tanggal & Waktu',
                'nama_barang': 'Nama Barang',
                'nama_kategori': 'Kategori',
                'jumlah_permintaan': 'Qty Dicari',
                'status': 'Status',
                'catatan': 'Catatan'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Belum ada catatan barang dicari.")


# ==========================================
# 📈 5. LAPORAN & ANALISIS DATA
# ==========================================
elif menu == "📈 Laporan & Analisis Data":
    st.subheader("📈 Laporan Analisis Penjualan & Perencanaan Stok")

    tab_kat, tab_dicari, tab_item, tab_history = st.tabs([
        "📊 Laporan Per Kategori Terbanyak Dibeli",
        "⚡ Laporan Barang Paling Dicari (Kehabisan)",
        "🏷️ Laporan Detail Per Jenis Item Barang",
        "📜 Riwayat Penjualan & Ekspor Data"
    ])

    # 1. LAPORAN PER KATEGORI
    with tab_kat:
        st.markdown("### 📦 Analisis Penjualan Berdasarkan Kategori Barang")
        df_kat_rep = db.get_report_kategori_df()

        if not df_kat_rep.empty:
            col_l, col_r = st.columns([1, 1])

            with col_l:
                st.markdown("#### 📊 Grafik Jumlah Item Terjual Per Kategori")
                fig_bar_kat = px.bar(
                    df_kat_rep,
                    x='nama_kategori',
                    y='total_qty_terjual',
                    text='total_qty_terjual',
                    color='nama_kategori',
                    labels={'nama_kategori': 'Kategori', 'total_qty_terjual': 'Jumlah Terjual (Pcs/Unit)'},
                    title="Kuantitas Terjual Per Kategori"
                )
                fig_bar_kat.update_traces(textposition='outside')
                st.plotly_chart(fig_bar_kat, use_container_width=True)

            with col_r:
                st.markdown("#### 💰 Grafik Kontribusi Omset Nominal Per Kategori")
                fig_pie_omset = px.pie(
                    df_kat_rep,
                    values='total_omset',
                    names='nama_kategori',
                    title="Proporsi Omset Per Kategori",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_pie_omset, use_container_width=True)

            st.markdown("#### 📋 Tabel Ringkasan Kategori Terlaris")
            df_kat_disp = df_kat_rep.copy()
            df_kat_disp['total_omset'] = df_kat_disp['total_omset'].apply(format_rupiah)
            df_kat_disp['total_profit'] = df_kat_disp['total_profit'].apply(format_rupiah)
            
            st.dataframe(
                df_kat_disp.rename(columns={
                    'nama_kategori': 'Nama Kategori',
                    'total_qty_terjual': 'Total Terjual (Unit)',
                    'total_omset': 'Total Omset (Rp)',
                    'total_profit': 'Estimasi Keuntungan (Rp)'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Belum ada data transaksi penjualan.")

    # 2. LAPORAN BARANG PALING DICARI (OUT OF STOCK)
    with tab_dicari:
        st.markdown("### ⚡ Analisis Barang yang Paling Dicari Pembeli (Kehabisan Stok)")
        st.caption("Menyoroti kategori dan barang mana yang paling berpotensi jika direstok / ditambahkan ke daftar jual warung.")

        df_dicari_rep = db.get_report_barang_dicari_df()

        if not df_dicari_rep.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 📊 Top Barang Kehabisan Stok / Paling Dicari")
                fig_dicari_bar = px.bar(
                    df_dicari_rep,
                    x='frekuensi_dicari',
                    y='nama_barang',
                    color='nama_kategori',
                    orientation='h',
                    labels={'frekuensi_dicari': 'Total Kuantitas Ditanyakan Pembeli', 'nama_barang': 'Barang'},
                    title="Perbandingan Tingkat Pencarian Pembeli"
                )
                fig_dicari_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_dicari_bar, use_container_width=True)

            with c2:
                st.markdown("#### 📂 Kategori Barang yang Paling Serius Kehabisan Stok")
                df_kat_dicari = df_dicari_rep.groupby('nama_kategori')['frekuensi_dicari'].sum().reset_index()
                fig_kat_dicari = px.pie(
                    df_kat_dicari,
                    values='frekuensi_dicari',
                    names='nama_kategori',
                    title="Distribusi Pencarian Per Kategori",
                    hole=0.3
                )
                st.plotly_chart(fig_kat_dicari, use_container_width=True)

            st.markdown("#### 📋 Tabel Peringkat Kebutuhan Restok Barang")
            st.dataframe(
                df_dicari_rep.rename(columns={
                    'nama_barang': 'Nama Barang',
                    'nama_kategori': 'Kategori',
                    'status': 'Status Barang',
                    'frekuensi_dicari': 'Jumlah Permintaan Pembeli',
                    'jumlah_kejadian': 'Frekuensi Ditanyakan',
                    'daftar_catatan': 'Catatan / Alasan'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Belum ada log barang dicari.")

    # 3. LAPORAN DETAIL PER JENIS ITEM BARANG
    with tab_item:
        st.markdown("### 🏷️ Analisis Penjualan & Keuntungan Per Jenis Item Barang")
        df_item_rep = db.get_report_item_df()

        if not df_item_rep.empty:
            # Filters
            kats_avail = ["Semua Kategori"] + list(df_item_rep['nama_kategori'].unique())
            sel_kat_item = st.selectbox("Filter berdasarkan Kategori Barang:", kats_avail, key="filter_kat_item")
            
            df_filtered_item = df_item_rep.copy()
            if sel_kat_item != "Semua Kategori":
                df_filtered_item = df_filtered_item[df_filtered_item['nama_kategori'] == sel_kat_item]

            col_i1, col_i2 = st.columns(2)
            with col_i1:
                st.markdown("#### 🏆 Top 10 Produk Terlaris (Kuantitas)")
                top_qty = df_filtered_item.sort_values(by='total_qty_terjual', ascending=False).head(10)
                fig_top_qty = px.bar(
                    top_qty,
                    x='total_qty_terjual',
                    y='nama_barang',
                    orientation='h',
                    color='total_qty_terjual',
                    color_continuous_scale='Greens',
                    labels={'total_qty_terjual': 'Terjual (Unit)', 'nama_barang': 'Nama Produk'}
                )
                fig_top_qty.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_top_qty, use_container_width=True)

            with col_i2:
                st.markdown("#### 💵 Top 10 Produk Penyumbang Profit Terbesar")
                top_profit = df_filtered_item.sort_values(by='total_profit', ascending=False).head(10)
                fig_top_profit = px.bar(
                    top_profit,
                    x='total_profit',
                    y='nama_barang',
                    orientation='h',
                    color='total_profit',
                    color_continuous_scale='Viridis',
                    labels={'total_profit': 'Total Keuntungan (Rp)', 'nama_barang': 'Nama Produk'}
                )
                fig_top_profit.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_top_profit, use_container_width=True)

            st.markdown("#### 📋 Rincian Margin Profit & Penjualan Seluruh Item")
            df_disp_item = df_filtered_item.copy()
            df_disp_item['harga_jual'] = df_disp_item['harga_jual'].apply(format_rupiah)
            df_disp_item['harga_beli'] = df_disp_item['harga_beli'].apply(format_rupiah)
            df_disp_item['profit_per_unit'] = df_disp_item['profit_per_unit'].apply(format_rupiah)
            df_disp_item['total_omset'] = df_disp_item['total_omset'].apply(format_rupiah)
            df_disp_item['total_profit'] = df_disp_item['total_profit'].apply(format_rupiah)

            st.dataframe(
                df_disp_item.rename(columns={
                    'nama_barang': 'Nama Barang',
                    'nama_kategori': 'Kategori',
                    'harga_jual': 'Harga Jual',
                    'harga_beli': 'Harga Modal',
                    'profit_per_unit': 'Margin/Unit',
                    'total_qty_terjual': 'Qty Terjual',
                    'total_omset': 'Total Omset',
                    'total_profit': 'Total Profit'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Belum ada data transaksi item.")

    # 4. RIWAYAT TRANSAKSI & EXPORT
    with tab_history:
        st.markdown("### 📜 Riwayat Transaksi & Unduh Laporan")
        df_tx_all = db.get_all_transaksi_df()

        if not df_tx_all.empty:
            df_tx_disp = df_tx_all.copy()
            df_tx_disp['total_harga_fmt'] = df_tx_disp['total_harga'].apply(format_rupiah)

            st.dataframe(
                df_tx_disp[['kode_transaksi', 'tanggal_transaksi', 'total_harga_fmt', 'metode_pembayaran', 'jumlah_item_berbeda', 'total_qty', 'catatan']].rename(columns={
                    'kode_transaksi': 'Kode Transaksi',
                    'tanggal_transaksi': 'Tanggal & Waktu',
                    'total_harga_fmt': 'Total Pembayaran',
                    'metode_pembayaran': 'Metode Pembayaran',
                    'jumlah_item_berbeda': 'Variasi Item',
                    'total_qty': 'Total Unit Barang',
                    'catatan': 'Catatan'
                }),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")
            st.markdown("#### 📥 Unduh Laporan (CSV)")
            c_dl1, c_dl2 = st.columns(2)
            with c_dl1:
                csv_tx = df_tx_all.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Unduh Data Transaksi (CSV)",
                    data=csv_tx,
                    file_name=f"laporan_transaksi_warung_madura_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with c_dl2:
                df_item_all = db.get_report_item_df()
                csv_item = df_item_all.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Unduh Laporan Per Jenis Barang (CSV)",
                    data=csv_item,
                    file_name=f"laporan_item_warung_madura_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("Belum ada riwayat transaksi.")
