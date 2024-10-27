#!/bin/bash

python3 data/data_install.py

python3 data/preprocess.py

zip -r data/data.zip data/data/