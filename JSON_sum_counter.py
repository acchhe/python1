import urllib.parse, urllib.request
import json

url = input("Enter URL: ")

data = urllib.request.urlopen(url).read().decode()

info = json.loads(data)

count = 0
sum = 0

for item in info["comments"]:
   count += 1
   sum = item["count"] + sum

print("characters retrieved:",len(info))
print("count",count)
print("sum:",sum)
