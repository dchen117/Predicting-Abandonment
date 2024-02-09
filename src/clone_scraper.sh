#!/bin/bash


# While loop to go through each repository
while read -r line; do
  git clone $line

  # Get directory name based off of SSH clone link
  directory=$(echo "$line" | cut -d ':' -f 2 | cut -d '.' -f 1)
  cd $directory

  # Gets all files, including ones in sub-directories
  # Doesn't count anything in the .git directory, as those files are not modified or created by the users directly
  num_files=$(find . -type f 2> /dev/null | grep -vwE ".git" | wc -l)


  # Get the max depth of files
  depth=$(find . -type f | sed 's/[^/]//g' | sort | tail -1)

  # Get number of different types of file

  # Number of Commits
  num_commits=$(git log --pretty=oneline | wc -l)

  # Number of Branches
  num_branches=$(git branch -a | wc -l)


  # List of commits for days
  day_trends=$(git log --date=short --pretty=format:%cd | sort | uniq -c)

  # List of commits for months
  month_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1-2 | sort | uniq -c)

  # List of commits for years
  year_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1 | sort | uniq -c)

done <file.txt
