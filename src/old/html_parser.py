from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import threading

# Declare the lists for each feature to be scraped
repo_url = []
repo_watches = []
repo_sponsors = []
repo_open_issues = []
repo_closed_issues = []
repo_labels = []
repo_milestones = []
repo_open_prs = []
repo_closed_prs = []

# Headless mode for Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")
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

def scrape_page(project_url):
    current_thread = threading.current_thread()
    thread_name = current_thread.name
    print(f"Code block is running in thread: {thread_name}")

    print(project_url)
    # Add url to list
    repo_url.append(project_url)

    # Set up Web Driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(project_url)

    # Wait for the document to be in 'complete' state
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")


    # Get the OWNER/REPO
    project = project_url[19:]
    print(project)

    # Parse HTML
    # Get number of watches and sponsered?
    num_watches = soup.find(href=f"/{project}/watchers").find("strong").text

    creator = project.split('/')[0]
    sponsored = "Yes" if soup.find(href=f"/sponsors/{creator}") != None else "No"

    repo_watches.append(num_watches)
    repo_sponsors.append(sponsored)


    # Issues
    issue_url = project_url + "/issues"
    driver.get(issue_url)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")

    open_issues = None if soup.find(href=f"/{project}/issues?q=is%3Aopen+is%3Aissue") == None else soup.find(href=f"/{project}/issues?q=is%3Aopen+is%3Aissue").text.split()[0]
    closed_issues = None if soup.find(href=f"/{project}/issues?q=is%3Aissue+is%3Aclosed") == None else soup.find(href=f"/{project}/issues?q=is%3Aissue+is%3Aclosed").text.split()[0]
    num_labels = None if soup.find(href=f"/{project}/labels") == None else soup.find(href=f"/{project}/labels").find("span").text
    num_milestones = None if soup.find(href=f"/{project}/milestones") == None else soup.find(href=f"/{project}/milestones").find("span").text

    repo_open_issues.append(open_issues)
    repo_closed_issues.append(closed_issues)
    repo_labels.append(num_labels)
    repo_milestones.append(num_milestones)


    # Pull Requests
    pull_url = project_url + "/pulls"
    driver.get(pull_url)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")

    open_prs = soup.find(href=f"/{project}/pulls?q=is%3Aopen+is%3Apr").text.split()[0]
    closed_prs = soup.find(href=f"/{project}/pulls?q=is%3Apr+is%3Aclosed").text.split()[0]

    repo_open_prs.append(open_prs)
    repo_closed_prs.append(closed_prs)

    # Clean close the Web Session and window(s)
    driver.quit()

project_list = pd.read_excel('project_5000Up.xlsx')
project_list = project_list['Project URL'].tolist()

for p in project_list[:10]:
    thread = threading.Thread(name=p,target=scrape_page(p))
    thread.start()

projects_df = pd.DataFrame({'Project URL':repo_url, 
                            'Number of Watches':repo_watches,
                            'Sponsored':repo_sponsors,
                            'Open Issues':repo_open_issues,
                            'Closed Issues':repo_closed_issues,
                            'Number of Labels':repo_labels,
                            'Number of Milestones':repo_milestones,
                            'Open Pull Requests':repo_open_prs,
                            'Closed Pull Requests':repo_closed_prs})
projects_df
