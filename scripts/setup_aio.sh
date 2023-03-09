#!/bin/sh

cd ~
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh

./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
./install_pivariety_pkgs.sh -p imx519_kernel_driver_low_speed

sudo apt install -y python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip git

cd ~
git clone https://github.com/mitwelten/mitwelten-cam-16mp.git

cd ~/mitwelten-cam-16mp
pip3 install -r requirements.txt

sudo cp ~/mitwelten-cam-16mp/mitwelten-cam.service /etc/systemd/system/mitwelten-cam.service 

sudo systemctl daemon-reload
sudo systemctl enable mitwelten-cam.service
sudo systemctl start mitwelten-cam.service