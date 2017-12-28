#! /bin/zsh

source /home/cryptocoins/.zshrc
cd /usr/local/lib/apps/cryptocoins
pyenv activate cryptocoins
python scripts/crypto_compare/collect_daily.py
