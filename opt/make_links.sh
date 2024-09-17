#!/bin/sh -e

make_links() {
    for file in scripts/*; do
        if test -x "$file" && test ! -L "$1/$(basename "$file")"; then
            ln -s "$file" "$1/$(basename "$file")"
        fi
    done
}

# Define a space-separated string of directories to check
dirs="${HOME}/.local/opt/bin"

# Loop through the directories
for dir in $dirs; do
    if [ -d "$dir" ]; then
        make_links "$dir"
        break
    fi
done
