#!/bin/bash
GIT_TAG="$1"
echo -n "Updating repos... "
sudo pacman -Sy --noconfirm --noprogressbar
echo "done!"
echo -n "Installing otpgui..."
sudo pacman -U ~/artifacts/otpgui-${GIT_TAG}-1-any.pkg.tar.zst --noconfirm --noprogressbar
echo "done!"
otpgui -v
