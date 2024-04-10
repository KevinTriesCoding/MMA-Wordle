import requests as r
from bs4 import BeautifulSoup
import pandas as pd
import re

response = r.get("https://en.wikipedia.org/wiki/List_of_current_UFC_fighters")

wiki_text = response.text

soup = BeautifulSoup(wiki_text, 'html.parser')

# List of identifiers for each weight class
weight_classes = [
    'Women\'s_strawweights_(115_lb,_52_kg)',  # Women's Division
    'Flyweights_(125_lb,_56_kg)',    # Men's and Women's Division
    'Bantamweights_(135_lb,_61_kg)', # Men's and Women's Division
    'Featherweights_(145_lb,_65_kg)',# Men's and Women's Division
    'Lightweights_(155_lb,_70_kg)',  # Men's Division
    'Welterweights_(170_lb,_77_kg)', # Men's Division
    'Middleweights_(185_lb,_84_kg)', # Men's Division
    'Light_heavyweights_(205_lb,_93_kg)', # Men's Division
    'Heavyweights_(265lb,_120_kg)', # Men's Division
    'Women\'s_flyweights_(125_lb,_56_kg)',  # Women's Division
    'Women\'s_bantamweights_(135_lb,_61_kg)', # Women's Division
    'Women\'s_featherweights_(145_lb,_65_kg)' # Women's Division
]

all_divisions_data = {}

for weight_class in weight_classes:
    header = soup.find('span', {'id': weight_class})
    if header:
        table = header.find_next('table')
        division_data = []

        for row in table.find_all('tr'):
            cleaned_row = [cell.get_text().strip().replace("\n", " ") for cell in row.find_all(['th', 'td'])]
            cleaned_row = [re.sub(' +', ' ', cell) for cell in cleaned_row]
            division_data.append(cleaned_row)

        all_divisions_data[weight_class] = division_data
        #print(all_divisions_data)
    else:
        print(f"{weight_class} division not found")

cleaned_data = {}

for division, rows in all_divisions_data.items():
    cleaned_rows = []
    for row in rows:
        cleaned_row = [cell.replace("\xa0", " ").strip() for cell in row]
        cleaned_rows.append(cleaned_row)
    cleaned_data[division] = cleaned_rows


print (cleaned_data)

for division, rows in cleaned_data.items():
    df = pd.DataFrame(rows[1:], columns=rows[0]) #this will exclude header row from data, and instead use it for the column names
    csv_filename = f"{division.replace("_", " ").title()}.csv"
    df.to_csv(csv_filename, index = False)
    print(f"Exported {division} to {csv_filename}")
























# # Find the 'h3' tag that contains the weight division name
# light_heavyweight_header = soup.find('span', {'id': 'Light_heavyweights_(205_lb,_93_kg)'})
# if light_heavyweight_header:
#     # The table we want is right after the 'h3' tag
#     required_table = light_heavyweight_header.find_next('table')
#     cleaned_table = required_table.strip()
#     print(cleaned_table.text)
# else:
#     print("Light heavyweight division not found")
































#table_soup = soup.find_all('table')
#filtered_table_soup = [table for table in table_soup if table.caption is not None]

#required_table = None

#for table in filtered_table_soup:
    #if str(table.caption.string).strip() == "Light heavyweights":
        #required_table = table
        #break

#print(required_table)

#header_tags = r