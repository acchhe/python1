import sqlite3 // hämtar pythons inbyggda stöd för SQLite för att kunna prata med SQLite databasen

# Skapar/öppnar databasen (måste sluta på .sqlite för inlämningen)
conn = sqlite3.connect('emaildb.sqlite') // – Skapar en fil som heter emaildb.sqlite om den inte finns – Om den finns: öppnar den Varför .sqlite? Uppgiften kräver just detta filändelseformat.
cur = conn.cursor() // Vad är en cursor? Tänk den som: en penna som skriver SQL i databasen en hand som hämtar resultat All SQL körs via cursorn.

# Skapa tabell
cur.execute('DROP TABLE IF EXISTS Counts') // – Tar bort tabellen Counts om den redan finns Varför? Uppgiften säger: “If you run the program multiple times… make sure to empty out the data” Detta garanterar en ren start varje gång. 
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)') // skapar tabellen "Counts" med attributen "org" och "count"

# Läs filen
fname = 'mbox.txt' // Sparar filnamnet i en variabel så det är lätt att ändra senare.
with open(fname, encoding='utf-8', errors='ignore') as fh: // – Öppnar mbox.txt – errors='ignore' gör att konstiga tecken inte kraschar programmet – fh = filhandtag with betyder: Python stänger filen automatiskt när vi är klara
    for line in fh: // Loopar igenom varje rad i filen, en i taget. 
        if not line.startswith('From '): // – Vi bryr oss bara om rader som börjar med exakt: From användare@domän
            continue

        parts = line.split() // delar in raden i olika delar och returnerar dem i en lista == ['From', 'stephen.marquard@uct.ac.za', 'Sat', ...]
        if len(parts) < 2: // För säkerhets skull — om raden är konstig och saknar e-post.
            continue

        email = parts[1] // email = parts[1]
        if '@' not in email: // Skyddar mot skräprader.
            continue

        org = email.split('@')[-1].strip().lower() // split('@') → delar på @ [-1] → tar sista delen (domänen) strip() → tar bort mellanslag lower() → gör allt till små bokstäver

        # Kolla om org finns
        cur.execute('SELECT count FROM Counts WHERE org = ?', (org,)) // – Frågar databasen: Finns denna organisation redan? ? + (org,) = skydd mot SQL-injection (bra vana).
        row = cur.fetchone() // Finns org → row = (count,) Finns inte → row = None

        if row is None:
            cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,)) // Skapar ny rad med startvärde 1.
        else:
            cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,)) // Ökar räknaren med 1.

# En commit på slutet (snabbare)
conn.commit() // – Skriver alla ändringar permanent till filen – Vi gör detta en gång (snabbare)

# Visa topp 10 så du kan kontrollera hint (toppcount ska vara 536)
cur.execute('SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10') // Sorterar: högst count först visar bara 10 rader
for org, count in cur.fetchall():
    print(org, count)

cur.close()
conn.close() // Stänger databasen korrekt.

print("\nKlar! Databasen 'emaildb.sqlite' är skapad.")
