#!/bin/bash
sudo chgrp sshfs /run
sudo chgrp sshfs /run/media

sudo mkdir /run/media/$USER

sudo chown $USER:sshfs /run/media/$USER
