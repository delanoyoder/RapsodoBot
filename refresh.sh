#!/bin/bash

# Define the python command you want to execute
command="python bot.py"

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not in a virtual environment."

    # Check if a virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Virtual environment not found, creating one..."
        python3 -m venv venv
    fi

    # Activate the virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Already in a virtual environment."
fi

# Check if selenium is installed
if ! pip freeze | grep -q selenium; then
	echo "Selenium not found, installing..."
	pip install selenium
fi

# Check urllib3 version and downgrade if needed
if pip freeze | grep -q "urllib3==1.26.7"; then
	echo "urllib3 is already the correct version."
else
	echo "urllib3 is not the correct version, downgrading..."
	pip install urllib3==1.26.7
fi

# Execute the command and store the exit status
$command
exit_status=$?

# Loop until the command exits successfully (exit status 0)
while [ $exit_status -ne 0 ]; do
	# If the command failed, sleep for a bit, then try again
	echo "Command failed with exit status $exit_status, retrying..."
	$command
	exit_status=$?
done

echo "Command executed successfully, exiting."
