import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Define the base URL
base_url = "http://www.chakoteya.net/"

# Define the series list
series_list = ["StarTrek", "NextGen", "DS9", "Voyager", "Enterprise", "STDisco17", "StarTrekPIC"]

# Iterate over each series
for series in series_list:
    outputfile = str(series)+"/list.txt"
    
    print(f"\nProcessing {series}, printing to {outputfile}...")

    
    # Create a directory for the series if it doesn't exist
    if not os.path.exists(series):
        os.makedirs(series)

    if os.path.exists(outputfile):        
        continue;

    # Get the episodes page
    episodes_page_url = f"{base_url}{series}/episodes.htm"
    if series == "Voyager":
        episodes_page_url = f"{base_url}{series}/episode_listing.htm"
    if series == "STDisco17" or series == "StarTrekPIC":
        episodes_page_url = f"{base_url}{series}/episodes.html"
    
    print(f"Fetching episodes list from {episodes_page_url}...")
    
    # Modify the get request to include a user-agent and increase timeout
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    }
    response = requests.get(episodes_page_url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the production numbers, episode names and air dates
    print("Parsing episode information...")
    episodes_data = []
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) == 3:  # assuming the format is consistent
            episode_name = tds[0].text.strip()
            production_number = tds[1].text.strip()
            airdate = tds[2].text.strip()
            episodes_data.append([episode_name, production_number, airdate])

    # Convert to a DataFrame for a tabular structure
    df = pd.DataFrame(episodes_data, columns=['Episode Name', 'Production Number', 'Airdate'])

    # Save the DataFrame to a .txt file in the series directory
    df.to_csv(outputfile, sep="\t", index=False)

    print(f"Saved episode information for {series} to {series}/list.txt")

    time.sleep(5)  # 5-second timeout between requests
