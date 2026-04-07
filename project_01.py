import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# ŚCIEŻKI DO PLIKÓW
# =========================

# 2023
path_2023_dl = 'C:\\prj\\pwr_mgr\\Analysis_of_Web-based_Systems-P\\202301\\curr_lct_dl.csv'
path_2023_ul = 'C:\\prj\\pwr_mgr\\Analysis_of_Web-based_Systems-P\\202301\\curr_lct_ul.csv'

# 2021
path_2021_dl = 'C:\\prj\\pwr_mgr\\Analysis_of_Web-based_Systems-P\\202101\\curr_lct_dl.csv'
path_2021_ul = 'C:\\prj\\pwr_mgr\\Analysis_of_Web-based_Systems-P\\202101\\curr_lct_ul.csv'


# =========================
# WCZYTANIE DANYCH
# =========================

data_dl_23 = pd.read_csv(path_2023_dl)
data_ul_23 = pd.read_csv(path_2023_ul)

data_dl_21 = pd.read_csv(path_2021_dl)
data_ul_21 = pd.read_csv(path_2021_ul)


# =========================
# PRZELICZENIE NA Mbps
# =========================

data_dl_23['speed_mbps'] = (data_dl_23['bytes_sec'] * 8) / 1_000_000
data_ul_23['speed_mbps'] = (data_ul_23['bytes_sec'] * 8) / 1_000_000

data_dl_21['speed_mbps'] = (data_dl_21['bytes_sec'] * 8) / 1_000_000
data_ul_21['speed_mbps'] = (data_ul_21['bytes_sec'] * 8) / 1_000_000


# =========================
# DODANIE KOLUMN (typ + rok)
# =========================

# typ
data_dl_23['type'] = 'Download'
data_ul_23['type'] = 'Upload'
data_dl_21['type'] = 'Download'
data_ul_21['type'] = 'Upload'

# rok
data_dl_23['year'] = '2023'
data_ul_23['year'] = '2023'
data_dl_21['year'] = '2021'
data_ul_21['year'] = '2021'


# =========================
# POŁĄCZENIE DANYCH
# =========================

data_all = pd.concat([data_dl_21, data_ul_21,data_dl_23, data_ul_23])


# =========================
# (OPCJONALNIE) USUNIĘCIE OUTLIERÓW
# =========================

data_all = data_all[data_all['speed_mbps'] < 200]


# =========================
# WYKRES 1 — 2021 vs 2023
# =========================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=data_all,
    x='speed_mbps',
    hue='year',
    bins=50,
    kde=True
)

plt.title('Porównanie prędkości Internetu: 2021 vs 2023')
plt.xlabel('Prędkość [Mbps]')
plt.ylabel('Liczba pomiarów')

plt.show()


# =========================
# WYKRES 2 — Download vs Upload
# =========================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=data_all,
    x='type',
    y='speed_mbps'
)

plt.title('Download vs Upload')
plt.xlabel('Typ')
plt.ylabel('Prędkość [Mbps]')
plt.ylim(0, 200)

plt.show()

# ==========================================
# WYKRES 3 — RELACJA: Pakiet vs Prędkość
# (Hipoteza: Im wyższy procent odebranych pakietów względem wysłanych (packets_sent),
# tym wyższa i stabilniejsza przepustowość bytes_sec.)
# ==========================================

plt.figure(figsize=(12, 7))

# Analizujemy np. dane Download z 2023 roku
sns.scatterplot(
    data=data_dl_23[data_dl_23['speed_mbps'] < 200], # Filtrowanie dla czytelności
    x='packets_received',
    y='speed_mbps',
    alpha=0.3,
    color='blue'
)

plt.title('Relacja: Liczba odebranych pakietów a Prędkość [2023 Download]')
plt.xlabel('Odebrane pakiety [packets_received]')
plt.ylabel('Prędkość [Mbps]')
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()

# WYKRES 4 — Zmiana efektywności pakietowej:2021 vs 2023
# Obliczenie współczynnika korelacji (matematyczne potwierdzenie relacji)
correlation = data_dl_23['packets_received'].corr(data_dl_23['speed_mbps'])
print(f"\nWspółczynnik korelacji między pakietami a prędkością: {correlation:.2f}")

# Porównanie relacji pakiety vs prędkość 2021 r. do 2023 r.
plt.figure(figsize=(12, 7))
sns.lmplot(
    data=data_all[data_all['speed_mbps'] < 200],
    x='packets_received',
    y='speed_mbps',
    hue='year',
    scatter_kws={'alpha':0.2}
)
plt.title('Zmiana efektywności pakietowej: 2021 vs 2023')
plt.show()

# =========================
# STATYSTYKI
# =========================

print("=== DOWNLOAD 2023 ===")
print(data_dl_23['speed_mbps'].describe())

print("\n=== DOWNLOAD 2021 ===")
print(data_dl_21['speed_mbps'].describe())

print("\n=== UPLOAD 2023 ===")
print(data_ul_23['speed_mbps'].describe())

print("\n=== UPLOAD 2021 ===")
print(data_ul_21['speed_mbps'].describe())