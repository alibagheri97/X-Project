#!/bin/bash

sudo rm /etc/systemd/system/test.service
sudo systemctl disable test.service
sudo systemctl stop test.service
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo | sudo systemctl status test.service
