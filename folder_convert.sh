#!/bin/bash
for filename in /files/*.png; do
    #echo $filename
    ./mtv.py -a $filename -s ${filename%.*}.mp3 -o ${filename%.*}.mp4
done