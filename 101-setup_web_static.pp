# puppet script that sets up your web servers for the deployment of web_static

# Update the package repository
exec { 'apt_update':
  command => 'apt-get update',
}

# Install Nginx
package { 'nginx':
  ensure => 'installed',
}

# Create directories
file { ['/data/web_static/shared/', '/data/web_static/releases/test/']:
  ensure => 'directory',
}

# Create index.html content
file { '/data/web_static/releases/test/index.html':
  content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>",
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Set ownership
file { '/data/':
  ensure  => 'directory',
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Configure Nginx
file { '/etc/nginx/sites-available/default':
  content => "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html

	server_name _;

	location /hbnb_static/ {
		alias /data/web_static/current/;
	}

	location / {
		add_header X-Served-By $hostname;
		try_files \$uri \$uri/ @404;
	}

	location /redirect_me {
		return 301 'Moved Permanently';
	}

	location @404 {
		return 404 'Ceci n\'est pas une page\n';
	}
}",
}

# Restart Nginx service
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
