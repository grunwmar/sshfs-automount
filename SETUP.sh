#!/bin/bash
echo "=> Creating $HOME/.local/auto_sshfs"
mkdir -p $HOME/.local/auto_sshfs

echo ""
echo "=> Copying content to $HOME/.local/auto_sshfs"
cp -R ./ $HOME/.local/auto_sshfs

cd $HOME/.local/auto_sshfs

echo ""
echo "=> Creating virtual environment"
python -m venv venv
./venv/bin/pip install -r packages.txt

echo ""
echo "=> Linking $HOME/.local/auto_sshfs/devices.toml to $HOME/.config/sshfs_devices.toml"
ln -s $HOME/.local/auto_sshfs/devices.toml $HOME/.config/sshfs_devices.toml

echo ""
echo "=> Setting limited permissions for content of ./id directory"
chmod 700 -R id

echo ""
echo "=> Creating sshfs group"
sudo groupadd sshfs

echo ""
echo "=> Adding user $USER to sshfs group"
sudo usermod --append --groups sshfs $USER

echo ""
echo "=> Adding /mnt to sshfs group"
sudo chgrp sshfs /mnt

echo ""
echo "=> Creating /mnt/$USER directory"
sudo mkdir /mnt/$USER

echo ""
echo "=> Adding /mnt/$USER to sshfs group"
echo "=> Changing owner of /mnt/$USER to $USER"
sudo chown $USER:sshfs /mnt/$USER

echo ""
echo "=> Creating symlink /mnt/$USER -> $HOME/Mounts"
ln -s /mnt/$USER -> $HOME/Mounts


