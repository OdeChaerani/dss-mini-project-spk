import pandas as pd
import numpy as np

def hitung_wp(matrix, bobot, tipe):
    w = [b / sum(bobot) for b in bobot]
    s = []
    for i in range(len(matrix)):
        nilai = 1
        for j, t in enumerate(tipe):
            if t == "benefit":
                nilai *= matrix.iloc[i, j] ** w[j]
            else:
                nilai *= (1 / matrix.iloc[i, j]) ** w[j]
        s.append(nilai)
    v = [si / sum(s) for si in s]
    hasil = pd.DataFrame({"Alternatif": matrix.index, "Skor": v})
    return hasil
