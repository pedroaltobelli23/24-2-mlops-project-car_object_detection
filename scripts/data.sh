#!/bin/bash

set -e

DROP=$1

if [ -z "$DROP" ]; then
    echo "Error: DROP parameter is missing. See data/preprocess.py for more."
    echo "Usage: $0 <drop_value>"
    exit 1
fi

python3 data/data_install.py

python3 data/preprocess.py --drop $DROP

zip -r data/data.zip data/data/

rm -r data/data/