import streamlit as st
import pandas as pd
from methods.saw import hitung_saw
from methods.wp import hitung_wp
from methods.ahp import hitung_ahp
from methods.topsis import hitung_topsis

st.title("🧠 Sistem Pendukung Keputusan (SPK) - MCDM Methods")
st.write("Metode yang tersedia: SAW, WP, AHP, dan TOPSIS")

# --- Input jumlah kriteria dan alternatif ---
n_kriteria = st.number_input("Jumlah Kriteria:", min_value=1, step=1)
n_alternatif = st.number_input("Jumlah Alternatif:", min_value=1, step=1)

if n_kriteria and n_alternatif:
    # --- Input data kriteria ---
    st.subheader("Data Kriteria")
    kriteria = []
    for i in range(n_kriteria):
        nama = st.text_input(f"Nama Kriteria {i+1}", key=f"k{i}")
        bobot = st.number_input(f"Bobot Kriteria {i+1}", min_value=0.0, key=f"b{i}")
        tipe = st.selectbox(f"Tipe Kriteria {i+1}", ["benefit", "cost"], key=f"t{i}")
        kriteria.append({"nama": nama, "bobot": bobot, "tipe": tipe})

    # --- Input nilai alternatif ---
    st.subheader("Data Alternatif")
    alternatif_data = []
    alternatif_names = []
    for i in range(n_alternatif):
        nama = st.text_input(f"Nama Alternatif {i+1}", key=f"a{i}")
        alternatif_names.append(nama)
        nilai = []
        for j in range(n_kriteria):
            v = st.number_input(f"Nilai {nama} untuk {kriteria[j]['nama']}", key=f"v{i}{j}")
            nilai.append(v)
        alternatif_data.append(nilai)

    # --- Pilih metode ---
    metode = st.selectbox("Pilih Metode SPK:", ["SAW", "WP", "AHP", "TOPSIS"])

    if st.button("Hitung"):
        df_nilai = pd.DataFrame(alternatif_data, columns=[k["nama"] for k in kriteria], index=alternatif_names)
        bobot = [k["bobot"] for k in kriteria]
        tipe = [k["tipe"] for k in kriteria]

        if metode == "SAW":
            hasil = hitung_saw(df_nilai, bobot, tipe)
        elif metode == "WP":
            hasil = hitung_wp(df_nilai, bobot, tipe)
        elif metode == "AHP":
            hasil = hitung_ahp(df_nilai, bobot)
        elif metode == "TOPSIS":
            hasil = hitung_topsis(df_nilai, bobot, tipe)

        st.subheader("📊 Hasil Perhitungan")
        st.dataframe(hasil.sort_values("Skor", ascending=False))
