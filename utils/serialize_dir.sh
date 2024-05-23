#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ] && [ "$#" -ne 3 ]; then
    echo "Usage: $0 <directory_to_process> <output_file> [filter]"
    exit 1
fi

file_filter_folder="file_filters"
PATH=$(dirname "$(realpath "$0")")
# Assign arguments to variables
start_directory=$1
output_file=$2
filter=$3

# Empty the output file if it exists
> "$output_file"

# Function to process directories and files
process_directory() {
    local dir_path=$1

    # Add directory start label
    echo "<dir: $dir_path>" >> "$output_file"

    # Find all files and directories in the current directory
    for item in "$dir_path"/*; do
        if [ -d "$item" ]; then
            # Recursively process directories
            process_directory "$item"
        elif [ -f "$item" ]; then
            # execute filter script and check return value is 0
            if [ -n "$filter" ]; then
                # echo "${PATH}/${file_filter_folder}/${filter}" "$item"
                $("${PATH}/${file_filter_folder}/${filter}" "$item")
                if [ $? -ne 0 ]; then
                    # echo "Skipping file: $item"
                    continue
                fi
            fi
            # echo "Processing file: $item"
            # Add file start label
            echo "" >> "$output_file"
            echo "<file: $item>" >> "$output_file"
            # Append file content
            /usr/bin/cat "$item" >> "$output_file"
            # Add file end label
            echo "" >> "$output_file"
            echo "</file: $item>" >> "$output_file"
        fi
    done

    # Add directory end label
    echo "</dir: $dir_path>" >> "$output_file"
}

# Start processing from the specified directory
process_directory "$start_directory"

echo "Processing completed. Output saved to $output_file"

