#!/bin/sh

sudo cp ~/mitwelten-cam-16mp/mitwelten-cam.service /etc/systemd/system/mitwelten-cam.service 

sudo systemctl daemon-reload
sudo systemctl enable mitwelten-cam.service
sudo systemctl start mitwelten-cam.service

systemctl is-active --quiet mitwelten-cam.service && echo mitwelten-cam service is running || echo mitwelten-cam service is not running