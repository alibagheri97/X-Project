#!/bin/bash

cur_dir=$(pwd)

sudo apt update && apt install python3-pip && pip install python-dateutil && pip install sqlite3 && pip install qrcode && pip install Image && sleep 2

echo "Your Panel Ip: "
read ip

echo "Your Panel Port: "
read port

sudo /bin/python3 insert.py -s "$ip:$port" && sleep 2
sudo cp test.service /etc/systemd/system/
echo "Service Replaced!!"
sudo mkdir /root/sqlBackup
sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
echo | sudo systemctl status test.service

echo "All Done!!"
