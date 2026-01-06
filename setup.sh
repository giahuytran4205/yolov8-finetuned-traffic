#!/bin/bash
apt install -y python3 python3-pip

mkdir dataset

pip install -r requirements.txt
pip uninstall opencv-python -y
pip install opencv-python-headless

python3 download_dataset.py