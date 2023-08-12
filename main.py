import csv
import json
import datetime
import requests
from bs4 import BeautifulSoup


url = "https://transitapp.com/region"

response = requests.get(url)
response.raise_for_status()

bs = BeautifulSoup(response.content, features="html.parser")
parsed = json.loads(
    bs.find_all("section", attrs={"data-regions": True})[0]["data-regions"]
)

slugs = {}
for country, regions in parsed.items():
    for region_data in regions:
        slug = region_data["slug"]
        slugs[slug] = {
            "country": country,
            "region": region_data["region"],
            "slug": slug,
        }

with open("data.csv") as f:
    reader = csv.DictReader(f)
    data = [r for r in reader]

existing_slugs = [e["slug"] for e in data]

for slug in [s for s in slugs if s not in existing_slugs]:
    row = slugs[slug]
    row["first_datetime"] = (
        datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    )
    data.append(row)

with open("data.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
