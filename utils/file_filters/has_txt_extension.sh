#!/bin/bash
if [ -z "$1" ]; then
  exit 1
fi

extension="${1##*.}"
if [ "$extension" == "txt" ]; then
  exit 0
else
  exit 1
fi

