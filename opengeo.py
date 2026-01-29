import urllib.request // Gör det möjligt att hämta data från webben via HTTP (som en webbläsare, fast i kod). 
import urllib.parse // Används för att bygga säkra URL:er, t.ex. om text innehåller mellanslag eller å/ä/ö. 
import json // Gör det möjligt att översätta JSON-text till Python-objekt (dict/list).
import ssl // Hanterar säker HTTPS-kommunikation (certifikat).

# API endpoint (ingen rate limit i uppgiften)
serviceurl = 'http://py4e-data.dr-chuck.net/opengeo?' // Bas-URL till webbtjänsten. Frågetecknet betyder: “här kommer parametrar snart”.


# Ignore SSL certificate errors (bra att ha med även om URL:en är http)
ctx = ssl.create_default_context()
ctx.check_hostname = False // Säger: “kontrollera inte att certifikatets namn matchar servern”.
ctx.verify_mode = ssl.CERT_NONE

address = input('Enter location: ').strip() // Frågar användaren efter en plats. .strip() tar bort extra mellanslag i början/slutet.

if len(address) < 1: // Om användaren bara trycker Enter → avsluta programmet. 
    quit()

# Bygg query-parametrar
params = {'q': address} // Skapar en dictionary med API-parametrar. q = query (sökfråga). Exempel: {'q': 'Monash University Churchill Australia'}

# Bygg komplett URL med korrekt URL-encoding
url = serviceurl + urllib.parse.urlencode(params) //Gör om dictionaryn till URL-format: q=Monash+University+Churchill+Australia Slutlig URL blir: http://py4e-data.dr-chuck.net/opengeo?q=Monash+University+Churchill+Australia

print('Retrieving', url) // Bra för felsökning – du ser exakt vad som anropas.

# Hämta data
uh = urllib.request.urlopen(url, context=ctx) // Skickar HTTP GET-request till API:t. uh = “url handle” (anslutningen).
data = uh.read().decode() // read() → hämtar bytes från servern. decode() → gör om bytes till text (str)

print('Retrieved', len(data), 'characters') // Visar hur mycket data som kom tillbaka.

# Parse JSON
js = json.loads(data) // Översätter JSON-text till Python: JSON-objekt → dict. JSON-array → list

# Plocka ut första plus_code
# I opengeo-svaret ligger det i första "feature": properties -> plus_code
try:
    plus_code = js['features'][0]['properties']['plus_code'] // Går igenom JSON-strukturen: features → lista [0] → första träffen properties → detaljer plus_code → det vi vill ha
except (KeyError, IndexError, TypeError):
    plus_code = None // Om något saknas (fel struktur, tom lista, fel typ) → krascha inte, sätt None.

if not plus_code: // Om plus_code inte hittades…
    print('==== Could not find plus_code in response ====')
    print(data) // Visa fel + hela svaret (bra för debugging).
else:
    print('Plus code', plus_code) // m allt gick bra → skriv ut svaret.
