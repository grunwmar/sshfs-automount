#!/bin/bash
cd $HOME/.local/auto_sshfs
./allow_run_media_mountpoint.sh
./venv/bin/python __main__.py $1

