import streamlit as st
import pandas as pd
import io

# Judul Website
st.title("Aplikasi Penggabung & Cek Duplikat Data 📊")
st.write("Upload 2 file Excel atau CSV, aplikasi akan menggabungkan dan mencari data duplikat berdasarkan kolom **no pesanan**.")

# 1. Tombol Upload File
file1 = st.file_uploader("Upload File Pertama", type=["csv", "xlsx"])
file2 = st.file_uploader("Upload File Kedua", type=["csv", "xlsx"])

kolom_patokan = 'no pesanan'

# Fungsi untuk mengubah dataframe menjadi file Excel di memori agar bisa didownload
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Jika kedua file sudah diupload
if file1 and file2:
    if st.button("Proses Data"):
        try:
            # Membaca file (deteksi apakah CSV atau Excel)
            if file1.name.endswith('.csv'):
                df1 = pd.read_csv(file1, sep=None, engine='python')
                df2 = pd.read_csv(file2, sep=None, engine='python')
            else:
                df1 = pd.read_excel(file1)
                df2 = pd.read_excel(file2)

            # Cek keberadaan kolom
            if kolom_patokan not in df1.columns or kolom_patokan not in df2.columns:
                st.error(f"❌ ERROR: Kolom '{kolom_patokan}' tidak ditemukan di salah satu file!")
            else:
                # Proses penggabungan dan duplikat
                df_all = pd.concat([df1, df2], ignore_index=True)
                
                df_gabungan = df_all.drop_duplicates(subset=[kolom_patokan], keep='first')
                df_duplikat = df_all[df_all.duplicated(subset=[kolom_patokan], keep=False)].drop_duplicates(subset=[kolom_patokan])

                st.success("✅ Berhasil diproses! Silakan download hasilnya di bawah:")

                # 2. Mengubah hasil menjadi file Excel (.xlsx)
                excel_gabungan = to_excel(df_gabungan)
                excel_duplikat = to_excel(df_duplikat)

                # 3. Tombol Download Hasil (Format Excel)
                st.download_button(
                    label="⬇️ Download Gabungan Bersih (.xlsx)", 
                    data=excel_gabungan, 
                    file_name="Gabungan_Bersih.xlsx", 
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.download_button(
                    label="⬇️ Download Hanya Duplikat (.xlsx)", 
                    data=excel_duplikat, 
                    file_name="Hanya_Duplikat.xlsx", 
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
