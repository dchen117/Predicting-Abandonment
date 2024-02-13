#!/bin/bash


repo_list=()

# While loop to get all the ssh_links for cloning
while read -r line
do
  repo_list+=("$line")
done < clone_repos.txt

for i in "${repo_list[@]}"; do
  echo "$i"
done
