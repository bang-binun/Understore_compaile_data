import streamlit as st
import pandas as pd
import io

# --- KONFIGURASI HALAMAN (Wajib di baris paling atas) ---
st.set_page_config(
    page_title="Pembersih Data | Bang Binun",
    page_icon="🚀",
    layout="wide"
)

# --- CSS KUSTOM UNTUK BACKGROUND DAN TAMPILAN ---
st.markdown("""
    <style>
    /* 1. MENGUBAH BACKGROUND MENJADI WARNA GRADASI SEGAR */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
    }
    
    /* 2. Membuat header atas transparan agar menyatu dengan background */
    [data-testid="stHeader"] {
        background-color: transparent;
    }

    /* 3. Membuat tombol proses terlihat keren */
    .stButton>button {
        background-color: #2e66f5;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease 0s;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #1b49bf;
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    /* 4. Teks Footer Bang Binun */
    .footer {
        text-align: right;
        margin-top: 50px;
        color: #4a4a4a;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BAGIAN HEADER ---
st.title("🚀 Aplikasi Pembersih Data")
st.markdown("Selamat datang! Sistem ini akan membersihkan **File 2 (SHOPEE K2)** dari data yang sudah ada di **File 1 (SHOPEE K1)** secara otomatis berdasarkan kolom **No. Pesanan
**.")

st.divider() # Garis pembatas

# --- BAGIAN UPLOAD FILE (TATA LETAK SEBELAHAN) ---
col1, col2 = st.columns(2)

with col1:
    st.info("📁 **LANGKAH 1: Data Master**")
    file1 = st.file_uploader("Upload File 1 (Sebagai Acuan)", type=["csv", "xlsx"])

with col2:
    st.warning("📄 **LANGKAH 2: Data Target**")
    file2 = st.file_uploader("Upload File 2 (Yang ingin dibersihkan)", type=["csv", "xlsx"])

kolom_patokan = 'No. Pesanan'

# Fungsi convert ke Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# --- BAGIAN PROSES ---
if file1 and file2:
    st.divider()
    
    # Membuat 3 kolom kosong agar tombol ada persis di tengah
    kolom_kiri, kolom_tengah, kolom_kanan = st.columns([1, 2, 1])
    
    with kolom_tengah:
        tombol_proses = st.button("⚙️ MULAI BERSIHKAN DATA", use_container_width=True)

    if tombol_proses:
        # Menambahkan animasi loading
        with st.spinner('Memindai dan membersihkan data... Mohon tunggu sebentar ⏳'):
            try:
                # Membaca File 1
                if file1.name.endswith('.csv'):
                    df1 = pd.read_csv(file1, sep=None, engine='python')
                else:
                    df1 = pd.read_excel(file1)
                
                # Membaca File 2
                if file2.name.endswith('.csv'):
                    df2 = pd.read_csv(file2, sep=None, engine='python')
                else:
                    df2 = pd.read_excel(file2)

                if kolom_patokan not in df1.columns or kolom_patokan not in df2.columns:
                    st.error(f"❌ ERROR: Kolom '{kolom_patokan}' tidak ditemukan di salah satu file! Pastikan huruf besar/kecilnya sama.")
                else:
                    daftar_pesanan_file1 = df1[kolom_patokan].tolist()
                    
                    df2_bersih = df2[~df2[kolom_patokan].isin(daftar_pesanan_file1)]
                    df2_terhapus = df2[df2[kolom_patokan].isin(daftar_pesanan_file1)]

                    st.success("✅ **Selesai!** File 2 berhasil dibersihkan dari data yang ada di File 1.")
                    st.info(f"📊 **Laporan Cepat:** Ada **{len(df2_terhapus)}** baris data yang dihapus dari File 2.")

                    excel_bersih = to_excel(df2_bersih)
                    
                    # Layout untuk hasil download
                    st.markdown("### 📥 Unduh Hasil")
                    col_down1, col_down2 = st.columns(2)
                    
                    with col_down1:
                        st.download_button(
                            label="⬇️ Download File 2 (Sudah Bersih)", 
                            data=excel_bersih, 
                            file_name="File_2_Bersih.xlsx", 
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )

                    with col_down2:
                        if len(df2_terhapus) > 0:
                            excel_terhapus = to_excel(df2_terhapus)
                            st.download_button(
                                label="⬇️ Download Data yang Dihapus", 
                                data=excel_terhapus, 
                                file_name="Data_Terhapus.xlsx", 
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses: {e}")

# --- FOOTER TARNO ENGINERING ---
st.markdown('<div class="footer"><i>dibuat bang Binun</i></div>', unsafe_allow_html=True)
