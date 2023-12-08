#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack."""
from fabric.api import local
from datetime import datetime
import os.path


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
