#!/bin/bash
if [ -z "$1" ]; then
  exit 1
fi

/usr/bin/file --mime-type -b "$1" | /usr/bin/grep -v "executable" > /dev/null
exit $?
