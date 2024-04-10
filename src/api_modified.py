import requests
from requests.auth import HTTPBasicAuth 
import pandas as pd
import time
import os
import math
import sys

# Get the command line arguments
if len(sys.argv) != 4:
  print("Usage: [export_file] [projects_file] [access_token]")
  exit()

export_file = str(sys.argv[1])
projects_file = str(sys.argv[2])
access_token = str(sys.argv[3])

# Import the project data from the Excel file
project_list = pd.read_excel(f"{projects_file}").iloc[:, 0].tolist()

# Initialize the lists to store the information for each repo
repo_url= []
repo_stars = []
repo_wiki = []
repo_open_issues = []
repo_forks = []
repo_last_update = []
repo_size = []
repo_created_date = []
repo_last_push = []
repo_language = []
repo_discussions = []
repo_pages = []
repo_license = []
repo_archived = []
repo_projects = []
repo_homepage = []
repo_org = []
repo_topics = []
repo_ssh_url = []
repo_watches = []

def get_github_repo_info(project):
    api_url = f"https://api.github.com/repos/{project}"

    headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(api_url, headers=headers)

    if response.status_code == 404:
        return None

    while response.status_code != 200:
        print(f"Request failed")
        print(response.status_code)
        response_check = requests.get("https://api.github.com", headers=headers)
        if response_check.status_code == 403:
            delay_seconds = 60  # default delay
            time.sleep(delay_seconds)
            response = requests.get(api_url, headers=headers)
        else:
            return None
    
    if response.status_code == 200:
        repo_info = response.json()
        
        # Extract and print relevant information
        repo_url.append(repo_info.get("html_url", "URL not found"))
        repo_stars.append(repo_info.get("stargazers_count", "Stargazers count not found"))
        repo_wiki.append(repo_info.get("has_wiki", "Wiki not found"))
        repo_open_issues.append(repo_info.get("open_issues_count", "Open issues count not found"))
        repo_forks.append(repo_info.get("forks_count", "Forks count not found"))
        repo_last_update.append(repo_info.get("updated_at", "Last update not found"))
        repo_size.append(repo_info.get("size", "size not found"))
        repo_created_date.append(repo_info.get("created_at", "Created date not found"))
        repo_last_push.append(repo_info.get("pushed_at", "Last push not found"))
        repo_language.append(repo_info.get("language", "Language not found"))
        repo_discussions.append(repo_info.get("has_discussions", "Discussions not found"))
        repo_pages.append(repo_info.get("has_pages", "Pages not found"))
        repo_archived.append(repo_info.get("archived", "Archived not found"))
        repo_projects.append(repo_info.get("has_projects", "Projects not found"))
        repo_topics.append(len(repo_info.get("topics", "No Topics")))
        repo_ssh_url.append(repo_info.get("ssh_url", "Projects not found"))
        repo_org.append(repo_info['owner'].get("type", "No type"))
        
        # Conditional statements are to avoid possible errors
        license = repo_info.get("license", "None")
        if license == "None" or license is None:
            repo_license.append("None")
        else:
            repo_license.append(license["spdx_id"])
            
            
        homepage = repo_info.get("homepage", "No Homepage")
        if homepage is None or len(homepage) == 0:
           repo_homepage.append("None")
        else:
            repo_homepage.append(homepage)      
            
        
    else:
        # If the request was not successful, print an error message
        print("Error:", response.status_code)
        print("Response:", response.text)

for project in project_list:
    print(project)
    project = project[19:]
    get_github_repo_info(project)

projects_df = pd.DataFrame({'Project URL':repo_url,
                            'Clone SSH URL':repo_ssh_url,
                            'Organization':repo_org,
                            'Homepage':repo_homepage,
                            'Last Update':repo_last_update, 
                            'Last Push':repo_last_push,
                            'Created Date':repo_created_date,
                            'Archived':repo_archived,
                            'Size':repo_size, 
                            'Number of Stars':repo_stars, 
                            'Number of Watches':repo_watches,
                            'Number of Open Issues':repo_open_issues, 
                            'Number of forks':repo_forks, 
                            'Has a Wiki':repo_wiki,
                            'Has Discussions':repo_discussions,
                            'Has Projects':repo_projects,
                            'Has Pages':repo_pages,
                            'License':repo_license,
                            'Language':repo_language,
                            'Topics': repo_topics})

# Export to Excel
# CHANGE THE EXPORTED FILE NAME ACCORDINGLY
try:
    with pd.ExcelWriter(
        export_file,
        mode="a",
        engine="openpyxl",
        if_sheet_exists="overlay",
    ) as writer:
         projects_df.to_excel(writer,sheet_name="Sheet1", startrow=writer.sheets["Sheet1"].max_row, index = False,header= False)
except FileNotFoundError:
    projects_df.to_excel(export_file, index=False)
