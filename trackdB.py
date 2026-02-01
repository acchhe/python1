import sqlite3 // Importerar Pythons inbyggda bibliotek för att prata med SQLite-databaser.

conn = sqlite3.connect('trackdb.sqlite') // Skapar/öppnar databasen trackdb.sqlite. Om filen inte finns: den skapas. conn = “anslutningen” till databasen (tänk: en öppen dörr till filen).
cur = conn.cursor() // Skapar en cursor. Cursorn är objektet du använder för att köra SQL-kommandon och hämta resultat.

# Make some fresh tables using executescript()
cur.executescript(''' // Kör flera SQL-satser på en gång (separerade med ;). Bra när du ska skapa tabeller eller nollställa databasen.
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track; // Tar bort tabellerna om de redan finns. IF EXISTS gör att det inte blir fel om tabellen inte finns. Detta ger dig en “tom start” varje gång du kör programmet.

CREATE TABLE Artist ( // Skapar tabell med: id: primärnyckel (unik identifierare, SQLite kan auto-fylla den) name: artistnamn, måste vara unik (UNIQUE)
    id  INTEGER PRIMARY KEY,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER PRIMARY KEY,
    artist_id  INTEGER, // artist_id är en “referens” till Artist.id. title är unik (så samma albumtitel kan inte finnas två gånger i hela DB; ibland vill man egentligen ha unik per artist, men här är det förenklat).
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER PRIMARY KEY,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

handle = open('tracks.csv') // Öppnar filen tracks.csv för läsning. handle är “filhandtaget” du läser rader ifrån. (Tips: brukar vara bättre att ange encoding och använda with open(...) för automatisk stängning.)

# Another One Bites The Dust,Queen,Greatest Hits,55,100,217103
#   0                          1      2           3  4   5

for line in handle:
    line = line.strip() // Tar bort whitespace i början/slutet, inklusive \n (radbrytning).
    pieces = line.split(',')
    if len(pieces) < 6 : continue // Om raden inte har minst 6 delar, hoppa över den.

    name = pieces[0]
    artist = pieces[1]
    album = pieces[2]
    count = pieces[3]
    rating = pieces[4]
    length = pieces[5] // Här skapas variabler med tydliga namn.

    print(name, artist, album, count, rating, length) // Skriver ut vad som lästs in så du ser att parsningen fungerar.

    cur.execute('''INSERT OR IGNORE INTO Artist (name) // Försöker lägga in artisten i tabellen Artist. INSERT OR IGNORE betyder: om artistens name redan finns (pga UNIQUE) → gör inget (ignorera) annars → skapa ny rad ? är en parameter-platshållare. (artist,) är en tuple med ett element (kommat är viktigt).
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, )) Du frågar databasen: “Ge mig id för den här artisten”. Du tar första raden:
    artist_id = cur.fetchone()[0] //  fetchone() returnerar en tuple, t.ex. (17,) [0] tar själva numret 17 artist_id blir alltså ett heltal id som används som foreign key i Album.

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) // Försöker lägga in albumet. Om albumtiteln redan finns (UNIQUE) → ignoreras. Lägger också in artist_id så albumet kopplas till artisten.
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, )) // Hämtar albumets id. fetchone()[0] ger själva id-numret.
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track // Om det redan finns ett spår med samma title (UNIQUE): SQLite tar bort den gamla raden och lägger in en ny Annars: lägger in en ny rad. Den sätter trackens: titel album_id (koppling till Album) längd, rating, count
        (title, album_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ? )''', 
        ( name, album_id, length, rating, count ) )

    conn.commit()
