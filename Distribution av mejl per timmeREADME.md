Detta program läser igenom filen mbox-short.txt och räknar hur många mejl som skickats under varje timme på dygnet.
Resultatet skrivs ut sorterat i stigande ordning efter timme.

📂 Indata

Filen mbox-short.txt innehåller rader med mejlinformation, till exempel:

From stephen.marquard@uct.ac.za Sat Jan  5 06:14:16 2008


Programmet använder endast rader som börjar med "From " (med mellanslag).

🧠 Viktiga delar i koden
1️⃣ Dictionary för att lagra antal per timme
count = {}


Används för att lagra timme → antal mejl

Exempel:

{'06': 1, '09': 2, '17': 2}

2️⃣ Öppna filen säkert
with open("mbox-short.txt", "r") as fil:


with ser till att filen stängs automatiskt

fil används för att läsa raden en i taget

3️⃣ Filtrera rätt rader
if line.startswith("From "):


Säkerställer att endast relevanta rader behandlas

Viktigt att inte använda "From:"

4️⃣ Dela upp raden i ord
words = line.split()


Delar raden vid mellanslag

Tiden (HH:MM:SS) ligger alltid på index 5

5️⃣ Plocka ut timmen
time = words[5]
hour = time.split(":")[0]


time → "06:14:16"

hour → "06"

6️⃣ Räkna förekomster per timme
count[hour] = count.get(hour, 0) + 1


get(hour, 0) ger 0 om timmen inte finns ännu

Ökar räknaren med 1

7️⃣ Sortera och skriv ut resultatet
for key, value in sorted(count.items()):
    print(key, value)


count.items() ger (timme, antal)

sorted() sorterar efter timme

Skriver ut i formatet:

06 1
09 2
17 2

✅ Exempel på output
04 3
06 1
07 1
09 2
10 3
11 6
14 1
15 2
16 4
17 2
18 1
19 1
