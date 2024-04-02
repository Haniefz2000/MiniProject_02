#!/bin/sh

print_line() {
    local length=$1
    local character=$2
    for (( i = 0; i < length; i++ )); do
        echo -n "$character"
    done
    echo ""
}

print_line 100 "*"
echo "Welcome to My DataBase"
print_line 100 "*"
topics=$(kafka-topics --bootstrap-server kafka-broker:29092 --list)

########### create topics ##########
if [ -z $topics ] ; then
	echo "No topics exist. Creating new topics..."
	kafka-topics --bootstrap-server kafka-broker:29092 --create  --topic users_info  --partitions 4 --replication-factor 1
	echo "Finished Successfully...."
	print_line 100 "-"
else
	echo "Existing topics:"
    	echo "$topics"
    	print_line 100 "-"
fi

echo "Creating new topics for Add Timestamp Column"
kafka-topics --bootstrap-server kafka-broker:29092 --create  --topic timestamp  --partitions 4 --replication-factor 1
echo "Finished Successfully...."
print_line 100 "-"

echo "Creating new topics for Add Label Column"
kafka-topics --bootstrap-server kafka-broker:29092 --create  --topic label  --partitions 4 --replication-factor 1
echo "Finished Successfully...." 

########### install requirements libraries ################
if [ -f "requirements.txt" ]; then
	echo "Requirements found. Installing requirements..."
	pip3 install -r requirements.txt
	echo "Requirements installed."
else
	echo "No requirements file found. There are no requirements to install."
fi
############ calling every one minute ####################
# Infinite loop
while true; do
	if [ -f "$PWD/get_data.py" ]; then
		echo "Data is Loading...."
		/usr/bin/python $PWD/get_data.py
		echo "Data Loaded Finished Successfully!"
		print_line 100 "-"
	fi


	if [ -f "$PWD/consumer1.py" ]; then
		echo "Add Timestamp column process is starting..."
		/usr/bin/python $PWD/consumer1.py
		echo "Finished Successfully!"
		print_line 100 "-"
	else
		echo "Can't add timestamp column, There is no processor exists!"
	fi



	if [ -f "$PWD/consumer2.py" ]; then
		echo "Add label column process is starting..."
		/usr/bin/python $PWD/consumer2.py
		echo "Finished Successfully!"
		print_line 100 "-"
	else
		echo "Can't add label column, There is no processor exists!"
	fi
	if [ -f "$PWD/consumer3.py" ]; then
		echo "Saving Data on Postgresql starting......."
		/usr/bin/python $PWD/consumer3.py
		echo "Finished Successfully!"
		print_line 100 "-"
	else
		echo "Can't save data in postgesql, There is no processor exists!"
	fi
	
	# Pause execution for 1 minute
    	sleep 60
done


