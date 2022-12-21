#!/bin/bash

cur_dir=$(pwd)

sudo apt update && apt install python3-pip && pip install python-dateutil && pip install qrcode && pip install Image && pip install selenium && sleep 2
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
wget https://chromedriver.storage.googleapis.com/108.0.5359.22/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
rm -rf chromedriver_linux64.zip
rm -rf google-chrome-stable_current_amd64.deb

echo "Your Panel Ip: "
read ip

echo "Your Panel Port: "
read port

echo "Your x-ui Panel Port: "
read xui

echo "Your x-ui Panel Username: "
read xuiUsr

echo "Your x-ui Panel Password: "
read xuiPass

sudo /bin/python3 insert.py -s "$ip:$port:$xui:$xuiUsr:$xuiPass" && sleep 2
sudo cp test.service /etc/systemd/system/
echo "Service Replaced!!"
sudo mkdir /root/sqlBackup
sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
echo | sudo systemctl status test.service

echo "All Done!!"
