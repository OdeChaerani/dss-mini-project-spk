import pandas as pd

def hitung_ahp(matrix, bobot):
    # Di sini AHP disederhanakan: langsung bobot * rata-rata kriteria
    skor = matrix.mul(bobot, axis=1).sum(axis=1)
    hasil = pd.DataFrame({"Alternatif": matrix.index, "Skor": skor})
    return hasil
