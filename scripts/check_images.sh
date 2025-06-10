#!/bin/bash

IFS=$'\n'
error=0

# Use a temporary file to communicate between subshells
temp_error_file=$(mktemp)
trap "rm -f $temp_error_file" EXIT
echo "0" > "$temp_error_file"

find content -name "*.md" | while read -r file; do
    # echo "Checking $file"
    # Extract image paths one at a time using a more precise regex
    grep -o -E '!\[[^]]*\]\([^)]+\)' "$file" | while read -r img_tag; do
        # Extract just the path part from between the parentheses
        img_path=$(echo "$img_tag" | sed -E 's/!\[[^]]*\]\(([^)]+)\)/\1/')
        # Remove any title or size attributes that might be in quotes
        img_path=$(echo "$img_path" | sed -E 's/"[^"]*"//g' | sed -E "s/'[^']*'//g" | xargs)
        
        if [[ "$img_path" == /* ]]; then
            echo "ERROR: $img_path is asbolute path in '$file'"
            echo "1" > "$temp_error_file"
            continue
        fi

        if [[ "$img_path" == https://* ]]; then
            echo "ERROR: $img_path is external URL in '$file'"
            echo "1" > "$temp_error_file"
            continue
        fi

        cd "$(dirname "$file")"

        # echo "Checking image: $img_path"
        if [[ ! -f "$img_path" ]]; then
            echo "1" > "$temp_error_file"
            echo "ERROR: '$img_path' not found in '$file'"
            continue
        fi

        cd - > /dev/null
    done
done

# Read the error status from the temporary file
error=$(cat "$temp_error_file")

if [[ $error -eq 1 ]]; then
    echo "FATAL: One of more checks failed."
    exit 1
else
    echo "All checks passed."
    exit 0
fi