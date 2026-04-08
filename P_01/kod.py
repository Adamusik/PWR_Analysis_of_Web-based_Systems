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
# lekko pozmieniałem więc przydało by sie to jeszcze sprawdzić czy działa
sns.histplot(data=data_all, x='speed_mbps', hue='year', bins=50, kde=True)


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
# WYKRES 5/6 - Analiza Statystyczna i Korelacja Zmiennych (Heatmapy) - tego wcześniej nie było do sprawdzenia
# =========================

# Wybieramy numeryczne kolumny interesujące pod kątem oceny jakości połączenia sieciowego
# zmieniłem kolumny pod nasz plik excel - chyba zadziała
corr_cols = ['bytes_sec', 'bytes_total', 'packets_received', 'packets_sent', 'duration']
# definiowanie zmiennych 
valid_21 = data_dl_21[data_dl_21['successes'] == 1]
valid_23 = data_dl_23[data_dl_23['successes'] == 1]

# Obliczenie współczynników z próbki pomyślnych testów (successes == 1)
pearson_21 = valid_21[corr_cols].corr(method='pearson')
pearson_23 = valid_23[corr_cols].corr(method='pearson')

spearman_21 = valid_21[corr_cols].corr(method='spearman')
spearman_23 = valid_23[corr_cols].corr(method='spearman')

# WIZUALIZACJA - KORELACJA LINIOWA PEARSONA
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.heatmap(pearson_21, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, ax=axes[0])
axes[0].set_title('Macierz Korelacji (Pearson) - 2021', fontsize=12)

sns.heatmap(pearson_23, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, ax=axes[1])
axes[1].set_title('Macierz Korelacji (Pearson) - 2023', fontsize=12)

plt.tight_layout()
plt.show()

# WIZUALIZACJA - KORELACJA MONOTONICZNA SPEARMANA
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.heatmap(spearman_21, annot=True, fmt=".2f", cmap='viridis', vmin=-1, vmax=1, ax=axes[0])
axes[0].set_title('Macierz Korelacji (Spearman) - 2021', fontsize=14, pad=15)

sns.heatmap(spearman_23, annot=True, fmt=".2f", cmap='viridis', vmin=-1, vmax=1, ax=axes[1])
axes[1].set_title('Macierz Korelacji (Spearman) - 2023', fontsize=14, pad=15)

plt.tight_layout()
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
