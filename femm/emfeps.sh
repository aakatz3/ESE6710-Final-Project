#!/bin/bash

# List all .emf files
for emf_file in $(ls *.emf)
do
    # Extract filename
    emf_filename="${emf_file%%.*}"
    # Convert .emf to .svg and .svg to .eps using Inkscape
    echo "inkscape $emf_file --export-plain-svg=$emf_filename.svg && inkscape $emf_filename.svg -E $emf_filename.eps"
    inkscape $emf_file --export-plain-svg=$emf_filename.svg && inkscape $emf_filename.svg -E $emf_filename.eps
done
