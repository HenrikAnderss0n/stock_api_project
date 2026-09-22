# Fördjupning i Python – aktiedata från ett API

## Syfte

Syftet var att lära mig hur Python kan hämta data från ett externt API, kontrollera svaret och förbereda datan för analys. Jag ville förstå HTTP-anrop, JSON, datatyper och felhantering samt hur en API-nyckel kan hållas utanför källkoden.

Jag byggde ett mindre program som hämtar dagliga aktiekurser för IBM från Alpha Vantage. Programmet beräknar enkla nyckeltal och sparar data och en graf. Jag avgränsade arbetet till API-hantering och grundläggande bearbetning. Handelssystem, maskininlärning och prognoser ingår inte.

## Området och dess relevans

Ett API är ett gränssnitt som gör att program kan kommunicera med andra system. I projektet skickar Python en förfrågan till Alpha Vantage och får kursdata tillbaka.

Det är relevant för Data Science eftersom data ofta kommer från externa tjänster. Innan den kan analyseras behöver den hämtas, kontrolleras och organiseras. Fördjupningen handlar därför främst om hur Python hanterar extern data, medan aktiekurserna fungerar som ett praktiskt exempel.

## Viktiga begrepp

### HTTP-anrop och statuskoder

Biblioteket `requests` skickar ett HTTP GET-anrop. Parametrarna anger API-funktionen `TIME_SERIES_DAILY`, aktiesymbolen och API-nyckeln. Programmet använder `timeout=10` för att begränsa väntan vid anslutning eller utebliven dataöverföring.

Statuskod 200 betyder att HTTP-förfrågan lyckades, men garanterar inte att svaret innehåller aktiedata. API:t kan exempelvis returnera information om en anropsgräns. Därför kontrollerar programmet både HTTP-statusen och innehållet.

### JSON och DataFrame

JSON är formatet som API:t använder för sitt svar. `response.json()` omvandlar svaret till Pythonobjekt, här bland annat nästlade dictionaries. Varje handelsdatum hör ihop med öppningskurs, högsta och lägsta kurs, stängningskurs och volym.

En Pandas DataFrame organiserar uppgifterna i en tabell. Följande kod gör varje datum till en rad:

```python
df = pd.DataFrame.from_dict(time_series, orient="index")
```

`orient="index"` behövs eftersom datumen är nycklar i den yttre dictionaryn. Priserna kommer som text och konverteras till tal med `pd.to_numeric`. Datumen konverteras med `pd.to_datetime`. Rätt datatyper behövs för beräkningar och datumhantering.

### API-nyckel

API-nyckeln läses från en lokal `.env`-fil med `python-dotenv` och `os.getenv`. Filen finns i `.gitignore`. Nyckeln hålls därmed utanför källkoden och ska inte läggas upp på GitHub.

## Genomförande

Jag började med ett enkelt API-anrop för att undersöka svarets struktur. Därefter byggde jag bearbetningen, analysen och grafen. Projektet använder `requests`, `pandas`, `python-dotenv` och `matplotlib`. Installation och körning beskrivs i README:n.

### Struktur och tekniska val

`main.py` styr körningen. Koden i `src/` har fyra ansvarsområden:

- `api_client.py` hämtar tidsserien och kontrollerar API-svaret.
- `processing.py` validerar och omvandlar datan till en DataFrame.
- `analysis.py` beräknar sammanfattande nyckeltal.
- `visualization.py` skapar och sparar kursgrafen.

Uppdelningen gör det lättare att följa flödet och ändra en del i taget. Jag använde requests direkt för att förstå HTTP-anrop och JSON. Ett färdigt bibliotek för finansdata hade kunnat minska mängden egen kod, men också dolt delar av kommunikationen jag ville lära mig.

Bearbetningen ger kolumnerna enklare namn och sorterar raderna från äldsta till senaste datum. Sorteringen är viktig eftersom analysen använder första och sista raden för att beräkna periodens förändring.

### Validering och felhantering

Programmet kontrollerar att API-nyckeln och aktiesymbolen finns. `raise_for_status()` upptäcker HTTP-fel. Programmet hanterar också nätverksproblem, ogiltig JSON och API-svar utan `Time Series (Daily)`.

Bearbetningen kontrollerar att tidsserien inte är tom och att de förväntade kolumnerna finns. Efter datatypskonverteringen kontrolleras även saknade värden:

```python
required_columns = ["date", *numeric_columns]

if df[required_columns].isna().any().any():
    raise ValueError(
        "API-datan innehåller saknade datum "
        "eller numeriska värden"
    )
```

`isna()` markerar saknade värden. Första `any()` kontrollerar varje kolumn och den andra avgör om någon kolumn innehåller ett saknat värde. Kontrollen behövs eftersom en kolumn kan finnas även om en enskild rad saknar sitt värde.

Jag valde att stoppa bearbetningen vid saknade värden. Att automatiskt fylla i priser eller ta bort rader kan påverka resultatet. `main.py` fångar förväntade fel och skriver ett felmeddelande.

