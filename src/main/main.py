# Import the python scripts and another libraries
import api_modified as api_m
import api_scraper as api
import html_scraper as html
import pandas as pd
import argparse
import subprocess
import os
import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

# Adding ArgumentParse object with description
parser = argparse.ArgumentParser(description='Scrapes features from Github projects.')

# Adding command-line arguments --mode, and other required arguments used in every mode
parser.add_argument('mode', choices=['scrape', 'rescrape', 'subscrape'], help='Specify mode for scraping: scrape, rescrape, subscrape.')
parser.add_argument('access_token', help='Github access token for authorization.')

# Parse command-line arguments
args = parser.parse_args()

# Access mode specified 
mode = args.mode
access_token = args.access_token

# Making export file
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_H%H-M%M-S%S")
export_file = "features_" + formatted_datetime + ".xlsx"

# Export merged dataframe as Excel file
def export_to_excel():
  os.makedirs(os.path.dirname(f"features/{export_file}"), exist_ok=True)
  df.to_excel(f"features/{export_file}", index=False)

if mode != 'subscrape':
  # Execute based on mode
  # api_s is the selected version of the api scraper
  if mode == 'scrape':
    # Prompt user to provide star range for scraping
    high = int(prompt("Please enter an upper limit for the star range you are collecting: ")) 
    low = int(prompt("Please enter a lower limit for the star range you are collecting: "))
    api_s = api

  elif mode == 'rescrape':
    # Prompt user for the name of the import file to be used
    import_file = prompt("Please enter the name of the import file containing the list of projects you've collected: ", completer=PathCompleter())
    # Import the list of projects from the import Excel file
    project_list = pd.read_excel(import_file)["Project URL"].tolist()
    api_s = api_m

  # Scraping features using html and api scrapers
  try:
    # Create a file to store the bash data, will be later deleted in order to avoid duplicate data
    export_bash_csv = "clone_data.csv"
    open(export_bash_csv, 'a').close()

    # Run API scraper
    if api_s == api:
      api.get_projects(low, high, access_token)
    else:
      api_m.scrape_project_list(project_list, access_token)    
    api_df = api_s.convertToDataFrame()

    # Retrieve the SSH urls for the bash script
    api_df['Clone SSH URL'].to_csv('clone_urls.txt', header=False, index=False)

    # Run HTML scraper and collect SBOMs
    html.scrape_project_list(api_s.repo_url)
    api_m.collect_sbom_list(api_s.repo_url, access_token)

    # Run the bash script scraper, using subprocess.run()
    command = f"./clone_scraper.sh ./clone_urls.txt {export_bash_csv}"
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
      print(line.decode().rstrip())

    # Wait for subprocess to finish running
    proc.wait()

  except KeyboardInterrupt:
    print("KeyboardInterrupt Detected. Saving results...")
  
  except Exception as e:
    print("Error Detected:", e)
    print("Saving Results...")
  
  finally:
    # Converting features to pandas dataframe
    api_df = api_s.convertToDataFrame()
    html_df = html.convertToDataFrame()
    bash_df = pd.read_csv(export_bash_csv, header=None, names=['Clone SSH URL','Number of Files','Depth of Files','Number of Contributors','Number of Commits','Number of Merges','Number of Branches','Number of Tags','Number of Links','Has README','Has SECURITY','Has Conduct','Has Contributing','Has ISSUE_TEMPLATE','Has PULL_TEMPLATE']) 

    # Merging dataframes
    df = pd.merge(api_df, html_df, how='outer', on='Project URL')
    df = pd.merge(df, bash_df, how='outer', on='Clone SSH URL')

    # Delete the files created by bash script
    os.remove(export_bash_csv)
    if os.path.exists("clone_urls.txt"):
      os.remove("clone_urls.txt")

    # Update excel file with new features
    export_to_excel()

elif mode == 'subscrape':
  # Prompt user to provide star range for scraping
  high = int(prompt("Please enter an upper limit for the star range you are collecting: ")) 
  low = int(prompt("Please enter a lower limit for the star range you are collecting: "))
  
  # Scrape a smaller amount of projects, only a list
  api.get_projects(low, high, access_token)

  # Converting features to pandas dataframe
  api_df = api.convertToDataFrame()
  df = api_df
    
  # export to excel file
  export_to_excel()
