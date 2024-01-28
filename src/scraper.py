import requests
from bs4 import BeautifulSoup
import csv

# Open CSV file to write to later
file_name = "features.csv"
f = csv.writer(open(file_name, 'a', newline=''))

# Create variables to store URL and retrieve HTML contents of URL
url = ""
page = requests.get(url)

# Create a BeautifulSoup object to parse HTML
soup = BeautifulSoup(page.content, "html.parser")

# Retrieve each URL link for each repository on the page
project_links = soup.find_all()

# Retrieve the features for each project on the page
for project in project_links:
  # Create variable to retrieve HTML contents of project URL
  project_page = requests.get(project)

  # Create a BeautifulSoup object to parse HTML
  project_soup = BeautifulSoup(project_page.content, "html.parser")

  # Extract all the features needed for data collection
  name_of_feature = project_soup.find()

  # Handling Errors for features that are not found

  # Write to CSV file
  f.writerow([project, feature_one, feature_two, feature_three])

f.close()





