#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers,
using the function do_deploy """
from fabric.api import local, put, run, env
from datetime import datetime
import os.path

env.hosts = ['100.25.180.19', '100.24.244.121']


def do_pack():
    """Function to generate a .tgz archive from the contents of the web_static
    folder of the AirBnB Clone repo."""
    if not os.path.isdir('versions'):
        local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(date)
    print("Packing web_static to {}".format(path))
    if local("tar -cvzf {} web_static".format(path)).failed:
        return None
    return path


def do_deploy(archive_path):
    """Function to distribute an archive to the web servers."""
    if not os.path.isfile(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split('/')[-1]
        path = "/data/web_static/releases/" + file_name.split('.')[0]
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(path, path))
        run("rm -rf {}/web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        print("New version deployed!")
        return True
    except Exception:
        return False
