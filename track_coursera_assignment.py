import sqlite3

CSV_FILE = "tracks.csv"
DB_FILE = "trackdb.sqlite"  # måste sluta på .sqlite

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Nollställ databasen varje körning
cur.executescript("""
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Artist;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
""")

def to_int(s: str) -> int:
    # SQLite klarar str->int ofta, men vi gör det tydligt och robust
    try:
        return int(s)
    except Exception:
        return 0

with open(CSV_FILE, encoding="utf-8", errors="ignore") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue

        pieces = line.split(",")
        # vi behöver minst 6-7 fält beroende på exportformat
        if len(pieces) < 6:
            continue

        # Städa citattecken runt fält (ibland kommer "..." från CSV-exporter)
        pieces = [p.strip().strip('"') for p in pieces]

        # Två vanliga format:
        # A) name, artist, album, count, rating, length               (6 fält)
        # B) name, artist, album, genre, count, rating, length        (7 fält)
        #
        # Vi detekterar vilket som gäller genom att titta på om pieces[3] är siffra.
        name = pieces[0]
        artist = pieces[1]
        album = pieces[2]

        genre = "Unknown"
        count = rating = length = 0

        if len(pieces) >= 7 and not pieces[3].isdigit():
            # Format B: genre ligger på index 3
            genre = pieces[3]
            count = to_int(pieces[4])
            rating = to_int(pieces[5])
            length = to_int(pieces[6])
        else:
            # Format A: genre saknas eller ligger inte på index 3
            count = to_int(pieces[3])
            rating = to_int(pieces[4])
            length = to_int(pieces[5])
            # Om genre faktiskt finns som 7:e fält trots att index 3 är siffra:
            if len(pieces) >= 7:
                genre = pieces[6]

        # 1) Artist
        cur.execute("INSERT OR IGNORE INTO Artist (name) VALUES (?)", (artist,))
        cur.execute("SELECT id FROM Artist WHERE name = ?", (artist,))
        artist_id = cur.fetchone()[0]

        # 2) Genre
        cur.execute("INSERT OR IGNORE INTO Genre (name) VALUES (?)", (genre,))
        cur.execute("SELECT id FROM Genre WHERE name = ?", (genre,))
        genre_id = cur.fetchone()[0]

        # 3) Album
        cur.execute(
            "INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)",
            (album, artist_id),
        )
        cur.execute("SELECT id FROM Album WHERE title = ?", (album,))
        album_id = cur.fetchone()[0]

        # 4) Track
        cur.execute(
            """
            INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, album_id, genre_id, length, rating, count),
        )

# Commit en gång (snabbt)
conn.commit()

# Kontrollfrågan som graderaren kör (nästan exakt)
cur.execute("""
SELECT Track.title, Artist.name, Album.title, Genre.name
FROM Track
JOIN Genre ON Track.genre_id = Genre.id
JOIN Album ON Track.album_id = Album.id
JOIN Artist ON Album.artist_id = Artist.id
ORDER BY Artist.name
LIMIT 3
""")

rows = cur.fetchall()
for r in rows:
    print(r)

cur.close()
conn.close()

print(f"\nKlar! Skapade databasen: {DB_FILE}")
