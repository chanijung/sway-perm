#!/bin/bash

## array of datasets
declare -a arr=("flex" "grep" "gzip" "sed")

## loop!
for i in "${arr[@]}"
do
	python3.6 main_linux.py -d "$i"&
done

exit 1