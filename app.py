import streamlit as st
import pandas as pd
import io

# Judul Website
st.title("Aplikasi Pembersih Data File 2 📊")
st.write("Aplikasi ini akan membersihkan **File 2** dari data yang sudah ada di **File 1** (berdasarkan kolom **no pesanan**).")

# 1. Tombol Upload File
file1 = st.file_uploader("Upload File 1 (Sebagai Data Acuan / Master)", type=["csv", "xlsx"])
file2 = st.file_uploader("Upload File 2 (Data yang ingin dibersihkan)", type=["csv", "xlsx"])

kolom_patokan = 'no pesanan'

# Fungsi untuk mengubah dataframe menjadi file Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Jika kedua file sudah diupload
if file1 and file2:
    if st.button("Proses Pembersihan"):
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

            # Cek keberadaan kolom
            if kolom_patokan not in df1.columns or kolom_patokan not in df2.columns:
                st.error(f"❌ ERROR: Kolom '{kolom_patokan}' tidak ditemukan di salah satu file!")
            else:
                # MENGAMBIL DAFTAR NO PESANAN DARI FILE 1
                daftar_pesanan_file1 = df1[kolom_patokan].tolist()

                # MEMFILTER FILE 2
                # Tanda '~' artinya "TIDAK". Jadi kita mengambil data di File 2 yang no pesanannya TIDAK ADA di File 1.
                df2_bersih = df2[~df2[kolom_patokan].isin(daftar_pesanan_file1)]
                
                # Mengambil data yang terhapus (Opsional, barangkali kamu mau mengecek data apa saja yang tadi dobel)
                df2_terhapus = df2[df2[kolom_patokan].isin(daftar_pesanan_file1)]

                st.success("✅ Berhasil! File 2 sudah dibersihkan dari data yang ada di File 1.")
                
                # Menampilkan info jumlah data
                st.info(f"📊 Info: Ada **{len(df2_terhapus)}** baris data di File 2 yang dihapus karena sudah ada di File 1.")

                # Mengubah hasil menjadi Excel
                excel_bersih = to_excel(df2_bersih)
                
                # Tombol Download File 2 yang sudah bersih
                st.download_button(
                    label="⬇️ Download File 2 (Sudah Bersih)", 
                    data=excel_bersih, 
                    file_name="File_2_Bersih.xlsx", 
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                # Tombol Download Data yang terhapus (Hanya muncul jika ada data yang dobel)
                if len(df2_terhapus) > 0:
                    excel_terhapus = to_excel(df2_terhapus)
                    st.download_button(
                        label="⬇️ Download Data yang Dihapus (Duplikat)", 
                        data=excel_terhapus, 
                        file_name="Data_Terhapus.xlsx", 
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            # --- FOOTER ---
st.markdown(
    """
    <div style="text-align: right; margin-top: 50px; color: gray; font-size: 14px;">
        <i>dibuat Tarno enginering</i>
    </div>
    """,
    unsafe_allow_html=True
)

