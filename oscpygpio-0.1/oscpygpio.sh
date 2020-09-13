#! /usr/bin/env bash

# get to right directory from $0 i guess

which $0

# see if venv exists
#   if not - create venv

# activate python enviroment 
source ../venv/bin/activate

# check req exists?
pip install -r requirments.txt

# launch with any passed parameters
# multiple instances will jsut error if trying to bind to the same port and crash out - maybe a nicer trap in the python for this
# do i need to create a PID file when running as a service... could do some catching then etc. / prompt to stop service version if same config file?
./oscpygpio.py 

