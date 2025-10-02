#!/usr/bin/bash

git clone https://github.com/grunwmar/sshfs-automount.git
cd sshfs-automount
bash ./SETUP.sh
cd ..
rm -rf sshfs-automount
