#!/bin/bash

while getopts i:o:b:l: option
do
        case "${option}"
        in
        i) lasfolder=${OPTARG};;
        o) outfolder=${OPTARG};;
        b) buffer=${OPTARG};;
        l) length=${OPTARG};;
        esac
done


pdal tile "$lasfolder/*" "$outfolder/out_#.laz" --buffer=$buffer --length=$length
