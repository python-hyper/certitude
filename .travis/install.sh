#!/bin/bash

set -e
set -x

# Update Homebrew and install Rust
brew update
brew install rust
brew outdated openssl || brew upgrade openssl

# Install PyEnv
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
PYENV_ROOT="$HOME/.pyenv"
PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

case "${TOXENV}" in
    py27)
        curl -O https://bootstrap.pypa.io/get-pip.py
        python get-pip.py --user
        ;;
    py33)
        pyenv install 3.3.6
        pyenv global 3.3.6
        ;;
    py34)
        pyenv install 3.4.6
        pyenv global 3.4.6
        ;;
    py35)
        pyenv install 3.5.3
        pyenv global 3.5.3
        ;;
    py36)
        pyenv install 3.6.2
        pyenv global 3.6.2
        ;;
    pypy*)
        pyenv install pypy-5.7.1
        pyenv global pypy-5.7.1
        ;;
esac
pyenv rehash
python -m pip install --user virtualenv
python -m virtualenv ~/.venv
source ~/.venv/bin/activate

export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CFLAGS="-I$(brew --prefix openssl)/include"
pip install -U tox wheel
