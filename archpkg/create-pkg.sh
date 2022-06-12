#!/bin/bash
GIT_TAG="$1"
export OTP_SOURCE="https://github.com/gianluca-mascolo/otpgui/archive/refs/tags/${GIT_TAG}.tar.gz"
OTP_TMP=$(mktemp --suffix ".tar.gz")
wget --timeout=30 --tries=3 -O ${OTP_TMP} "$OTP_SOURCE"
tar tzf ${OTP_TMP} && OTP_SHA256=$(sha256sum -b ${OTP_TMP} | awk '{print $1}')
echo $OTP_SOURCE
echo $OTP_SHA256
[ -f ${OTP_TMP} ] && rm -f ${OTP_TMP}
export OTP_SOURCE OTP_SHA256 GIT_TAG
envsubst '$OTP_SOURCE,$OTP_SHA256' < /home/testuser/archpkg/PKGBUILD.tmpl > /home/testuser/build/PKGBUILD
pushd /home/testuser/build
sudo pacman -Sy --noconfirm --noprogressbar
makepkg -s --noconfirm --noprogressbar
popd