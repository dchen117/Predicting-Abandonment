# Import the python scripts and another libraries
import api_modified as api_m
import html_scraper as html
import pandas as pd
import argparse
from pathlib import Path
import subprocess
import sys

# Adding ArgumentParse object with description
parser = argparse.ArgumentParser(description='Scrapes features from Github projects.')

# Adding command-line arguments --mode, and other required arguments used in every mode
parser.add_argument('mode', choices=['scrape', 'rescrape', 'subscrape'], help='Specify mode for scraping: scrape, rescrape, subscrape.')
parser.add_argument('access_token', help='Github access token for authorization.')
parser.add_argument('export_file', help='Name of excel file that stores the collected features.')

# Parse command-line arguments
args = parser.parse_args()

# Access mode specified 
mode = args.mode
access_token = args.access_token
export_file = args.export_file

# Execute based on mode
if mode == 'scrape':
  # Prompt user to provide star range for scraping
  high = int(input("Please enter an upper limit for the star range you are collecting: ")) 
  low = int(input("Please enter a lower limit for the star range you are collecting: "))


elif mode == 'rescrape':
  # Prompt user for the name of the import file to be used
  import_file = str(input("Please enter the name of the import file containing the list of projects you've collected: ")) 

elif mode == 'subscrape':
  # Prompt user to provide star range for scraping
  high = int(input("Please enter an upper limit for the star range you are collecting: ")) 
  low = int(input("Please enter a lower limit for the star range you are collecting: "))


# Scraping features using html and api scrapers
html.scrape_project('https://github.com/freeCodeCamp/freeCodeCamp')
api_m.scrape_project('https://github.com/freeCodeCamp/freeCodeCamp', access_token)
api_m.collect_sbom('https://github.com/freeCodeCamp/freeCodeCamp', access_token)

# Run the bash script scraper, using subprocess.run()
#command = f"./clone_scraper.sh {import_file_for_list_of_projects} {export_file_for_bash_info}"
#result = subprocess.run(command, shell=True, capture_output=True, text=True)
# Print the output
# print(result.stdout)

# Converting features to pandas dataframe
api_df = api_m.convertToDataFrame()
html_df = html.convertToDataFrame()

# Merging dataframes
df = pd.merge(api_df, html_df, how='outer', on='Project URL')

# Export merged dataframe as Excel file
if Path(export_file).is_file():
    with pd.ExcelWriter(export_file, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
         df.to_excel(writer,sheet_name="Sheet1", startrow=writer.sheets["Sheet1"].max_row, index = False,header= False)
else:
    df.to_excel(export_file, index=False)

