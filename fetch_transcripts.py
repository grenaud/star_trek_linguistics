import requests
from bs4 import BeautifulSoup
import os
import re
import time

# Define the base URL
base_url = "http://www.chakoteya.net/"

# Define the series list
series_list = ["StarTrek", "NextGen", "DS9", "Voyager", "Enterprise", "STDisco17", "StarTrekPIC"]

# Iterate over each series
for series in series_list:
    print(f"\nProcessing {series}...")

    # Open the list file and read the lines
    with open(f"{series}/list.txt", 'r') as f:
        lines = f.readlines()

    # Initialize season number
    season_number = 1

    # Iterate over each line
    for line in lines:
        line = line.strip()

        # If this line indicates a season, update the season number
        if line.startswith("Episode"):
            continue
        
        if line.startswith("Season"):
            season_number = line.split(" ")[1]
            continue

        # Split the line into fields
        fields = line.split('\t')
        if len(fields) >= 3:
            episode_name = fields[0]
            production_numbers = fields[1]
            airdate = fields[2]

            # Handle multiple production numbers separated by '+', '&', etc.
            production_numbers = [num.strip() for num in re.split('[+&]', production_numbers)]

            # Fetch and save the transcript for each production number
            for production_number in production_numbers:
                # Define the transcript file path
                transcript_file_path = f"{series}/Season {season_number}/{production_number}.txt"

                # If the transcript file already exists, skip this episode
                if os.path.exists(transcript_file_path):
                    print(f"Transcript for {series}, Season {season_number}, Episode {production_number} already exists. Skipping...")
                    continue

                # Get the transcript page
                transcript_page_url = f"{base_url}{series}/{production_number}.html"
                print(f"Fetching transcript from {transcript_page_url}...")
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
                }
                response = requests.get(transcript_page_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the transcript text
                transcript_text = soup.get_text()

                # Save the transcript text to a file
                os.makedirs(os.path.dirname(transcript_file_path), exist_ok=True)
                with open(transcript_file_path, 'w') as f:
                    f.write(transcript_text)

                time.sleep(5)  # 5-second timeout between requests

    print(f"\nFinished processing {series}.")
