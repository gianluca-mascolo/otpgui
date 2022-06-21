#!/bin/bash
pushd ~/build
tar xzf ~/dist/otpgui-0.2.1.tar.gz
pushd otpgui-0.2.1
./icons/128x128/otpgui.png usr/share/icons/hicolor/32x32/apps/otpgui.png
cp -r ~/gitsrc/icons .
mkdir -p desktop
cp ~/gitsrc/otpgui.desktop desktop/otpgui.desktop
tar -C ~/build -czf ~/build/otpgui_0.2.1.orig.tar.gz otpgui-0.2.1
cp -r ~/debian .
debuild -us -uc
popd
popd