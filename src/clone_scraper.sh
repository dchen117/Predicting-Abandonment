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




done <file.txt