### Kontroll av lösningen

Ett tidigare test med tom aktiesymbol gav meddelandet `Fel: Aktiesymbol saknas`. Vid granskningen kontrollerades också den sparade datan och ett exempel där en handelsdag saknade stängningskurs. Den nya valideringen stoppade det ofullständiga exemplet, medan de 100 sparade raderna fortfarande gav samma nyckeltal.

Programmet sparar data i `data/ibm_daily_prices.csv` och grafen i `output/ibm_price_chart.png`. Dessa resultat kan granskas även när ett nytt API-anrop inte är möjligt.

## Resultat

Den sparade körningen innehåller 100 handelsdagar för IBM, från 2026-04-21 till 2026-09-11. Sammanfattningen av stängningskurserna är:

```text
Första stängningskurs: 255.68 USD
Senaste stängningskurs: 243.29 USD
Högsta stängningskurs: 329.23 USD
Lägsta stängningskurs: 205.77 USD
Förändring: -4.85 %
```

Förändringen beräknas som skillnaden mellan senaste och första stängningskursen, dividerad med den första kursen och multiplicerad med 100. Slutkursen var alltså cirka 4,85 procent lägre än startkursen.

Den sparade grafen visar variationerna under perioden. Högsta och lägsta värdet ovan gäller stängningskurser, inte högsta och lägsta notering under en handelsdag. Skillnaden mellan första och sista kursen beskriver därför inte hela utvecklingen.

## Begränsningar och möjliga förbättringar

Programmet analyserar hela tidsserien som API:t returnerar. Användaren kan inte välja start- och slutdatum, och en ny hämtning kan ge en annan period. Aktiesymbolen är inställd på IBM i koden och programmet analyserar en aktie åt gången.

Lösningen är beroende av internet, en giltig API-nyckel och Alpha Vantages tillgänglighet och anropsgränser. Om svarets struktur ändras kan koden behöva anpassas. Sparade resultat gör det möjligt att visa en tidigare körning, men programmet växlar inte automatiskt till CSV-filen när API:t misslyckas.

Valideringen upptäcker flera vanliga problem, men garanterar inte att varje pris är rimligt. Möjliga förbättringar är rimlighetskontroller och valbar aktiesymbol. Mer avancerad analys och jämförelser mellan aktier är möjliga fortsättningar. De ingår inte i projektets nuvarande avgränsning.

## Koppling till yrkesrollen

En Data Scientist behöver kunna förstå externa datastrukturer, hantera fel och förbereda data för vidare analys. Projektet demonstrerar ett sådant arbetsflöde i liten skala. Samma principer kan användas för väderdata, energidata eller företags interna API:er.

En viktig slutsats är att kvaliteten på analysen beror på stegen före själva beräkningen. Datatyper, datumordning och hantering av saknade värden påverkar om resultatet går att använda.

## Källor

- [Alpha Vantage](https://www.alphavantage.co/documentation/) – API-funktion, parametrar och svarsstruktur.
- [Requests](https://requests.readthedocs.io/) – HTTP-anrop, timeout och felhantering.
- [Pandas](https://pandas.pydata.org/docs/) – DataFrame, datatyper, sortering och CSV-export.
- [python-dotenv](https://pypi.org/project/python-dotenv/) – inläsning av miljövariabler från `.env`.
- [Matplotlib](https://matplotlib.org/stable/) – skapande och sparande av grafen.

## Självreflektion

### Vad lärde jag mig?

Jag lärde mig hur Python hämtar extern data och hur nästlad JSON kan bli en användbar tabell. Jag förstod också varför ett lyckat HTTP-anrop inte räcker som kontroll av datan.

### Vad var svårast?

Det svåraste var att förstå hur anropet, svarets struktur och datatyperna hänger ihop. Jag behövde också skilja mellan nätverksfel och svar där API:t fungerar men inte levererar förväntad data.

### Vilket tekniskt val är jag mest nöjd med?

Uppdelningen i moduler gav varje del ett tydligt ansvar och gjorde programmet lättare att följa. Att hålla API-nyckeln utanför koden var också ett viktigt val.

### Vad hade jag gjort annorlunda?

Jag hade planerat kontroller av saknade värden tidigare. Att först bygga en enkel prototyp var samtidigt användbart eftersom jag kunde förstå en del i taget.

### Vad är ett naturligt nästa steg?

Jag skulle låta användaren välja aktiesymbol vid körning. Därefter skulle samma struktur kunna användas för att jämföra flera aktier.

### Vilket betyg bedömer jag att arbetet motsvarar?

Jag bedömer att arbetet motsvarar VG. Projektet har ett avgränsat syfte, fungerande kod, körinstruktioner, sparade resultat och källor. Min bedömning bygger också på att jag kan förklara och motivera tekniska val samt resonera om begränsningar och alternativ. Det gäller särskilt skillnaden mellan HTTP-status och API-innehåll samt varför datan måste kontrolleras före analys.