#!/bin/bash
if [ $1="" ]; then
	x='phonebook.dat'
else
	if [ -f "$1" ]; then
		x=$1
	else
		x='phonebook.dat'
	fi
fi

HI='\033[0;32m'
NORMAL='\033[0m'

echo -e "${HI}1. Starts or ends with Jose$NORMAL"
echo "$(grep -E --color=always '^Jose|Jose$' $x)"

echo -e "${HI}2. Contain at least 27 upper- or lower-case characters a-z$NORMAL"
echo "$(grep -E --color=always '[a-z|A-Z]{27}' $x)"

echo -e "${HI}3. Consist of more than 18 characters$NORMAL"
echo "$(grep -E --color=always '^.{19}' $x)"

echo -e "${HI}4. Contains exactly 10 characters$NORMAL"
echo "$(grep -E --color=always '^.{10}$' $x)"

echo -e "${HI}5. Contains a sequence between 6 and 8 upper- or lower-case alphabetic characters$NORMAL"
echo "$(grep -E --color=always '(\s| )[a-zA-Z]{6,8}(\s| )' $x)"

echo -e "${HI}6. Contains a local phone number$NORMAL"
echo "$(grep -E --color=always '([^-][0-9]{3}[-][0-9]{4})|(^[0-9]{3}[-][0-9]{4})' $x)"

echo -e "${HI}7. Contains a valid URL on a line by itself$NORMAL"
echo "$(grep -E --color=always '^(http://www.|HTTP://www.)[a-zA-Z0-9]+(.com|.edu)$' $x)"
