import requests
from bs4 import BeautifulSoup
import pandas as pd

#Bea
def parse_height(height_str):
    if height_str:
        parts = height_str.split(" ")
        if len(parts) >= 4:
            feet = int(parts[0])
            inches = int(parts[2])
            return f"{feet}'{inches}\""  # format: X'Y"
    return height_str
 

def scrape_fighter_data(url):
    response = requests.get(url)
    wiki_text = response.text
    soup = BeautifulSoup(wiki_text, 'html.parser')

    # Find all tables with the class 'wikitable sortable'
    tables = soup.find_all('table', {'class': 'wikitable sortable'})

    all_fighters_data = []

    # Iterate over each table (each weight class)
    for table in tables:
        # Extract headers
        headers = [header.text.strip() for header in table.find_all('th')]
        
        # Iterate over each row in the table
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                fighter_data = {}
                for i in range(len(cells)):
                    data = cells[i].text.strip()
                    if headers[i] == 'Ht.':  # If the column is 'Height'
                        data = parse_height(data)
                    fighter_data[headers[i]] = data
                all_fighters_data.append(fighter_data)

    return all_fighters_data

# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_current_UFC_fighters'

# Scraping the fighter data
fighter_data = scrape_fighter_data(url)

# Convert to DataFrame
df = pd.DataFrame(fighter_data)
print(df.head())  # Display the first few rows of the DataFrame

# Optionally, print the title of the webpage
#print(soup.title)

