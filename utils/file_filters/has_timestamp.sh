#!/bin/bash

# Check if a file is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"

# Check if the file exists
if [ ! -f "$1" ]; then
    echo "File not found!"
    exit 1
fi

# Regular expression patterns for different timestamp formats
patterns=(
    # ISO 8601 format
    '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?Z'
    # YYYY-MM-DD HH:MM:SS format
    '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
    # YYYY/MM/DD HH:MM:SS format
    '[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
    # MM/DD/YYYY HH:MM:SS AM/PM format
    '[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} (AM|PM)'
)

# Full path to grep
GREP="/bin/grep"  # Change this to the full path to grep if different

# Loop through each pattern and check the file
for pattern in "${patterns[@]}"; do
    if $GREP -qE "$pattern" "$filename"; then
        # echo "Timestamp found in the file."
        exit 0
    fi
done

# If no pattern matches, return 1
# echo "No timestamp found in the file."
exit 1
