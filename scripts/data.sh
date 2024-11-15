#!/bin/bash

set -e

DROP=$1

if [ -z "$DROP" ]; then
    echo "Error: DROP parameter is missing. See data/preprocess.py for more."
    echo "Usage: $0 <drop_value>"
    exit 1
fi

# Download data and Drop images and respective labels of the full folder
python3 data/dataset.py --drop $DROP --download_data

zip -r data/data.zip data/data/

rm -r data/data/