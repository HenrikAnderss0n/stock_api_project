# Stock API Project

Ett Pythonprojekt som hämtar historiska dagliga aktiekurser för IBM från Alpha Vantage. Syftet är att fördjupa förståelsen för API-anrop, JSON, databehandling och felhantering.

Programmet bearbetar datan med Pandas, beräknar första, senaste, högsta och lägsta stängningskurs samt procentuell förändring. Det sparar även datan som CSV och skapar en kursgraf.

## Installation

Du behöver Python, internetanslutning och en egen API-nyckel från [Alpha Vantage](https://www.alphavantage.co/).

Ladda ner eller klona projektet och öppna en terminal i projektets huvudmapp.

Skapa en virtuell miljö:

```powershell
python -m venv .venv
```

Aktivera miljön i PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Installera beroendena:

```powershell
python -m pip install -r requirements.txt
```

Projektet använder `requests`, `pandas`, `python-dotenv` och `matplotlib`.

## Konfigurera API-nyckeln

Skapa en fil med namnet `.env` i projektets huvudmapp och lägg in:

```text
ALPHA_VANTAGE_API_KEY=DIN_API_NYCKEL
```

Ersätt `DIN_API_NYCKEL` med din egen nyckel. Filen `.env` finns i `.gitignore` och ska inte läggas upp på GitHub.

## Kör programmet

Kör följande från projektets huvudmapp, med den virtuella miljön aktiverad:

```powershell
python main.py
```

Programmet skriver ut resultaten i terminalen och sparar:

- `data/ibm_daily_prices.csv` – bearbetad kursdata.
- `output/ibm_price_chart.png` – graf över stängningskursen.

Dessa filer finns också med som sparade exempel och kan granskas utan ett nytt API-anrop. En lyckad körning skriver över de tidigare resultatfilerna.

## Data och exempelresultat

Datakällan är Alpha Vantages API-funktion `TIME_SERIES_DAILY`. Svaret innehåller dagliga värden för öppningskurs, högsta och lägsta kurs, stängningskurs och handelsvolym. Analysen använder stängningskursen (`close`).

Den sparade exempelkörningen omfattar 100 handelsdagar:

```text
Period: 2026-04-21 till 2026-09-11
Första stängningskurs: 255.68
Senaste stängningskurs: 243.29
Högsta stängningskurs: 329.23
Lägsta stängningskurs: 205.77
Förändring: -4.85 %
```

Kurserna anges i USD. Perioden och resultaten kan ändras vid en ny hämtning.

## Felhantering och begränsningar

Programmet hanterar bland annat saknad API-nyckel, nätverksfel, HTTP-fel och ogiltiga API-svar. Det kontrollerar även att tidsserien och förväntade kolumner finns samt att datum och numeriska värden inte saknas.

Aktiesymbolen är inställd på IBM i `main.py`. Programmet analyserar hela tidsserien som API:t returnerar. Användaren kan inte välja start- och slutdatum. Nya hämtningar kräver att Alpha Vantage är tillgängligt och att API-tjänstens anropsgränser inte har nåtts.

Analysen är avgränsad till enkla sammanfattningar av en aktie och innehåller ingen prognosmodell.

## Projektets uppbyggnad

`main.py` styr körningen. I mappen `src/` finns separata moduler för API-anrop, bearbetning, analys och visualisering.

Tekniska förklaringar, motiveringar, källor och självreflektion finns i [rapporten](report.md).