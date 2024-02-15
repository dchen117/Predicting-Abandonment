#!/bin/bash

# Listed below are the headers to be copied to the csv file when needed
# Number of Files,Max Depth of Files,Number of Contributors,Number of Commits,Number of Merge Commits,Number of Branches,Number of Tags,Number of Links,Has README,Has SECURITY,Has CODE_OF_CONDUCT,Has CONTRIBUTING,Has ISSUE_TEMPLATE,Has PULL_REQUEST_TEMPLATE

repo_list=()

# While loop to get all the ssh_links for cloning
while read -r line
do
  repo_list+=("$line")
done < clone_repos.txt


for i in "${repo_list[@]}"; do
  echo "$i"
  git clone "$i"

  # Get directory name based off of SSH clone link
  directory=$(echo "$i" | cut -d '/' -f 2 | rev | cut -c 5- | rev)
  cd $directory

  # Gets all files, including ones in sub-directories
  # Doesn't count anything in the .git directory, as those files are not modified or created by the users directly
  num_files=$(find . -type f 2> /dev/null | grep -vwE ".git" | wc -l | tr -d "[:blank:]")

  # Get the max depth of files
  depth=$(find . -type f | sed 's/[^/]//g' | sort | tail -1 | awk '{ print length }' | tr -d "[:blank:]")
  
  # Number of Contributors, people who have made commits, could be more as remote commits are listed as different people
  num_contributors=$(git shortlog -s -n | wc -l | tr -d "[:blank:]")

  # Number of Commits
  num_commits=$(git log --pretty=oneline | wc -l | tr -d "[:blank:]")

  # Number of Merge Commits, is included in number of commits above
  num_merges=$(git log --pretty=oneline --merges | wc -l | tr -d "[:blank:]")

  # Number of Branches
  num_branches=$(git branch -a | wc -l | tr -d "[:blank:]")

  # Number of tags AKA releases
  num_tags=$(git tag | sort | uniq | wc -l | tr -d "[:blank:]")

  # Number of Links on the README (including images) will be set later
  num_links=0

  # Presence of README and other files
  README=$(find . -name "README.md")
  SECURITY=$(find . -name "SECURITY.md")
  CONDUCT=$(find . -name "CODE_OF_CONDUCT.md")
  CONTRIBUTING=$(find . -name "CONTRIBUTING.md")
  ISSUE_TEMPLATE=$(find . -name "ISSUE_TEMPLATE.md")
  PULL_TEMPLATE=$(find . -name "PULL_REQUEST_TEMPLATE.md")

  # Check if empty
  if [[ -z "$README" ]]; then
    README="NO"
  else
    # Change num_links accordingly if README file is present
    README="YES"
    COUNT_ONE=$(cat README.md | grep -o '(https' | wc -l | tr -d "[:blank:]")
    COUNT_TWO=$(cat README.md | grep -o 'href' | wc -l | tr -d "[:blank:]")
    num_links=$(($COUNT_ONE + $COUNT_TWO))
  fi

  if [[ -z "$SECURITY" ]]; then
    SECURITY="NO"
  else
    SECURITY="YES"
  fi

  if [[ -z "$CONDUCT" ]]; then
    CONDUCT="NO"
  else
    CONDUCT="YES"
  fi

  if [[ -z "$CONTRIBUTING" ]]; then
    CONTRIBUTING="NO"
  else
    CONTRIBUTING="YES"
  fi

  if [[ -z "$ISSUE_TEMPLATE" ]]; then
    ISSUE_TEMPLATE="NO"
  else
    ISSUE_TEMPLATE="YES"
  fi

  if [[ -z "$PULL_TEMPLATE" ]]; then
    PULL_TEMPLATE="NO"
  else
    PULL_TEMPLATE="YES"
  fi

  # List of commits for days
  day_trends=$(git log --date=short --pretty=format:%cd | sort | uniq -c)
  
  # List of commits for months
  month_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1-2 | sort | uniq -c)

  # List of commits for years
  year_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1 | sort | uniq -c)

  # Output data to the csv file
  echo "$num_files,$depth,$num_contributors,$num_commits,$num_merges,$num_branches,$num_tags,$num_links,$README,$SECURITY,$CONDUCT,$CONTRIBUTING,$ISSUE_TEMPLATE,$PULL_TEMPLATE" >> ../clone_data.csv

  # Remove the cloned repository's directory
  cd ..
  echo -e "y\ny\n" | rm -r $directory
done 
