import json // Importerar Python-modulen json, som används för att läsa och tolka JSON-data.
data = 
[
{ "id" : "001",
"x" : "2",
"name" : "Chuck"
} ,
{ "id" : "009",
"x" : "7",
"name" : "Brent"
}
]
############## 🔹 Skapar en sträng som innehåller JSON-data.
🔹 JSON-datan består av en lista ([ ]) med två objekt (dictionary-objekt) ({ }).
🔹 Varje objekt representerar en användare med:

"id" → användarens ID

"x" → ett attribut (värde som text)

"name" → användarens namn ###############

info = json.loads(data) #######
🔹 json.loads() översätter JSON-strängen till ett Python-objekt.
🔹 Resultatet blir en lista av dictionaries (ordböcker).
🔹 Variabeln info innehåller nu datan i ett format som Python kan arbeta med. 
######################

print(User count:, len(info)) // 🔹 len(info) räknar hur många objekt som finns i listan. 🔹 Skriver ut hur många användare som finns i datan. 
for item in info: // 🔹 Startar en loop som går igenom varje användare i listan info. 🔹 item blir en dictionary som innehåller data för en användare åt gången. 
print(Name, item[name]) // 🔹 Hämtar värdet för nyckeln "name" från dictionaryn. 🔹 Skriver ut användarens namn.
164
print(Id, item[id])
CHAPTER 13. USING WEB SERVICES
print(Attribute, item[x])
