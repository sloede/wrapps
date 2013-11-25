#!/usr/bin/env python

import os
import subprocess
import sys

class Wrapps:
    # Set default executables
    ssh_exe = 'ssh'
    scp_exe = 'scp'

    def __init__(self, host, user=None, port=None, local_dir=None,
                 remote_dir=None):
        # Save arguments
        self.set_host(host)
        self.set_user(user)
        self.set_port(port)
        self.set_local_dir(local_dir)
        self.set_remote_dir(remote_dir)

        # Save current directory
        self.cwd = os.getcwd()

    def set_host(self, host):
        self._host = host

    def set_user(self, user):
        self._user = user

    def set_port(self, port):
        self._port = port

    def set_local_dir(self, local_dir):
        self._local_dir = local_dir

    def set_remote_dir(self, remote_dir):
        self._remote_dir = remote_dir

    def set_ssh_exe(self, exe):
        self.ssh_exe = exe

    def set_scp_exe(self, exe):
        self.scp_exe = exe

    def execute(self, cmd, remote_dir=None):
        # Build ssh command
        ssh_cmd = self.build_ssh_command(
                cmd,
                remote_dir if remote_dir else self._remote_dir)

        # Execute command
        p = subprocess.Popen(ssh_cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        # Return exit code and output
        return p.returncode, out, err

    def download(self, filepath, local_dir=None, target_name=None):
        # Build source
        if self._user:
            source = "{u}@{h}:{f}".format(u=self._user, h=self._host, f=filepath)
        else:
            source = "{h}:{f}".format(h=self._host, f=filepath)

        # Build target
        if local_dir:
            target = os.path.normpath(local_dir) + os.sep
        elif self._local_dir:
            target = os.path.normpath(self._local_dir) + os.sep
        else:
            target = self.cwd + os.sep
        if target_name:
            target = target + target_name
        target = os.path.expanduser(target)

        # Build command and stringify it
        if self._port:
            cmd = [self.scp_exe, '-P', self._port, source, target]
        else:
            cmd = [self.scp_exe, source, target]
        cmd = map(str, cmd)

        # Execute scp command
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        # Return exit code and output
        return p.returncode, out, err

    def upload(self, filepath, remote_dir=None, target_name=None):
        # Build source
        source = filepath

        # Build target
        if remote_dir:
            target = os.path.normpath(remote_dir) + os.sep
        elif self._remote_dir:
            target = os.path.normpath(self._remote_dir) + os.sep
        else:
            target = ''
        if self._user:
            target = "{u}@{h}:{t}".format(u=self._user, h=self._host, t=target)
        else:
            target = "{h}:{t}".format(h=self._host, t=target)
        if target_name:
            target = target + target_name

        # Build command and stringify it
        if self._port:
            cmd = [self.scp_exe, '-P', self._port, source, target]
        else:
            cmd = [self.scp_exe, source, target]
        cmd = map(str, cmd)

        # Execute scp command
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        # Return exit code and output
        return p.returncode, out, err

    def reachable(self):
        # Run command that is guaranteed to work on all shells and return
        # True if the command execution was successful
        returncode, _, _ = self.execute('echo')
        if returncode == 0:
            return True
        else:
            return False

    def build_ssh_command(self, cmd, remote_dir=None):
        # Start with executable
        args = [self.ssh_exe]

        # Add user if set
        if self._user:
            args.extend(['-l', self._user])

        # Add port if set
        if self._port:
            args.extend(['-p', self._port])

        # Add host
        args.append(self._host)

        # Change to remote_dir first, if remote_dir is set
        if remote_dir:
            args.append("cd {r}; {c}".format(r=remote_dir, c=cmd))
        else:
            args.append(cmd)

        # Stringify arguments and return them
        args = map(str, args)
        return args
