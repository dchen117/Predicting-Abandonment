import requests
from requests.auth import HTTPBasicAuth 
import pandas as pd
import time
import os
import math
import datetime

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

# Directory name for storing sbom files
current_dir = os.getcwd()
date = datetime.date.today()
sbom_dir_name = f"sbom_{date}"
sbom_dir_path = f"{current_dir}/{sbom_dir_name}"
	
def collect_sbom(project_url, access_token):
    if not os.path.exists(sbom_dir_name): 
        os.makedirs(sbom_dir_name)

    owner_repo = project_url[19:]
    sbom_url = f"https://api.github.com/repos/{owner_repo}/dependency-graph/sbom"

    # File name for repo's sbom
    file_name = owner_repo.split('/')
    file_name = f"{file_name[0]}_{file_name[1]}_sbom.json"
    print(file_name)

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {access_token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    # Getting sbom and storing it in sbom directory
    response = requests.get(sbom_url, headers=headers)
    if response.status_code == 200:
        with open(f"{sbom_dir_path}/{file_name}", "wb") as file:
            file.write(response.content)
        print(f"{project_url}: SBOM downloaded")
    else:
        print(f"{project_url}: SBOM download failed")



def scrape_project(project_url, access_token):
    project = project_url[19:]
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
        repo_watches.append(repo_info.get("subscribers_count", "Watches not found"))
        
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


def scrape_project_list(project_list):
    for project_url in project_list:
        print(project_url)
        scrape_project(project_url)

def convertToDataFrame():
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
    return projects_df
