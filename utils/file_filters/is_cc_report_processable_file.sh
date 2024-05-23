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
REALPATH=$(/usr/bin/realpath "$0")
PATH=$(/usr/bin/dirname "${REALPATH}")
sc1="has_log_extension.sh"
sc2="has_txt_extension.sh"
sc3="has_timestamp.sh"

$(${PATH}/${sc1} ${filename})
r1=$?
$(${PATH}/${sc2} ${filename})
r2=$?
$(${PATH}/${sc3} ${filename})
r3=$?

if [ $r1 -eq 0 ] || [ $r2 -eq 0 ] || [ $r3 -eq 0 ]; then
    exit 0
else
    exit 1
fi
