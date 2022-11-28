#!/bin/bash

sudo rm /etc/systemd/system/test.service
sudo systemctl desable test.service
sudo systemctl stop test.service
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo | sudo systemctl status test.service
