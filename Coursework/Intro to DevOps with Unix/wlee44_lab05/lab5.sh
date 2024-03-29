#!/bin/bash
if [ $# -ne 2 ]; then 
	echo "incorrect number of arguments"
	exit 1
fi

if [ ! -f $1 ]; then
	echo "no such file name exists"
	exit 1
fi

while IFS= read line;
do

	if [ "$line" == "$2" ]; then 
		echo "$2 is already in the file"
		exit 0
	fi

done < $1
echo $2 >> $1
echo "$2 was added to the file"
