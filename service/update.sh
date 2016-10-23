#!/bin/bash

cd /var/www/friskytaphouse.com/frisco-backend

git pull

# Install the init.d script and setup permissions
cp ./service/friscod /etc/init.d/friscod
chmod 755 /etc/init.d/friscod
chmod root:root /etc/init.d/friscod

# Add it as a service that starts on boot
update-rc.d friscod defaults

service friscod restart
