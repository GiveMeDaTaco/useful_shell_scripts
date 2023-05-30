#!/bin/bash

# Concatenate repositories from sources.list
echo "Repositories from /etc/apt/sources.list:"
echo "---------------------------------------"
cat /etc/apt/sources.list

# Concatenate repositories from files in sources.list.d
echo
echo "Repositories from /etc/apt/sources.list.d/:"
echo "-------------------------------------------"
for file in /etc/apt/sources.list.d/*.list; do
  echo "File: $file"
  echo "----------------------"
  cat "$file"
  echo
done

