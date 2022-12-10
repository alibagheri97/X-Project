#!/bin/bash

cur_dir=$(pwd)

sudo apt update && apt install python3-pip && sudo /bin/python3 insert.py && sleep 2
sudo cp test.service /etc/systemd/system/
echo "Service Replaced!!"
sudo mkdir /root/sqlBackup
sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
echo | sudo systemctl status test.service

echo "All Done!!"
