#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

apt-get update
apt-get -y install nginx
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/current/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
service nginx restart
