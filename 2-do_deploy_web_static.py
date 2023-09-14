#!/usr/bin/python3
"""
Fabric script to execute the do_deploy function
"""

from fabric.api import *
import os

env.hosts = ["54.144.137.166", "54.237.14.236"]
env.user = "ubuntu"
env.key_filename = "/root/0-RSA_public_key"

def do_deploy(archive_path):
    """
    Executes the do_deploy function on remote servers
    """
    if not os.path.exists(archive_path):
        print("Archive path does not exist. Aborting deployment.")
        return False

    """
    Args:
    """
    
    archive_filename = os.path.basename(archive_path)
    archive_basename = os.path.splitext(archive_filename)[0]

    remote_folder = "/data/web_static/releases/{}".format(archive_basename)

    put(archive_path, "/tmp/")
    run("sudo mkdir -p {}".format(remote_folder))
    run("sudo tar -xzf /tmp/{} -C {}/".format(archive_filename, remote_folder))
    run("sudo rm /tmp/{}".format(archive_filename))
    run("sudo mv {}/web_static/* {}".format(remote_folder, remote_folder))
    run("sudo rm -rf {}/web_static".format(remote_folder))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(remote_folder))

    print("New version deployed!")
    
    """
    Returns:
    """

    return True

if __name__ == "__main__":
    archive_path = "versions/web_static_20230914071506.tgz"  # Update with your actual archive path
    do_deploy(archive_pat)
