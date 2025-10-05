import pandas as pd
import numpy as np

def hitung_topsis(matrix, bobot, tipe):
    # Normalisasi
    norm = matrix / np.sqrt((matrix ** 2).sum())
    # Bobotkan
    terbobot = norm * bobot

    # Tentukan solusi ideal
    ideal_plus, ideal_minus = [], []
    for j, t in enumerate(tipe):
        if t == "benefit":
            ideal_plus.append(terbobot.iloc[:, j].max())
            ideal_minus.append(terbobot.iloc[:, j].min())
        else:
            ideal_plus.append(terbobot.iloc[:, j].min())
            ideal_minus.append(terbobot.iloc[:, j].max())

    # Hitung jarak ke solusi ideal
    d_plus = np.sqrt(((terbobot - ideal_plus) ** 2).sum(axis=1))
    d_minus = np.sqrt(((terbobot - ideal_minus) ** 2).sum(axis=1))
    skor = d_minus / (d_plus + d_minus)

    hasil = pd.DataFrame({"Alternatif": matrix.index, "Skor": skor})
    return hasil
