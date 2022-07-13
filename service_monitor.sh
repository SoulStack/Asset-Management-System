#!/bin/bash
# service monitor script

if [ $# -eq 0 ]; then
	echo "Usage: $(basename $0) [service] "
	exit
fi

# checking for service in local system
service=$(which $1 | cut -d/ -f4)

# chcking if service exists
if [ $? -ne 0 ] || [ -z "$service" ]; then
	echo "service not found...exiting!"
	exit
fi

echo "checking for $service service..."

# checking service
while [ 1 ]
do
	echo "checking service..."
	ps -e | grep $service &> /dev/null
	# if service stop, attempt to restart 3 times
	if [ $? -ne 0 ]; then
		echo "$service stopped.. restarting"
		i=0
		while [ $i -lt 3 ]
		do
			systemctl restart $service &> /dev/null
			[ $? -eq 0 ] && break
			i=$((i + 1))			
			sleep 1
		done
		#chcking if service coul not be restarted
		if [ $i == 3 ]; then
			echo "$service could not restart exiting..."
			break
		fi		
	fi
	sleep 3
done

# if service couldn't be restarted, notify root user
echo "Service $service could not be started. Needs attn" | mail -s "$service stopped" root 

#end 
