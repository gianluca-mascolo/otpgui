#!/bin/bash
GIT_TAG="$1"
sudo pacman -Sy --noconfirm --noprogressbar
sudo pacman -U /home/testuser/build/otpgui-${GIT_TAG}-1-any.pkg.tar.zst