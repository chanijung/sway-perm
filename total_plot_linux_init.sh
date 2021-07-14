#!/bin/bash

declare -a arr=(3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)

## loop
for i in "${arr[@]}"
do
	python3.6 main_linux.py -d sed -init $i&
done

exit 1