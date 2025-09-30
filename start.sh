#!/bin/bash
sleep 2

cd $HOME/.local/auto_sshfs
./venv/bin/python mount.py unmount &> /dev/null

if [[ $1 = "-u" ]]; then
	./venv/bin/python mount.py unmount 
	exit
else
	while [[ 0 ]];
	do
	    ./venv/bin/python mount.py mount
	    sleep 2
	done
fi
