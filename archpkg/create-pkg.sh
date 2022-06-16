#!/bin/bash
set -eu
set -o pipefail

GIT_TAG="$1"
if ( [ "$GIT_TAG" = "dev" ] ); then {
    OTP_SHA256="SKIP"
    OTP_SOURCE="otpgui-dev::git+file:///home/testuser/gitsrc"
} else {
    export OTP_SOURCE="otpgui-${GIT_TAG}.tar.gz::https://github.com/gianluca-mascolo/otpgui/archive/refs/tags/${GIT_TAG}.tar.gz"
    OTP_TMP=$(mktemp --suffix ".tar.gz")
    wget --timeout=30 --tries=3 -O ${OTP_TMP} "$OTP_SOURCE"
    tar tzf ${OTP_TMP} && OTP_SHA256=$(sha256sum -b ${OTP_TMP} | awk '{print $1}')
    [ -f ${OTP_TMP} ] && rm -f ${OTP_TMP}
}
fi
echo $OTP_SOURCE
echo $OTP_SHA256
export OTP_SOURCE OTP_SHA256 GIT_TAG
envsubst '$OTP_SOURCE,$OTP_SHA256,$GIT_TAG' < /home/testuser/archpkg/PKGBUILD.tmpl > /home/testuser/build/PKGBUILD
pushd /home/testuser/build
sudo pacman -Sy --noconfirm --noprogressbar
makepkg -s --noconfirm --noprogressbar
makepkg --printsrcinfo > .SRCINFO
popd
