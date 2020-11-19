mport pandas
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

URL = "http://insideairbnb.com/get-the-data.html"

# Get raw data
r = requests.get(URL)
p = r.content
s = BeautifulSoup(p)

# Parse raw data
cities = s.find_all("h2")

records = []

for city in cities:
    table = city.find_next_sibling("table")
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        link = row.find("a")
        values = [col.text for col in cols]
        if len(values) == 4:
            allowed_values = ["listings.csv.gz", "calendar.csv.gz"]
            if values[2] in  allowed_values:
                o = OrderedDict()
                o["city"] = city
                o["scraped_at"] = values[0]
                o["city"] = values[1]
                o["file"] = values[2]
                o["url"] = link["href"]
                o["country_from_url"] = link["href"].split("/")[3]
                o["region_from_url"] = link["href"].split("/")[4]
                o["city_from_url"] = link["href"].split("/")[5]
                records.append(o)
                
# Final cleanup
metadata = pandas.DataFrame(records)
m = metadata.drop_duplicates()
m["scraped_at_cleaned"] = pandas.to_datetime(m["scraped_at"])
m = m.sort_values(["city", "scraped_at"])

# Building a unique file name
#m["file_name"] = m["city"].map(lambda x: x.lower()) + "-" + m["file"].map(lambda x: x.split(".")[0]) + "-" + m["scraped_at_cleaned"].astype(str)
m["file_name"] = m["country_from_url"] + " _ " + m["region_from_url"] + " _ " + m["city_from_url"] + " _ " + m["scraped_at_cleaned"].astype(str) + "_" + m["file"]

# Write recipe outputs
listing_metadata = dataiku.Dataset("listing_metadata")
listing_metadata.write_with_schema( m )
