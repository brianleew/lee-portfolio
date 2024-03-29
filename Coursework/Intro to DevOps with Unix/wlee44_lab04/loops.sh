#!/bin/bash

M=$(date +%M) #minutes
m=$(date +%m) #month
a=`expr $M + $m` #minutes and month added
for ((i = 0 ; i < $a ; i++)); do
	echo Iteration `expr $i + 1` out of $a. $(( $a - ($i + 1) )) iterations remaining. 
done
