from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv

# Open CSV file to write to later
file_name = "test.csv"
f = csv.writer(open(file_name, 'a', newline=''))

# Create variables to store URL and retrieve HTML contents of URL
url = "https://github.com/search?q=project&type=repositories&p=1"
#url = "https://realpython.github.io/fake-jobs/"
session = HTMLSession()
page = session.get(url)

page.html.render()
# Create a BeautifulSoup object to parse HTML
#soup = BeautifulSoup(page.html.html, "html.parser")
#print(soup)
project_links = page.html.find("a")
# Retrieve each URL link for each repository on the page
#project_links = soup.find("a",class_="Link__StyledLink-sc-14289xe-0 bKUZnR")

print(project_links)
# Retrieve the features for each project on the page
for project in project_links:
  # Create variable to retrieve HTML contents of project URL
  project_page = session.get(project)

  # Create a BeautifulSoup object to parse HTML
  project_soup = BeautifulSoup(project_page.html, "html.parser")

  # Extract all the features needed for data collection
  feature = project_soup.find("svg", class_="octicon octicon-star mr-2").find_next_sibling()

  # Handling Errors for features that are not found
 
  # Write to CSV file
  f.writerow([project, feature])

#f.close()






