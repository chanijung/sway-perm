#!/bin/bash

## array of datasets
declare -a arr=("flex" "grep" "gzip" "sed")

## loop!
for i in "${arr[@]}"
do
	# python3.6 main_linux.py -d "$i"&
	python3.6 main_linux.py -d "$i" -init 4 -n 2&
done

exit 1