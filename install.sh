#!/bin/bash

sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS study"

python /home/box/web/ask/manage.py syncdb

cd /home/box/web
gunicorn -w 1 -b 0.0.0.0:8080 hello:app &
cd /home/box/web/ask/ask
gunicorn -w 1 -b 0.0.0.0:8000 wsgi:application &


