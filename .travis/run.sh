#!/bin/bash

set -e
set -x

PYENV_ROOT="$HOME/.pyenv"
PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
source ~/.venv/bin/activate

tox

MACOSX_DEPLOYMENT_TARGET="10.7"
PLATFORM_NAME="macosx_10_7_intel"
python setup.py bdist_wheel --plat-name "$PLATFORM_NAME"
