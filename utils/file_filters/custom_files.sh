#!/bin/bash

# File name to check (passed as the first argument to the script)
file_name="$1"

# Define patterns
pattern1="^.*JOB.*_FAILED_.*\.txt$"
pattern2="^.*cmon\.log$"

# Check if the file name matches either of the patterns using grep
echo "$file_name" | /usr/bin/grep -E "$pattern1" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    exit 0
fi
echo "$file_name" | /usr/bin/grep -E "$pattern2" > /dev/null 2>&1
exit $?
