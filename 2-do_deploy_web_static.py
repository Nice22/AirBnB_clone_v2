#!/usr/bin/python3
"""
Fabric script to execute the do_deploy function
"""

from fabric.api import env, put, run  # Import put and run functions
import os

env.hosts = ["54.144.137.166", "54.159.22.227"]
env.user = "ubuntu"
env.key_filename = "/root/0-RSA_public_key"


def do_deploy(archive_path):
    """
    Deploy a compressed archive to the web server.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print("Archive path does not exist. Aborting deployment.")
        return False

    archive_filename = os.path.basename(archive_path)
    archive_basename = os.path.splitext(archive_filename)[0]

    remote_folder = "/data/web_static/releases/{}".format(archive_basename)

    put(archive_path, "/tmp/")
    run("sudo mkdir -p {}".format(remote_folder))
    run("sudo tar -xzf /tmp/{} -C {}/".format(archive_filename, remote_folder))
    run("sudo rm /tmp/{}".format(archive_filename))

    # Check if files and directories exist in remote_folder
    result = run("sudo ls {}/web_static/".format(remote_folder))

    if not result.succeeded:
        print("Failed to list files and directories in remote_folder. Aborting deployment.")
        return False

    # Remove any existing files and directories in the target directory
    run("sudo rm -rf {}/web_static/*".format(remote_folder))

    # Explicitly specify the source directory for the mv command
    run("sudo mv {}/web_static/* {}/".format(remote_folder, remote_folder))
    run("sudo rm -rf {}/web_static".format(remote_folder))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(remote_folder))

    print("New version deployed!")
    return True


if __name__ == "__main__":
    archive_path = "versions/web_static_20230914071506.tgz"
    # Update with your actual archive path
    do_deploy(archive_path)
