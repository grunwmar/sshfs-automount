#!/bin/bash
cd $HOME/.local/auto_sshfs

if [[ $1 = "--edit-device-list" ]] || [[ $1 = "-e" ]]; then
    nano devices.toml
    exit
fi

fatal() {
    echo "FATAL ERROR: $@"
    exit 1
  }
  trap 'sudo -k' EXIT
  zenity --password | sudo -Sv || fatal "Unable to sudo"

./allow_run_media_mountpoint.sh
./venv/bin/python __main__.py $1

