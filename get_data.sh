#!/bin/bash 

for j in $(echo {14..10})
do 
	for i in $(echo {01..12})
	do 
		fil=yellow_tripdata_20$j-$i.csv
		filg=$fil.gz
		if [ -e $filg ] || [ -e $fil ]
		then
			echo 'done skiping'
		else 
			echo 'downloading'
			wget https://storage.googleapis.com/tlc-trip-data/20$j/yellow_tripdata_20$j-$i.csv
		fi
	done
done

