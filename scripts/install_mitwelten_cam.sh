#!/bin/sh
sudo apt install -y python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip git

cd ~
git clone https://github.com/mitwelten/mitwelten-cam-16mp.git

cd ~/mitwelten-cam-16mp
pip3 install -r requirements.txt

