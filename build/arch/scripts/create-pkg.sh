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
    wget --timeout=30 --tries=3 -O ${OTP_TMP} "https://github.com/gianluca-mascolo/otpgui/archive/refs/tags/${GIT_TAG}.tar.gz"
    tar tzf ${OTP_TMP} && OTP_SHA256=$(sha256sum -b ${OTP_TMP} | awk '{print $1}')
    [ -f ${OTP_TMP} ] && rm -f ${OTP_TMP}
}
fi

cat << EOF > ~/.makepkg.conf
PACKAGER="Gianluca Mascolo <gianluca@gurutech.it>"
EOF

echo $OTP_SOURCE
echo $OTP_SHA256
export OTP_SOURCE OTP_SHA256 GIT_TAG

envsubst '$OTP_SOURCE,$OTP_SHA256,$GIT_TAG' < ~/gitsrc/build/arch/PKGBUILD.tmpl > ~/artifacts/PKGBUILD
pushd ~/artifacts
sudo pacman -Sy --noconfirm --noprogressbar
makepkg -s --noconfirm --noprogressbar
makepkg --printsrcinfo > .SRCINFO
echo "*** PACKAGE INFORMATION ***"
pacman -Qpi otpgui-${GIT_TAG}-1-any.pkg.tar.zst
popd
