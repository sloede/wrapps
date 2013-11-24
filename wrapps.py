#!/usr/bin/env python

import os
import subprocess
import sys

class Wrapps:
    ssh_cmd = 'ssh'
    scp_cmd = 'scp'

    def __init__(self, host=None, user=None, port=None, local_dir=None, remote_dir=None):
        self.host = host
        self.user = user
        self.port = port
        self.local_dir = local_dir
        self.remote_dir = remote_dir

    def execute(self, cmd, remote_dir=None):
        p = subprocess.Popen([self.ssh_cmd, self.host, cmd],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        return p.returncode, out, err

    def download(self, filename, local_dir=None):
        pass

    def upload(self, filename, remote_dir=None):
        pass
