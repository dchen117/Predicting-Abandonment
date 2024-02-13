#!/bin/bash

# While loop to go through each repository
while read -r line
do
  echo $line
  git clone $line

  # Get directory name based off of SSH clone link
  directory=$(echo "$line" | cut -d '/' -f 2 | cut -d '.' -f 1)
  cd $directory

  # Gets all files, including ones in sub-directories
  # Doesn't count anything in the .git directory, as those files are not modified or created by the users directly
  # num_files=$(find . -type f 2> /dev/null | grep -vwE ".git" | wc -l | tr -d "[:blank:]")

  # Get the max depth of files
  # depth=$(find . -type f | sed 's/[^/]//g' | sort | tail -1 | awk '{ print length }' | tr -d "[:blank:]")
  
  # Number of Contributors, people who have made commits, could be more as remote commits are listed as different people
  # num_contributors=$(git shortlog -s -n | wc -l | tr -d "[:blank:]")

  # Number of Commits
  #num_commits=$(git log --pretty=oneline | wc -l | tr -d "[:blank:]")

  # Number of Merge Commits, is included in number of commits above
  #num_merges=$(git log --pretty=oneline --merges | wc -l | tr -d "[:blank:]")

  # Number of Branches
  #num_branches=$(git branch -a | wc -l | tr -d "[:blank:]")

  # Number of tags AKA releases
  #num_tags=$(git tag | sort | uniq | wc -l | tr -d "[:blank:]")

  # List of commits for days
  #day_trends=$(git log --date=short --pretty=format:%cd | sort | uniq -c)
  
  # List of commits for months
  #month_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1-2 | sort | uniq -c)

  # List of commits for years
  #year_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1 | sort | uniq -c)

  # Output data to the csv file
  #echo "$num_files,$depth,$num_contributors,$num_commits,$num_merges,$num_branches,$num_tags" >> ../clone_data.csv

  # Remove the cloned repository's directory
  cd ..
  echo -e "y\ny\n" | rm -r $directory

done < clone_repos.txt
