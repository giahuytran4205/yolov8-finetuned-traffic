#!/bin/bash
apt install -y python3 python2-pip

mkdir dataset

pip install -r requirements.txt

python3 download_dataset.py