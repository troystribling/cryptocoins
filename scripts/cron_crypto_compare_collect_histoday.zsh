#! /bin/zsh

source /home/cryptocoins/.zshrc
cd /usr/local/lib/apps/cryptocoins
pyenv activate cryptocoins
python /usr/local/lib/apps/crypto_compare_collect_histoday.py
