#!/bin/bash

cd /var/www/friskytaphouse.com/frisco-backend

git pull

cp ./service/friscod /etc/init.d/friscod
chkconfig friscod on
service friscod restart
