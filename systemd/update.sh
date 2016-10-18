#!/bin/bash

cd /var/www/friskytaphouse.com/frisco-backend

git pull

cp ./systemd/friscod.service /lib/systemd/system/friscod.service
systemctl daemon-reload
systemctl enable friscod
systemctl restart friscod
