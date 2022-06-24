#!/bin/bash
set -eu
set -o pipefail
GIT_TAG="$1"
[ "$GIT_TAG" = "dev" ] && GIT_TAG="0.0.0"
export GIT_TAG

pushd ~/artifacts

tar xzf ~/gitsrc/build/python/artifacts/otpgui-${GIT_TAG}.tar.gz
pushd otpgui-${GIT_TAG}
cp -r ~/gitsrc/icons .
mkdir -p desktop
cp ~/gitsrc/otpgui.desktop desktop/otpgui.desktop
tar -C ~/artifacts -czf ~/artifacts/otpgui_${GIT_TAG}.orig.tar.gz otpgui-${GIT_TAG}
cp -r ~/templates/debian .
debuild -us -uc
popd
popd
