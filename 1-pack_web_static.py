#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from web_static folder
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Creates a compressed archive of the web_static folder
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)

        # Ensure the "versions" directory exists
        if not os.path.exists("versions"):
            os.makedirs("versions")

        local("tar -czvf {} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None

