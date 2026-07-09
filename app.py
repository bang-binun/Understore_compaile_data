import streamlit as st
import pandas as pd

# Judul Website
st.title("Aplikasi Penggabung & Cek Duplikat Data 📊")
st.write("Upload 2 file Excel atau CSV, aplikasi akan menggabungkan dan mencari data duplikat berdasarkan kolom **no pesanan**.")

# 1. Tombol Upload File
file1 = st.file_uploader("Upload File Pertama", type=["csv", "xlsx"])
file2 = st.file_uploader("Upload File Kedua", type=["csv", "xlsx"])

kolom_patokan = 'no pesanan'

# Jika kedua file sudah diupload
if file1 and file2:
    if st.button("Proses Data"):
        try:
            # Membaca file (deteksi apakah CSV atau Excel)
            if file1.name.endswith('.csv'):
                df1 = pd.read_csv(file1, sep=None, engine='python') # Otomatis deteksi koma atau titik koma
                df2 = pd.read_csv(file2, sep=None, engine='python')
            else:
                df1 = pd.read_excel(file1)
                df2 = pd.read_excel(file2)

            # Cek keberadaan kolom
            if kolom_patokan not in df1.columns or kolom_patokan not in df2.columns:
                st.error(f"❌ ERROR: Kolom '{kolom_patokan}' tidak ditemukan di salah satu file!")
            else:
                # Proses penggabungan dan duplikat (Sama persis seperti kodenya sebelumnya)
                df_all = pd.concat([df1, df2], ignore_index=True)
                
                df_gabungan = df_all.drop_duplicates(subset=[kolom_patokan], keep='first')
                df_duplikat = df_all[df_all.duplicated(subset=[kolom_patokan], keep=False)].drop_duplicates(subset=[kolom_patokan])

                st.success("✅ Berhasil diproses! Silakan download hasilnya di bawah:")

                # 2. Tombol Download Hasil
                # Mengubah dataframe menjadi CSV agar bisa didownload
                csv_gabungan = df_gabungan.to_csv(index=False).encode('utf-8')
                csv_duplikat = df_duplikat.to_csv(index=False).encode('utf-8')

                st.download_button("⬇️ Download Gabungan Bersih", data=csv_gabungan, file_name="Gabungan_Bersih.csv", mime="text/csv")
                st.download_button("⬇️ Download Hanya Duplikat", data=csv_duplikat, file_name="Hanya_Duplikat.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
