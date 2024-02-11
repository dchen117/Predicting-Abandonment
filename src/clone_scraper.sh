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

  # Get top programming language used
  top_lang=$(cloc . | sed -n 5p | cut -d ' ' -f 1)

  # Number of Contributors, people who have made commits, could be more as remote commits are listed as different people
  num_contributors=$(git shortlog -s -n | wc -l)

  # Number of Commits
  num_commits=$(git log --pretty=oneline | wc -l)

  # Number of Merge Commits, is included in number of commits above
  num_merges=$(git log --pretty=oneline --merges | wc -l)

  # Number of Branches
  num_branches=$(git branch -a | wc -l)

  # Number of tags AKA releases
  num_tags=$(git tag | sort | uniq | wc -l)

  # List of commits for days
  day_trends=$(git log --date=short --pretty=format:%cd | sort | uniq -c)

  # List of commits for months
  month_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1-2 | sort | uniq -c)

  # List of commits for years
  year_trends=$(git log --date=short --pretty=format:%cd | cut -d '-' -f 1 | sort | uniq -c)

done <file.txt
