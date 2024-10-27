#!/bin/bash

exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>logs/data.log 2>&1

python3 data/data_install.py

python3 data/preprocess.py

zip -r data/data.zip data/data/

rm -r data/data/