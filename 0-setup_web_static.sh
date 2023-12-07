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
</html>" | tee /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

printf %s "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html

	server_name _;

	location /hbnb_static/ {
		alias /data/web_static/current/;
	}

	location / {
		add_header X-Served-By $HOSTNAME;
		try_files \$uri \$uri/ @404;
	}

	location /redirect_me {
		return 301 \"Moved Permanently\";
	}

	location @404 {
		return 404 \"Ceci n'est pas une page\n\";
	}
}" > /etc/nginx/sites-available/default

service nginx restart
