import urllib.request, urllib.parse, urllib.error

handle = urllib.request.urlopen("https://data.pr4e.org/intro-short.txt")

for line in handle:
    print(line.decode().rstrip())
