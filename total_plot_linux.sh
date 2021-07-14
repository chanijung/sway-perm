#!/bin/bash

## array of datasets
declare -a arr=("flex" "grep" "gzip" "sed")
# declare -a arr=("flex")

## loop!
for i in "${arr[@]}"
do
	python3.6 main_linux.py -d "$i"&
#	python main_linux.py -d "$i" -n 5 &
done

exit 1