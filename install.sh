#!/bin/bash

cur_dir=$(pwd)

sudo /bin/python3 insert.py &
sleep 2
sudo cp test2.service /etc/systemd/system/test.service
echo "Service Replaced!!"

sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
echo | sudo systemctl status test.service

echo "All Done!!"
