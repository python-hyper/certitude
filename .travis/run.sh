#!/bin/bash

set -e
set -x

PYENV_ROOT="$HOME/.pyenv"
PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
source ~/.venv/bin/activate

tox
python setup.py bdist_wheel
