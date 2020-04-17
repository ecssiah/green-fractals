#!/bin/bash

convert -size 1024x1024 xc:black black.png

for f in $1/*
do
    echo "Processing $f file..."
    convert $f -rotate 90 xform1.png
    convert xform1.png black.png $f -combine *.png
done