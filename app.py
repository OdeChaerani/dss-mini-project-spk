import streamlit as st
import pandas as pd
from methods.saw import hitung_saw
from methods.wp import hitung_wp
from methods.ahp import hitung_ahp
from methods.topsis import hitung_topsis

st.set_page_config(page_title="SPK App", page_icon="🧮", layout="wide")
st.title("🧠 Sistem Pendukung Keputusan (SPK)")
st.caption("Metode: SAW, WP, AHP, TOPSIS — tanpa library perhitungan")

# Jumlah kriteria dan alternatif
st.header("1️⃣ Tentukan Jumlah Data")
col1, col2 = st.columns(2)
with col1:
    n_kriteria = st.number_input("Jumlah Kriteria", min_value=1, step=1)
with col2:
    n_alternatif = st.number_input("Jumlah Alternatif", min_value=1, step=1)

# Jika jumlah sudah diisi
if n_kriteria > 0 and n_alternatif > 0:

    # Input nama & bobot kriteria
    st.header("2️⃣ Masukkan Data Kriteria")
    st.info("Isi nama, bobot, dan tipe (benefit/cost) untuk setiap kriteria")

    kriteria_data = []
    for i in range(n_kriteria):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            nama = st.text_input(f"Nama Kriteria {i+1}", key=f"k{i}")
        with col2:
            bobot = st.number_input(f"Bobot", min_value=0.0, key=f"b{i}")
        with col3:
            tipe = st.selectbox(f"Tipe", ["benefit", "cost"], key=f"t{i}")
        kriteria_data.append({"nama": nama, "bobot": bobot, "tipe": tipe})

    # Input nama alternatif
    st.header("3️⃣ Masukkan Nama Alternatif")
    alternatif_names = []
    for i in range(n_alternatif):
        nama = st.text_input(f"Nama Alternatif {i+1}", key=f"a{i}")
        alternatif_names.append(nama)

    # tabel nilai alternatif x kriteria
    if all(k["nama"] for k in kriteria_data) and all(alternatif_names):
        st.header("4️⃣ Isi Nilai Setiap Alternatif untuk Setiap Kriteria")

        columns = [k["nama"] for k in kriteria_data]
        empty_data = {col: [0 for _ in range(n_alternatif)] for col in columns}
        df_input = pd.DataFrame(empty_data, index=alternatif_names)

        edited_df = st.data_editor(df_input, use_container_width=True, num_rows="fixed")

        # Pilih metode dan hitung
        st.header("5️⃣ Pilih Metode dan Lihat Hasil")
        metode = st.selectbox("Pilih Metode SPK:", ["SAW", "WP", "AHP", "TOPSIS"])

        if st.button("Hitung Hasil"):
            df_nilai = edited_df
            bobot = [k["bobot"] for k in kriteria_data]
            tipe = [k["tipe"] for k in kriteria_data]

            if metode == "SAW":
                hasil = hitung_saw(df_nilai, bobot, tipe)
            elif metode == "WP":
                hasil = hitung_wp(df_nilai, bobot, tipe)
            elif metode == "AHP":
                hasil = hitung_ahp(df_nilai, bobot)
            elif metode == "TOPSIS":
                hasil = hitung_topsis(df_nilai, bobot, tipe)

            st.success(f"Hasil Perhitungan Menggunakan Metode {metode}")
            st.dataframe(hasil.sort_values("Skor", ascending=False), use_container_width=True)

            st.bar_chart(
                hasil.set_index("Alternatif")["Skor"],
                use_container_width=True,
                height=300,
            )
