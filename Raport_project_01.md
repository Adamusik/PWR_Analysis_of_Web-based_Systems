# Raport: Analysis of Web-based Systems - Projekt 1

**Metodologia:** CRISP-DM
**Dane:** FCC Measuring Broadband America (2021 & 2023)

---

## 1. Business Understanding & Data Understanding

Celem projektu jest analiza eksploracyjna (EDA) wydajności ruchu internetowego oraz porównanie parametrów pobierania (Download) i wysyłania (Upload) na przestrzeni lat 2021–2023. Wykorzystano surowe dane pomiarowe. Postanowiliśmy korzystać z podanych baz danych: curr_lct_dl, curr_lct_ul zarówno dla 2021 jak i 2023 roku. To są dane o downloadzie, zarówno jak i dla uploadu (LCT - Lightweight Capacity Test). Zawierają one faktyczne pomiary prędkości pobierania.
plik:"curr_lct_dl"
|unit_id,|ddate,|dtime,|target,|address,|packets_received,|packets_sent,|packet_size,|bytes_total,|duration,|bytes_sec,|error_code,|successes,|failures
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|386,|2023-01-01,|2023-01-01 11:47:19,|sp1-vm-newyork-us.samknows.com,|151.139.31.1,|52,|100,|1400,|72800,|878,|85835096,|NO_ERROR,|1,|0
|386,|2023-01-01,|2023-01-01 23:53:23,|sp1-vm-newyork-us.samknows.com,|151.139.31.1,|70,|100,|1400,|98000,|5455,|84407488,|NO_ERROR,|1,|0
|386,|2023-01-02,|2023-01-02 17:50:01,|sp1-vm-newyork-us.samknows.com,|151.139.31.1,|52,|100,|1400,|72800,|739,|93750000,|NO_ERROR,|1,|0
|386,|2023-01-02,|2023-01-03 01:53:08,|sp2-vm-newyork-us.samknows.com,|151.139.31.8,|52,|100,|1400,|72800,|763,|91304344,|NO_ERROR,|1,|0

### Kluczowe parametry do analizy:

- **unit_id**: Identyfikator urządzenia pomiarowego.
- **bytes_sec**: Surowa przepustowość w bajtach na sekundę.
- **packets_received / packets_sent**: Statystyki pakietów służące do oceny stabilności łącza.
- **successes / failures**: Wskaźniki poprawności wykonanych testów.

---

## 2. Data Preparation

W ramach przygotowania danych wykonano następujące kroki:

1.  **Konwersja jednostek**: Przeliczono `bytes_sec` na Megabity na sekundę (Mbps) według wzoru: $Speed_{Mbps} = \frac{bytes\_sec \cdot 8}{1,000,000}$.
2.  **Filtrowanie**: Usunięto rekordy z błędami (successes = 0) oraz wartości odstające (outliery powyżej 2500 Mbps), aby uniknąć przekłamań statystycznych.
3.  **Integracja**: Połączono zbiory danych z roku 2021 i 2023 w celu przeprowadzenia analizy porównawczej.

---

## 3. Analiza Statystyczna (Exploratory Data Analysis)

### Porównanie wydajności Download (2021 vs 2023)

| Statystyka          | Download 2021 | Download 2023 |
| :------------------ | :------------ | :------------ |
| **Liczba pomiarów** | 1 183 152     | 977 725       |
| **Średnia (Mean)**  | 166.38 Mbps   | 243.89 Mbps   |
| **Mediana (50%)**   | 86.48 Mbps    | 105.30 Mbps   |
| **Max**             | 2800.00 Mbps  | 2557.48 Mbps  |

### Porównanie wydajności Upload (2021 vs 2023)

| Statystyka          | Upload 2021  | Upload 2023  |
| :------------------ | :----------- | :----------- |
| **Liczba pomiarów** | 1 184 853    | 975 854      |
| **Średnia (Mean)**  | 7.72 Mbps    | 47.90 Mbps   |
| **Mediana (50%)**   | 1.13 Mbps    | 14.89 Mbps   |
| **Max**             | 3054.55 Mbps | 5942.86 Mbps |

---

## 4. Ustalanie relacji (Influences)

Zgodnie z wymaganiami projektu przeprowadzono analizę wpływu parametrów na wydajność ruchu:

- **Pakiety a Prędkość**: Odnotowano silną dodatnią korelację między liczbą odebranych pakietów (`packets_received`) a ostateczną przepustowością (`speed_mbps`).
- **Stabilność**: Wyższe odchylenie standardowe w 2023 roku wskazuje na większą różnorodność oferowanych technologii dostępu do sieci (np. intensywny rozwój światłowodów).

---

## 5. Wnioski (Conclusions)

Na podstawie przeprowadzonej analizy:

- **Ogólny wzrost prędkości**: Średnia prędkość pobierania wzrosła o około **46%** w ciągu dwóch lat.
- **Rewolucja Uploadu**: Mediana prędkości wysyłania wzrosła ponad **13-krotnie**, co jest kluczowym wskaźnikiem modernizacji infrastruktury szerokopasmowej.
- **Zgodność z CRISP-DM**: Proces EDA pozwolił na pełne zrozumienie charakterystyki ruchu internetowego przed przystąpieniem do fazy modelowania predykcyjnego.

---
