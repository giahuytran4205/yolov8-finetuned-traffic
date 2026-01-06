#!/bin/bash

mkdir dataset

pip install -r requirements.txt

huggingface-cli download giahuy4205/traffic-detection --local-dir ./dataset --repo-type dataset --local-dir-use-symlinks False