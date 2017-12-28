#! /bin/zsh

source /home/cryptocoins/.zshrc
cd /usr/local/lib/apps/cryptocoins
pyenv activate cryptocoins
python scripts/crypto_compare/crypto_compare_collect_daily.py
