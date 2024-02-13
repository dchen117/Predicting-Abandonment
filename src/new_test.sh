#!/bin/bash

while read -r line
do
  echo $line
done < clone_repos.txt
