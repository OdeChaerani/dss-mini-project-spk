def hitung_saw(matrix, bobot, tipe, alternatif, kriteria):
    """
    matrix     : list of list nilai alternatif × kriteria
    bobot      : list bobot kriteria
    tipe       : list tipe ("benefit" / "cost")
    alternatif : list nama alternatif
    kriteria   : list nama kriteria
    """

    # 1️⃣ Normalisasi bobot
    total_bobot = sum(bobot)
    if total_bobot == 0:
        raise ValueError("Total bobot = 0. Beri bobot yang valid.")
    w = [b / total_bobot for b in bobot]

    # 2️⃣ Normalisasi matriks
    n_alt = len(matrix)
    n_kri = len(matrix[0]) if matrix else 0
    R = [[0 for _ in range(n_kri)] for _ in range(n_alt)]

    for j in range(n_kri):
        kolom = [matrix[i][j] for i in range(n_alt)]
        if tipe[j] == "benefit":
            max_val = max(kolom)
            for i in range(n_alt):
                R[i][j] = matrix[i][j] / max_val if max_val != 0 else 0
        else:  # cost
            min_val = min(kolom)
            for i in range(n_alt):
                R[i][j] = (min_val / matrix[i][j]) if matrix[i][j] != 0 else 0

    # 3️⃣ Hitung skor akhir Vi = Σ(wj * rij)
    skor = []
    for i in range(n_alt):
        total = 0
        for j in range(n_kri):
            total += w[j] * R[i][j]
        skor.append(total)

    # 4️⃣ Gabungkan hasil ke list of dict (biar mudah ditampilkan)
    hasil = []
    for i in range(n_alt):
        hasil.append({
            "Alternatif": alternatif[i],
            "Skor": round(skor[i], 4)
        })

    return hasil, R, w
