import xml.etree.ElementTree as ET // Här importeras biblioteket xml.etree.ElementTree, som används för att arbeta med XML-data i Python. Förkortningen ET gör koden kortare och mer lättläst.

data = '''
<person> // Ett rot-element: <person>
<name>Chuck</name> // Ett namn: <name>
<phone type="intl"> // Ett telefonnummer med ett attribut (type="intl")
+1 734 303 4456
</phone>
<email hide="yes" /> // Ett e-post-element med attributet hide="yes"
</person> '''



tree = ET.fromstring(data) // Denna rad omvandlar XML-strängen till ett ElementTree-objekt, vilket gör det möjligt att navigera i XML-strukturen som ett träd.
print("Name:", tree.find("name").text) // find("name") letar upp <name>-elementet .text hämtar texten inuti elementet Resultatet blir: Name: Chuck.  
print("Nr:" , tree.find("phone").get("type")) // find("phone") hittar <phone>-elementet .get("type") hämtar värdet på attributet type Resultatet blir: Nr: intl

