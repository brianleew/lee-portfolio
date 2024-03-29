#!/bin/bash

function read_hosts {
	if [ -f "$1" ]; then
	       	count=1
        	for f in $(cat $1);
        	do
                	hosts_array[$count]=$f
                	((count++))
        	done
        else
		echo "$1 doesn't exist"
                exit 0
        fi
}

function pick_host {
	count=1
	for f in $(cat $1);
	do
		echo "$count"")" "${hosts_array[$count]}" 
		((count++))
	done
	
	read -p "Enter a number to select a host: " which_host
	
	until (( "$which_host" < "$count" )) && (( "$which_host" > 0 )); do
		read -p "Enter a number to select a host: " which_host
	done
}

read_hosts $@
cmd=""
while [ "$cmd" != "q" ] || [ "$cmd" != "Q" ]; do

echo "(P) for ping"
echo "(N) for nslookup"
echo "(S) for ssh"
echo "(H) for hostname"
echo "(I) for ifconfig"
echo "(Q) for quit" 
read -p "Select one of the above: " cmd 

case $cmd in
	[Pp]*)
		pick_host $@
		echo "ping -c 1" "${hosts_array[$which_host]}"
		echo $(ping -c 1 ${hosts_array[$which_host]})
		;;
	[Nn]*)
		pick_host $@
		echo "nslookup" "${hosts_array[$which_host]}"
		echo $(nslookup ${hosts_array[$which_host]})
		;;
	[Ss]*)
		read -p "Enter your user name: " un
		read -p "Enter your server name: " sn
		ssh $un@$sn
		;;
	[Hh]*)
		hostname 
		;;
	[Ii]*)
		ifconfig -a
		;;
	[Qq]*)
		exit 1
		;;
esac
done
