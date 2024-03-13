from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
import sys

# Get command line arguments
if len(sys.argv) != 5:
  print("Usage: [import_file] [export_file] [start_index] [end_index]")
  exit()

# Skip first index which is script name
import_file = str(sys.argv[1])
export_file = str(sys.argv[2])
start_index = int(sys.argv[3])
end_index = int(sys.argv[4])

# Declare list to be used to store projects that failed to collect any information
error_projects = []

# Chrome options to be added
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-renderer-backgrounding")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-client-side-phishing-detection")
chrome_options.add_argument("--disable-crash-reporter")
chrome_options.add_argument("--disable-oopr-debug-crash-dump")
chrome_options.add_argument("--no-crash-upload")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-low-res-tiling")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--silent")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")


# Declare function to scrape the features for each project
def scrape_page(project_url):

    project_features = []

    print(project_url)
    # Add url to list
    project_features.append(project_url)

    # Get the OWNER/REPO
    project = project_url[19:]
    print(project)

    # Set up Web Driver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(project_url)

    # Get number of watches and sponsors
    # Wait for the document to be in 'complete' state
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'body'))
    )

    # Parse HTML
    # Get number of watches and sponsered?
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")

    num_watches = soup.find(href=f"/{project}/watchers").find("strong").text

    creator = project.split('/')[0]
    sponsored = "Yes" if soup.find(href=f"/sponsors/{creator}") != None else "No"

    project_features.append(num_watches)
    project_features.append(sponsored)

    # Issues
    #thread = threading.Thread(name=watch_sponsors,target=issues(project_url, project, driver))
    #thread.start()
    issue_url = project_url + "/issues"
    driver.get(issue_url)

    # Wait for the document to be in 'complete' state
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'body'))
    )

    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")

    open_issues = None if soup.find(href=f"/{project}/issues?q=is%3Aopen+is%3Aissue") == None else soup.find(href=f"/{project}/issues?q=is%3Aopen+is%3Aissue").text.split()[0]
    closed_issues = None if soup.find(href=f"/{project}/issues?q=is%3Aissue+is%3Aclosed") == None else soup.find(href=f"/{project}/issues?q=is%3Aissue+is%3Aclosed").text.split()[0]
    num_labels = None if soup.find(href=f"/{project}/labels") == None else soup.find(href=f"/{project}/labels").find("span").text
    num_milestones = None if soup.find(href=f"/{project}/milestones") == None else soup.find(href=f"/{project}/milestones").find("span").text


    project_features.append(open_issues)
    project_features.append(closed_issues)
    project_features.append(num_labels)
    project_features.append(num_milestones)

    print(f"Project:{project_url}, Open issues: {open_issues}, Closed issues: {closed_issues}")

    # Pull Requests
    pull_url = project_url + "/pulls"
    driver.get(pull_url)

    # Wait for the document to be in 'complete' state
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'footer'))
    )

    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")

    #print(f"Getting prs: {project}")
    #open_prs = soup.find(href=f"/{project}/pulls?q=is%3Aopen+is%3Apr")
    #if open_prs != None:
     #   open_prs = open_prs.text.split()[0]
    #else:
     #   count = 0
      #  while count < 4 and open_prs == None:
       #     driver.get(pull_url)
        #    # Wait for the document to be in 'complete' state
         #   WebDriverWait(driver, 10).until(
         #       EC.visibility_of_element_located((By.TAG_NAME, 'body'))
          #  )
          #  html = driver.page_source
           # soup = BeautifulSoup(html, "html.parser")
           # open_prs = soup.find(href=f"/{project}/pulls?q=is%3Aopen+is%3Apr")
           # count += 1
       # if open_prs == None:
       #     return [None, project_url]
       # else:
        #    open_prs = open_prs.text.split()[0]
    #closed_prs = soup.find(href=f"/{project}/pulls?q=is%3Apr+is%3Aclosed").text.split()[0]

    #print(f"Getting prs: {project} Open={open_prs} Closed={closed_prs}")

    #project_features.append(open_prs)
    #project_features.append(closed_prs)

    # Number of Workflow Runs
    workflow_url = project_url + "/actions"
    driver.get(workflow_url)

    # Wait for the document to be in 'complete' state
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'footer'))
    )

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    workflow = soup.find(lambda tag: tag.name == 'strong' and 'workflow runs' in tag.get_text())
    if workflow != None:
        workflow = workflow.text.split()[0]
    print(f"workflow: {workflow}")

    project_features.append(workflow)

    # Number of Dependent Repos
    dependent_url = project_url + "/network/dependents"
    driver.get(dependent_url)

    # Wait for the document to be in 'complete' state
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'footer'))
    )

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    dependents = soup.find('a', class_='btn-link selected')
    if dependents != None:
        dependents = dependents.text.split()[0]

    print(f"dependents: {dependents}")

    project_features.append(dependents)

    # Verified Repo Owner
    owner_url = f"https://github.com/{creator}"
    print(owner_url)
    driver.get(owner_url)

    # Wait for the document to be in 'complete' state
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'footer'))
    )

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    verified = soup.find('summary', {'title': 'Label: Verified'})
    if verified != None:
        verified = verified.text.split()[0]

    print(verified)
    project_features.append(verified)

    # Number of Owner Followers
    #followers = soup.find('a', class_='Link--secondary no-underline no-wrap')
    #if followers != None:
      #  followers = followers.text.split()[0]
   # else:
      #  count = 0
       # while count < 4 and followers == None:
        #    driver.get(owner_url)
         #   # Wait for the document to be in 'complete' state
          #  WebDriverWait(driver, 10).until(
           #     EC.visibility_of_element_located((By.TAG_NAME, 'body'))
            #)
           # html = driver.page_source
           # soup = BeautifulSoup(html, "html.parser")
           # followers = soup.find('a', class_='Link--secondary no-underline no-wrap')
           # count += 1
        #if followers == None:
       #     return [None, project_url]
        #else:
         #   followers = followers.text.split()[0]
    #print(f"followers: {followers}")

    #project_features.append(followers)

    # Clean close the Web Session and window(s)
    driver.quit()

    return project_features


# RUNNING CODE
# Read in the excel file consisting of projects to scrape
project_list = pd.read_excel(import_file)
project_list = project_list['Project URL'].tolist()
project_list = project_list[start_index:end_index]


# Create list to store features scraped and execute the function above to scrape the features
projects = []
low = 0
high = 10
with ThreadPoolExecutor(max_workers=10) as p:
    while high <= len(project_list):
        features = p.map(scrape_page, project_list[low:high])
        print(high)
        for f in features:
            if f[0] != None:
                projects.append(f)
            else:
                error_projects.append(f[1])

        low += 10
        high += 10
        time.sleep(2)

# Create pandas DataFrame to store the data
projects_df = pd.DataFrame(projects, columns=['Project URL',
                                              'Number of Watches',
                                              'Sponsored',
                                              'Open Issues',
                                              'Closed Issues',
                                              'Number of Labels',
                                              'Number of Milestones',
                                              #'Open Pull Requests',
                                              #'Closed Pull Requests',
                                              'Number of Workflow Runs',
                                              'Number of Dependents',
                                              'Verified Owner',
                                              #'Followers of Owner'
                                             ])
# For printing data frame
# projects_df


# Export to excel file
# try: with pd.ExcelWriter(export_file, mode="a", engine="openpyxl", if_sheet_exists="overlay", ) as writer: projects_df.to_excel(writer,sheet_name="Sheet1", startrow=writer.sheets["Sheet1"].max_row, index = False,header= False) except FileNotFoundError: projects_df.to_excel(export_file, index=False)
