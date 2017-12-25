#! /bin/zsh

source /home/cryptocoins/.zshrc
cd /usr/local/lib/apps/cryptocoins
pyenv activate cryptocoins
python crypto_compare_collect_histoday.py
