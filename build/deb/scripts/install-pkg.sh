#!/bin/bash
GIT_TAG="$1"
export DEBIAN_FRONTEND=noninteractive
[ "$GIT_TAG" = "dev" ] && GIT_TAG="0.0.0"
echo -n "Updating repos... "
sudo apt-get -y update 
echo "done!"
echo -n "Installing otpgui..."
sudo apt-get -y install ~/artifacts/python3-otpgui_${GIT_TAG}-1_all.deb
echo "done!"
otpgui -v
