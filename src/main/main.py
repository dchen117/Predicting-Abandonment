# Import the python scripts and another libraries
import api_modified as api_m
import html_scraper as html
import pandas as pd
import argparse
from pathlib import Path
import subprocess

# Adding ArgumentParse object with description
parser = argparse.ArgumentParser(description='Scrapes features from Github projects.')

# Adding command-line argument --mode
parser.add_argument('--mode', choices=['scrape', 'rescrape', 'subscrape'], help='Specify mode for scraping: scrape, rescrape, subscrape.')

# Parse command-line arguments
args = parser.parse_args()

# Access mode specified 
mode = args.mode

# Execute based on mode
if mode == 'scrape':
  # Add and retrieve arguments for this mode
  parser.add_argument('access_token', help='Github access token for authorization.')
  parser.add_argument('export_file', help='Name of excel file that stores the collected features.')
  parser.add_argument('import_file', help='Name of excel file with list of projects to be collected. The list should be in the first column of the excel file.')

  # Access arguments
  access_token = args.access_token
  export_file = args.export_file
  import_file = args.import_file

elif mode == 'rescrape':
  # Add and retrieve arguments for this mode
  parser.add_argument('access_token', help='Github access token for authorization.')
  parser.add_argument('export_file', help='Name of excel file that stores the collected features.')
  parser.add_argument('import_file', help='Name of excel file with list of projects to be collected. The list should be in the first column of the excel file.')

  # Access arguments
  access_token = args.access_token
  export_file = args.export_file
  import_file = args.import_file

elif mode == 'subscrape':

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

