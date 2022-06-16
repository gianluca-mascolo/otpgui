#!/bin/bash
GIT_TAG="$1"
echo -n "Updating repos... "
sudo pacman -Sy --noconfirm --noprogressbar
echo "done!"
echo -n "Installing otpgui..."
sudo pacman -U /home/testuser/build/otpgui-${GIT_TAG}-1-any.pkg.tar.zst
echo "done!"
