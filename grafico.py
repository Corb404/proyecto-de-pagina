import json
import urllib.request

url = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json"
urllib.request.urlretrieve(url, "data/colombia_departamentos.geojson")

with open("data/colombia_departamentos.geojson", encoding="utf-8") as f:
    geo = json.load(f)

print("Departamentos en el mapa:", len(geo["features"]))
print(geo["features"][0]["properties"])