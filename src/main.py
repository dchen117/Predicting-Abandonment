import api_modified as api_m
import html_scraper as html
import pandas as pd
import argparse
from pathlib import Path

# Adding ArgumentParse object with description
parser = argparse.ArgumentParser(description='Scrapes features from Github projects.')

# Adding command-line arguments and options
parser.add_argument('access_token', help='Github access token for authorization.')
parser.add_argument('export_file', help='Name of excel file that stores the collected features.')
parser.add_argument('input_file', help='Name of excel file with list of projects to be scraped.')

# Parse command-line arguments
args = parser.parse_args()

# Access arguments
access_token = args.access_token
export_file = args.export_file
input_file = args.input_file

# Scraping features using html and api scrapers
html.scrape_project('https://github.com/freeCodeCamp/freeCodeCamp')
api_m.scrape_project('https://github.com/freeCodeCamp/freeCodeCamp', access_token)
api_m.collect_sbom('https://github.com/freeCodeCamp/freeCodeCamp', access_token)

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

