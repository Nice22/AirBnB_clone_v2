#!/usr/bin/env python3
"""
Fabric script to execute the do_deploy function
"""

from fabric.api import *

env.hosts = ["35.196.96.41", "3.234.218.189"]
env.user = "ubuntu"
env.key_filename = "/root/0-RSA_public_key"

def deploy(archive_path):
    """
    Executes the do_deploy function on remote servers
    """
    archive_path = local("./2-do_deploy_web_static.py")
    if archive_path.failed:
        print("Error generating archive. Aborting deployment.")
        return

    result = run("python3 -c 'from datetime import datetime; print(datetime.now().strftime(\"%Y%m%d%H%M%S\"))'")
    if result.failed:
        print("Error running remote command. Aborting deployment.")
        return

    remote_archive_path = "versions/web_static_{}.tgz".format(result)
    put(archive_path, remote_archive_path)

    print("Deploying archive...")
    with settings(warn_only=True):
        if run("mkdir -p /tmp/web_static").succeeded:
            if run("tar -xzf {} -C /tmp/web_static".format(remote_archive_path)).succeeded:
                if run("mv /tmp/web_static/web_static/* /tmp/web_static").succeeded:
                    if run("rm -rf /tmp/web_static/web_static").succeeded:
                        if run("rm -rf /data/web_static/current").succeeded:
                            if run("ln -s /tmp/web_static /data/web_static/current").succeeded:
                                print("New version deployed!")
                                return

    print("Deployment failed.")

