import urllib.request
import urllib.parse
import json
import ssl

# API endpoint (ingen rate limit i uppgiften)
serviceurl = 'http://py4e-data.dr-chuck.net/opengeo?'

# Ignore SSL certificate errors (bra att ha med även om URL:en är http)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

address = input('Enter location: ').strip()
if len(address) < 1:
    quit()

# Bygg query-parametrar
params = {'q': address}

# Bygg komplett URL med korrekt URL-encoding
url = serviceurl + urllib.parse.urlencode(params)

print('Retrieving', url)

# Hämta data
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()

print('Retrieved', len(data), 'characters')

# Parse JSON
js = json.loads(data)

# Plocka ut första plus_code
# I opengeo-svaret ligger det i första "feature": properties -> plus_code
try:
    plus_code = js['features'][0]['properties']['plus_code']
except (KeyError, IndexError, TypeError):
    plus_code = None

if not plus_code:
    print('==== Could not find plus_code in response ====')
    print(data)
else:
    print('Plus code', plus_code)
