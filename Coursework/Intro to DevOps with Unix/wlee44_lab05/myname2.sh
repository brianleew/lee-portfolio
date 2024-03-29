#!/bin/bash
read -p "Enter a string: " x
echo $x > $$.name
echo $(cat $$.name)
