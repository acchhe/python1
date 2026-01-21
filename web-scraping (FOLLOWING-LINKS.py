import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL/TLS certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter start URL: ')
position = int(input('Enter position (first link is 1): '))
repeats = int(input('Enter repeats: '))

for i in range(repeats):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all of the anchor tags
    tags = soup('a') // soup är hela HTML-dokumentet (parsad webbsida) 'a' betyder: anchor-taggar, alltså länkar 👉 Den här raden betyder: “Hämta ALLA <a>-taggar från webbsidan”. tags blir en lista (ordnad samling) av länkar.

    # Pick the link at the given position
    tag = tags[position - 1] // tag = tags[position - 1] Vad händer? tags är en lista position är ett tal du skrev in (t.ex. 18) Men: människor räknar från 1 Python räknar från 0

    name = tag.get_text(strip=True)// tag är en <a>-tagg <a>-taggar har text mellan öppning och stängning Exempel: <a href="...">Domanic</a> get_text() Hämtar texten: "Domanic".
    url = tag.get('href', None)// <a>-taggar har attribut href innehåller länkens URL Exempel: <a href="http://example.com">Name</a> get('href', None) Betyder: “Ge mig värdet på href. Om det inte finns, ge None istället för att krascha.”

    print(f"Step {i+1}: {name}") // i är loopens räknare (börjar på 0) i + 1 gör det mänskligt läsbart (steg 1, 2, 3…)
