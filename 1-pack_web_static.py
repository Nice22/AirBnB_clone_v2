#!/usr/bin/env python3
"""Fabric script to generate a .tgz archive from web_static folder"""

from fabric.api import local
from datetime import datetime

def do_pack():
    """Creates a .tgz archive from web_static folder"""
    local("mkdir -p versions")
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )
    result = local("tar -cvzf versions/{} web_static".format(archive_name))
    if result.failed:
        return None
    return "versions/{}".format(archive_name)

