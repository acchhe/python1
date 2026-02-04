import sqlite3 # pratar med en SQLite-databasfil
import urllib.error # feltyper från nätverksanrop (används indirekt i try/except).
import ssl # hanterar HTTPS/SSL-inställningar.
from urllib.parse import urljoin # bygger en absolut URL av en bas-URL + en relativ länk
from urllib.parse import urlparse # plockar isär en URL (scheme, host, path osv).
from urllib.request import urlopen # hämtar innehållet från en URL.
from bs4 import BeautifulSoup # tolkar HTML så du kan hitta länkar <a href=...>.

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
# Detta skapar ett SSL-“context” som: inte bryr sig om att domännamn matchar certifikat (check_hostname=False) accepterar även “osäkra” certifikat (CERT_NONE) Varför? För att programmet inte ska krascha på sidor med certifikatproblem.

conn = sqlite3.connect('spider.sqlite') # öppnar (eller skapar) filen spider.sqlite.
cur = conn.cursor() # är objektet du använder för att köra SQL-kommandon.

cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
     error INTEGER, old_rank REAL, new_rank REAL)''')
##Skapar tabellen om den inte finns

Tabellen Pages lagrar info per webbsida:

id: unikt id (automatiskt)

url: unik URL

html: sidans HTML (sparas som blob/text)

error: felkod (t.ex. -1 eller HTTP status)

old_rank, new_rank: används ofta för PageRank senare (inte fullt här)##

cur.execute('''CREATE TABLE IF NOT EXISTS Links
    (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')
###Tabellen Links är länk-grafen:

from_id: sidan som länkar

to_id: sidan den länkar till

UNIQUE(...): undvik dubbla länkar.###

cur.execute('''CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE)''') #Tabellen Webs lagrar “start-domäner/områden” crawlern får hålla sig inom.


cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
### Letar efter en sida där:

html is NULL = inte hämtad ännu

error is NULL = inget fel registrerat

ORDER BY RANDOM() = slumpa vilken sida vi tar nästa

LIMIT 1 = ta en

fetchone() = hämta raden (eller None om ingen finns)###


if row is not None:
    print("Restarting existing crawl.  Remove spider.sqlite to start a fresh crawl.") # Om det finns en sådan rad: databasen har redan arbete kvar → den fortsätter.
else :
    starturl = input('Enter web url or enter: ')
    if ( len(starturl) < 1 ) : starturl = 'http://www.dr-chuck.com/' #Frågar efter start-URL Om du trycker Enter blir default dr-chuck.
    if ( starturl.endswith('/') ) : starturl = starturl[:-1] # Tar bort sista / för att undvika dubletter.
		
    web = starturl
    if ( starturl.endswith('.htm') or starturl.endswith('.html') ) :
        pos = starturl.rfind('/')
        web = starturl[:pos]
		###Om starturl är en fil som /page.html:

hitta sista /

web blir “mappen” (bas-URL)###

    if ( len(web) > 1 ) :
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES ( ? )', ( web, ) )
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( starturl, ) )
        conn.commit()
###Lägg basen i Webs

Lägg startsidan i Pages med html=NULL (inte hämtad än)

new_rank=1.0 (för framtida rank-beräkning)

commit() sparar till fil.###


cur.execute('''SELECT url FROM Webs''')
webs = list()
for row in cur:
    webs.append(str(row[0]))

print(webs)
##Läser alla links till en lista
Lägg basen i Webs

Lägg startsidan i Pages med html=NULL (inte hämtad än)

new_rank=1.0 (för framtida rank-beräkning)

commit() sparar till fil.###

many = 0
while True: # Evig loop tills du bryter.
	
    if ( many < 1 ) :
        sval = input('How many pages:')
        if ( len(sval) < 1 ) : break
        many = int(sval)
    many = many - 1
	###Om many är 0 frågar den hur många sidor du vill crawla.

Tom input → avsluta.

Annars minskar den many med 1 per varv.###

    cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        row = cur.fetchone()
        # print row
        fromid = row[0]
        url = row[1]

###Plockar en slumpad “oupphämtad” sida.

fromid = sidans id i DB (för Links-tabellen)

url = sidan vi ska hämta###

    except:
        print('No unretrieved HTML pages found') # Om row var None eller något gick fel → inget kvar att crawla.
        many = 0
        break

    print(fromid, url, end=' ') # Statusrad. Skriver t.ex. 12 http://... på samma rad.

    # If we are retrieving this page, there should be no links from it

    cur.execute('DELETE from Links WHERE from_id=?', (fromid, ) ) # Om man hämtar om sidan vill man inte ha gamla länkar kvar.

    try:
        document = urlopen(url, context=ctx) 
		html = document.read() # Öppnar URL:en med SSL-context Läser bytes (rå HTML)

        if document.getcode() != 200 :
            print("Error on page: ",document.getcode())
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url) ) # Om HTTP status inte är 200 → spara felkoden i databasen.

        if 'text/html' != document.info().get_content_type() :
            print("Ignore non text/html page")
            cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
            conn.commit()
            continue # Om det inte är HTML (t.ex. PDF, bild) → ta bort sidan ur Pages och hoppa vidare.

        print('('+str(len(html))+')', end=' ')

        soup = BeautifulSoup(html, "html.parser")

#Skriv storlek på HTML i bytes

Skapa soup för att kunna hitta länkar##

    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break

    except:
        print("Unable to retrieve or parse page")
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
        conn.commit()
        continue
##
Ctrl+C → avbryt snyggt

Annat fel → error=-1 och fortsätt.##

    cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( url, ) ) # Ser till att URL:en finns i Pages.
    cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url ) ) # Lägger själva HTML:en i Pages.html memoryview(html) används för att lagra bytes effektivt i SQLite.
    conn.commit()

    # Retrieve all of the anchor tags
    tags = soup('a') # tags blir alla <a>-taggar.
    count = 0

    for tag in tags: # plocka href om ingen href → hoppa över
        href = tag.get('href', None)
        if ( href is None ) : continue
			
        
        up = urlparse(href) # urlparse kollar om länken är absolut (har scheme som http/https) om den är relativ → gör den absolut med urljoin
        if ( len(up.scheme) < 1 ) :
            href = urljoin(url, href)


        ipos = href.find('#') # Tar bort fragment #section (så samma sida inte blir flera).
        if ( ipos > 1 ) : href = href[:ipos]
			
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ) : continue
        if ( href.endswith('/') ) : href = href[:-1]
        # print href
        if ( len(href) < 1 ) : continue
			##hoppa över bilder

normalisera slash på slutet

hoppa över tomma##

		
        found = False # Kolla om länken börjar med någon av bas-URLs i webs Om inte → ignorera (så du inte crawlar hela internet)
        for web in webs:
            if ( href.startswith(web) ) :
                found = True
                break
        if not found : continue 

        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( href, ) )
        count = count + 1
        conn.commit()
##Se till att målsidan finns i Pages (oupphämtad än) öka räknare för antal funna länkar###

        cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( href, ))
        try:
            row = cur.fetchone()
            toid = row[0]

##Hämta id för href-sidan → det blir toid##

        except: # Om den saknas (ovanligt) → hoppa.
            print('Could not retrieve id')
            continue
        # print fromid, toid
        cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromid, toid ) ) #Spara länken: fromid -> toid i Links.


    print(count)  # Skriv hur många länkar den hittade på sidan Stäng cursor

cur.close()
