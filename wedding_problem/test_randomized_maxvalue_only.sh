#!/bin/bash

FILE_NAME='randomized_maxvalue.py'
for i in 1 2 3 4 5 6 7 8 9 10
do
	python3 $FILE_NAME given/64_16.in >> "results/$FILE_NAME $i 64_16"
	python3 $FILE_NAME given/99_33.in >> "results/$FILE_NAME $i 99_33"
	python3 $FILE_NAME given/100_10.in >> "results/$FILE_NAME $i 100_10"
	python3 $FILE_NAME given/100_20.in >> "results/$FILE_NAME $i 100_20"
done
