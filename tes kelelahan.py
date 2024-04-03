import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fungsi interpretasi untuk mengubah nilai fuzzy menjadi label kategori
def interpretasi_tingkat_kelelahan(nilai):
    if nilai <= 40:
        return 'Rendah'
    elif nilai <= 70:
        return 'Sedang'
    else:
        return 'Tinggi'

# Membaca data dari CSV
data = pd.read_excel(r"C:\python\datnak.xlsx")

# Definisikan variabel input
minum = ctrl.Antecedent(np.arange(700, 1601, 100), 'minum')
lari = ctrl.Antecedent(np.arange(500, 1201, 100), 'lari')
tidur = ctrl.Antecedent(np.arange(6, 10.1, 1), 'tidur')

# Definisikan variabel output
tingkat_kelelahan = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_kelelahan')

# Fungsi keanggotaan untuk variabel input dan output
minum.automf(3)
lari.automf(3)
tidur.automf(3)

tingkat_kelelahan['rendah'] = fuzz.trimf(tingkat_kelelahan.universe, [0, 0, 40])
tingkat_kelelahan['sedang'] = fuzz.trimf(tingkat_kelelahan.universe, [30, 50, 70])
tingkat_kelelahan['tinggi'] = fuzz.trimf(tingkat_kelelahan.universe, [60, 80, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(minum['poor'] | lari['poor'] | tidur['poor'], tingkat_kelelahan['rendah'])
rule2 = ctrl.Rule(minum['average'] | lari['average'] | tidur['average'], tingkat_kelelahan['sedang'])
rule3 = ctrl.Rule(minum['good'] | lari['good'] | tidur['good'], tingkat_kelelahan['tinggi'])

# Sistem kontrol fuzzy
tingkat_kelelahan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tingkat_kelelahan_sim = ctrl.ControlSystemSimulation(tingkat_kelelahan_ctrl)

# Inisialisasi list untuk menyimpan hasil
hasil_tingkat_kelelahan = []

# Iterasi melalui setiap record dalam data
for index, row in data.iterrows():
    # Masukkan nilai variabel input dari data yang dibaca
    tingkat_kelelahan_sim.input['minum'] = row['minum']
    tingkat_kelelahan_sim.input['lari'] = row['lari']
    tingkat_kelelahan_sim.input['tidur'] = row['tidur']

    # Hitung nilai variabel output
    tingkat_kelelahan_sim.compute()

    # Simpan hasil
    hasil_tingkat_kelelahan.append(tingkat_kelelahan_sim.output['tingkat_kelelahan'])

# Tambahkan hasil ke data frame
data['tingkat_kelelahan'] = hasil_tingkat_kelelahan

# Interpretasikan nilai fuzzy menjadi kategori
data['kategori_tingkat_kelelahan'] = data['tingkat_kelelahan'].apply(interpretasi_tingkat_kelelahan)

# Simpan ke file Excel
data.to_excel('azzam_fuzzy.xlsx', index=False)