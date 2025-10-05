import pandas as pd

def hitung_saw(matrix, bobot, tipe):
    # Normalisasi matriks
    norm = matrix.copy()
    for j, t in enumerate(tipe):
        if t == "benefit":
            norm.iloc[:, j] = matrix.iloc[:, j] / matrix.iloc[:, j].max()
        else:
            norm.iloc[:, j] = matrix.iloc[:, j].min() / matrix.iloc[:, j]
    
    # Hitung skor akhir
    skor = norm.mul(bobot, axis=1).sum(axis=1)
    hasil = pd.DataFrame({"Alternatif": matrix.index, "Skor": skor})
    return hasil
