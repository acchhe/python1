Web scraping betyder:

att ett program automatiskt hämtar en webbsida och extraherar specifik information ur HTML-koden.

from bs4 import BeautifulSoup //importerar HTML-parsern Beautiful Soup.HTML är strukturerat språk, inte vanlig text. Beautiful Soup låter dig: hitta taggar (<span>, <a>,<p>) läsa innehållet i dem navigera i dokumentet. HTML ska inte lösas med regex eller split(). 

import urlib.parse,urllib.request // Du importerar bibliotek för att hämta data från URL:er. Det är så man hämtar data från webben. 

url = input("Enter URL: ") // Frågar efter input. Denna kod kan alltså köras föra vilken hemsida du är skriver in i programmet med förutsättning att det är rätt URL.

html = urllib.request.urlopen(url).read() // Python skickar en HTTP-request, Servern svarar med HTML, .read() hämtar alla bytes. Viktigt att förstå att Internetdata kommer som bytes, inte text.

soup = BeautifulSoup(html,"html.parser") //Den gör tre saker samtidigt: Decodar bytes → 1.text, 2-Parser HTML,3-Bygger en strukturerad modell av dokumentet. Den gör alltså att datan blir strukturerad och enkel att jobba med.

tags = soup("span", class_="comments") // Du säger: “Ge mig bara <span>-taggar som har class="comments". 

tot = 0
count = 0

for tag in tags: // Du går igenom varje <span>-tagg.
    number = int(tag.get_text()) // Hämtar texten: "90" och konverterar om till tal: 90
    tot += number
    count += 1

print("Count", count)
print("Sum", tot)

##################################################
Kunskap	Varför viktigt
HTTP & URL	All web-programmering
Bytes vs text	Kodning / Unicode
HTML-parsing	Web scraping
Filtrering	Data science
Loop + sum	Algoritmiskt tänkande
Robust kod	Korrekt resultat
🏁 VARFÖR DENNA KOD ÄR “BRA”


📌 En mening (perfekt till inlämning)

Programmet hämtar HTML från en URL, parser dokumentet med Beautiful Soup, filtrerar relevanta element och summerar numeriska värden på ett strukturerat och tillförlitligt sätt.


    Vad är <span>?
🔹 <span> är en HTML-tagg

I HTML är <span>: en inline-tagg, den används för att markera små delar av text

har ingen egen betydelse i sig

Exempel:

<p>Antal kommentarer: <span>90</span></p>


Här används <span> för att “peka ut” talet 90.

🔹 Varför används <span> här?

I Py4E-sidan:

<span class="comments">90</span>


Siffran ligger i en egen tagg

Lätt för CSS, JavaScript och scraping att hitta

🧩 Vad betyder class="comments"?
🔹 class är ett HTML-attribut

HTML-taggar kan ha attribut:

<tag attribut="värde">


I detta fall:

<span class="comments">90</span>

class = attribut

"comments" = värde

class används bla till web-scraping

🧠 Hur används detta i Python?

I din kod:

tags = soup("span", class_="comments")

Detta betyder: “Ge mig alla <span>-taggar som har attributet class="comments"”
