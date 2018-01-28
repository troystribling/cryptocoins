#! /bin/zsh

source /home/cryptocoins/.zshrc
cd /usr/local/lib/apps/cryptocoins
pyenv activate cryptocoins
python scripts/one_forge/collect_daily.py
