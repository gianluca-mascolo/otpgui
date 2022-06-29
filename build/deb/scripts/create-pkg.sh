#!/bin/bash
set -eu
set -o pipefail
GIT_TAG="$1"
if ( [ "$GIT_TAG" = "dev" ] ); then GIT_TAG="0.0.0"; CHANGELOG_FLAG="-d"; else CHANGELOG_FLAG=""; fi
[ -z ${GITHUB_TOKEN:+is_null} ] || CHANGELOG_FLAG="$CHANGELOG_FLAG -m api"
export GIT_TAG
pushd ~/artifacts
  tar xzf ~/gitsrc/build/python/artifacts/otpgui-${GIT_TAG}.tar.gz
  pushd otpgui-${GIT_TAG}
    cp -r ~/gitsrc/icons .
    mkdir -p desktop
    cp ~/gitsrc/otpgui.desktop desktop/otpgui.desktop
    tar -C ~/artifacts -czf ~/artifacts/otpgui_${GIT_TAG}.orig.tar.gz otpgui-${GIT_TAG}
    cp -r ~/debian .
    pushd ~/gitsrc
      ./tools/debian-changelog-generator.py $CHANGELOG_FLAG > ~/artifacts/otpgui-${GIT_TAG}/debian/changelog
    popd
    debuild -us -uc
  popd
  echo "*** PACKAGE INFORMATION ***"
  dpkg-deb -I "python3-otpgui_${GIT_TAG}-1_all.deb"
popd
