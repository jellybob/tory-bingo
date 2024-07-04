import requests
from bs4 import BeautifulSoup
import json
import re

# Fetch the Wikipedia page
url = "https://en.wikipedia.org/wiki/Results_of_the_2024_United_Kingdom_general_election_by_constituency"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize the dictionary to hold the data
incumbents = []

# Find all the tables containing the election results
tables = soup.find_all('table', class_='wikitable')

for table in tables:
    rows = table.find_all('tr')
    
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')
        
        if len(cells) < 4:
            continue
        
        # Extract data from the cells
        constituency = cells[0].get_text(strip=True)
        incumbent_mp = re.sub(r'[\[\(].*[\]\)]$', "", cells[-1].get_text(strip=True))
        incumbent_party = cells[-2].get_text(strip=True)
        candidates = [cell.get_text(strip=True) for cell in cells[1:-3]]

        # Check if incumbent MP is in the list of candidates
        resigned = incumbent_mp not in candidates

        if incumbent_party == "Conservative" and resigned is False:
          # Add to dictionary
          incumbents.append({
              "constituency": constituency,
              "candidate": incumbent_mp,
          })

# Convert the dictionary to JSON
json_data = json.dumps(incumbents, indent=4)
print(json_data)

# Save the JSON data to a file
with open('incumbents.json', 'w') as file:
    file.write(json_data)

print("Data saved to incumbents.json")
