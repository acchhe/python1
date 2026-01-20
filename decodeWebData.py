import urllib.request, urllib.parse, urllib.error

handle = urllib.request.urlopen("https://data.pr4e.org/intro-short.txt")

for line in handle:
    print(line.decode().rstrip())


Detta program hämtar en textfil från internet via en URL och skriver ut innehållet rad för rad i terminalen.
Programmet använder Pythons inbyggda bibliotek urllib för att göra HTTP-förfrågningar.

🧩 Kod
import urllib.request, urllib.parse, urllib.error

handle = urllib.request.urlopen("https://data.pr4e.org/intro-short.txt")

for line in handle:
    print(line.decode().rstrip())

🔍 Förklaring av viktiga delar
1️⃣ urllib – nätverksbiblioteket
import urllib.request, urllib.parse, urllib.error


urllib är ett inbyggt Python-bibliotek som används för att arbeta med URL:er och webbresurser.

urllib.request
→ används för att öppna URL:er (t.ex. webbsidor, textfiler)

urllib.parse
→ används för att tolka och bygga URL:er (används inte i denna kod men importeras ofta tillsammans)

urllib.error
→ innehåller felklasser för nätverksfel (t.ex. om URL:en inte finns)

2️⃣ urlopen() – öppna en webbresurs
handle = urllib.request.urlopen("https://data.pr4e.org/intro-short.txt")


Skickar en HTTP-förfrågan till URL:en

Returnerar ett fil-liknande objekt

Kan användas precis som en vanlig fil i Python

handle fungerar alltså ungefär som om vi hade öppnat en lokal textfil med open().

3️⃣ Iterera över innehållet rad för rad
for line in handle:


Varje line är en rad från filen

Raderna kommer i bytes-format, inte som vanliga strängar

4️⃣ decode() – konvertera bytes till sträng
line.decode()


Data från webben kommer som bytes

decode() konverterar bytes → sträng (UTF-8 som standard)

Exempel:

b'Hello\n'  →  'Hello\n'

5️⃣ rstrip() – ta bort radbrytningar
.rstrip()


Tar bort osynliga tecken på slutet av raden

T.ex. \n (ny rad)

Utan rstrip() hade varje rad skrivits ut med extra tomma rader.

6️⃣ print() – skriva ut resultatet
print(line.decode().rstrip())


Skriver ut varje rad i ett rent och läsbart format

✅ Sammanfattning

Programmet:

Importerar nätverksbiblioteket urllib

Hämtar en textfil från internet

Läser filen rad för rad

Konverterar bytes till strängar

Skriver ut innehållet snyggt i terminalen
