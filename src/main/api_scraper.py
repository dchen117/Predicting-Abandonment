import requests
from requests.auth import HTTPBasicAuth 
import pandas as pd
import time
import os
import math
import datetime
import subprocess
import sys

# Declare lists to store feature data
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

# Function used to scrape the data using the Github API
def get_github_repo_info(search_filter, page_number, access_token):
    api_url = f"https://api.github.com/search/repositories?q="+str(search_filter)+"&page="+str(page_number)+"&per_page=100"

    headers = {
    "Authorization": "Bearer " + access_token,
    "Accept": "application/vnd.github.v3+json"
    }

    # Get number of repos to be used to determine number of pages in the calling cell below
    num_repos = 0

    response = requests.get(api_url, headers=headers)

    while response.status_code != 200:
        print(f"Request failed on page {page_number}")
        delay_seconds = 60  # default delay
        time.sleep(delay_seconds)
        response = requests.get(api_url, headers=headers)

    #response = requests.get(api_url)
    if response.status_code == 200:
        # Parse the JSON response
        repo_list = response.json()['items']
        num_repos = response.json()['total_count']

        for repo_info in repo_list:

            # Extract and print relevant information
            repo_url.append(repo_info.get("html_url", "URL not found"))
            repo_stars.append(repo_info.get("stargazers_count", "Stargazers count not found"))
            #repo_watches.append(repo_info.get("subscribers_count", "Watchers count not found"))
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

    return num_repos



# Function used to facilitate scraping by changing search filters for number of stars, and some of them created date
def get_projects(low, high):
    # Variable for determining range of projects
    decrement = 500
    # While loop to go through each range from low to high
    while high > low:
        # Change ranges accordingly to get <1000 projects
        if high == 400000:
            decrement = 375000
        elif high == 25000:
            decrement = 5000
        elif high == 15000:
            decrement = 500
        elif high == 5000:
            decrement = 100
        elif high == 3000 or high == 1000:
            decrement = 10
        elif high == 680:
            decrement = 5
        elif high == 500:
            decrement = 1

        if (high-decrement) < low:
          decrememt = high - low

        # Search URL just in case => q=stars%3A120..120+created%3A2021-01-01..2021-12-31&

        # Add the 'created:' parameter for <178 stars
        if high <= 179:
            decrement = 1
            # Value of 9 goes down to year 2016
            for i in range(9):
                year = 2024 - i
                created_date = "+created%3A" + str(year) + "-01-01.." + str(year) + "-12-31"
                print(high-decrement, high-1, year, 1)
                return_value = get_github_repo_info("stars%3A"+str(high-decrement)+'..'+str(high-1)+created_date, 1, project_set)
                # For loop to run function to get features
                for page_number in range(2,math.ceil(return_value/100)+1):
                    print(high-decrement, high-1, page_number)
                    return_value = get_github_repo_info("stars%3A"+str(high-decrement)+'..'+str(high-1)+created_date, page_number, project_set)
            # One more request for all projects <=2015
            created_date = "+created%3A<=2015-12-31"
            print(high-decrement, high-1, 2015, 1)
            return_value = get_github_repo_info("stars%3A"+str(high-decrement)+'..'+str(high-1)+created_date, 1, project_set)
            for page_number in range(2,math.ceil(return_value/100)+1):
                print(high-decrement, high-1, 2015, page_number)
                return_value = get_github_repo_info("stars%3A"+str(high-decrement)+'..'+str(high-1)+created_date, page_number, project_set)
        else:
            print(high-decrement, high-1, 1)
            return_value = get_github_repo_info("stars%3A"+str(high-decrement)+'..'+str(high-1), 1, project_set)
            for page_number in range(2,math.ceil(return_value/100)+1):
                # For loop to run function to get features
                print(high-decrement, high-1, page_number)
                return_value = get_github_repo_info("stars%3A"+str(high-decrement)+'..'+str(high-1), page_number, project_set)
        high -= decrement
