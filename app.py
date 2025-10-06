import streamlit as st
from methods.saw import hitung_saw
from methods.wp import hitung_wp
from methods.ahp import hitung_ahp
from methods.topsis import hitung_topsis

st.set_page_config(page_title="SPK App", page_icon="🧮", layout="wide")
st.title("🧠 Sistem Pendukung Keputusan (SPK)")
st.caption("Metode: SAW, WP, AHP, TOPSIS — tanpa library perhitungan")

# --- STEP 1: Jumlah kriteria dan alternatif ---
st.header("1️⃣ Tentukan Jumlah Data")
col1, col2 = st.columns(2)
with col1:
    n_kriteria = st.number_input("Jumlah Kriteria", min_value=1, step=1)
with col2:
    n_alternatif = st.number_input("Jumlah Alternatif", min_value=1, step=1)

if n_kriteria > 0 and n_alternatif > 0:

    # --- STEP 2: Data kriteria ---
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

    # --- STEP 3: Data alternatif ---
    st.header("3️⃣ Masukkan Nama Alternatif")
    alternatif_names = []
    for i in range(n_alternatif):
        nama = st.text_input(f"Nama Alternatif {i+1}", key=f"a{i}")
        alternatif_names.append(nama)

    # --- STEP 4: Tabel nilai ---
    if all(k["nama"] for k in kriteria_data) and all(alternatif_names):
        st.header("4️⃣ Isi Nilai Setiap Alternatif untuk Setiap Kriteria")

        columns = [k["nama"] for k in kriteria_data]
        data_awal = {col: [0 for _ in range(n_alternatif)] for col in columns}

        # Gunakan data_editor untuk input tabel
        edited_df = st.data_editor(data_awal, use_container_width=True, num_rows="fixed")

        # Konversi ke list of lists
        matrix = []
        for i in range(n_alternatif):
            baris = []
            for col in columns:
                baris.append(float(edited_df[col][i]))
            matrix.append(baris)

        bobot = [k["bobot"] for k in kriteria_data]
        tipe = [k["tipe"] for k in kriteria_data]
        kriteria = [k["nama"] for k in kriteria_data]
        alternatif = alternatif_names

        # --- STEP 5: Pilih metode ---
        st.header("5️⃣ Pilih Metode dan Lihat Hasil")
        metode = st.selectbox("Pilih Metode SPK:", ["SAW", "WP", "AHP", "TOPSIS"])

        if st.button("Hitung Hasil"):
            if metode == "SAW":
                hasil, _, _ = hitung_saw(matrix, bobot, tipe, alternatif, kriteria)
            elif metode == "WP":
                hasil, _ = hitung_wp(matrix, bobot, tipe, alternatif, kriteria)
            elif metode == "AHP":
                hasil = hitung_ahp(matrix, bobot)
            elif metode == "TOPSIS":
                hasil = hitung_topsis(matrix, bobot, tipe)

            # Tampilkan hasil
            st.success(f"Hasil Perhitungan Menggunakan Metode {metode}")
            st.write("### 📊 Hasil Ranking:")

            # Sortir hasil berdasarkan skor tertinggi
            hasil_sorted = sorted(hasil, key=lambda x: x['Skor'] if 'Skor' in x else x['V'], reverse=True)

            for i, h in enumerate(hasil_sorted, 1):
                if 'Skor' in h:
                    st.write(f"**{i}. {h['Alternatif']}** — Skor: {h['Skor']}")
                elif 'V' in h:
                    st.write(f"**{i}. {h['Alternatif']}** — V: {h['V']}")
