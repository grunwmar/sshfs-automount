#!/bin/bash
cd $HOME/.local/auto_sshfs

fatal() {
    echo "FATAL ERROR: $@"
    exit 1
  }
  trap 'sudo -k' EXIT
  zenity --password | sudo -Sv || fatal "Unable to sudo"

./allow_run_media_mountpoint.sh
./venv/bin/python __main__.py $1

