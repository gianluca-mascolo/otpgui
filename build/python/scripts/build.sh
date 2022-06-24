#!/bin/bash
set -eu
set -o pipefail

GIT_TAG="$1"
if ( [ "$GIT_TAG" = "dev" ] ); then {
    poetry version 0.0.0
} else {
    poetry version ${GIT_TAG}
}
fi

poetry build
mv dist/otpgui* build/python/artifacts/