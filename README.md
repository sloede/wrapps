wrapps
======

This is a tiny wrapper library to enable using the `ssh` and `scp` commands from
within Python. Contrary to e.g. `paramiko` it does not need any additional
libraries to be installed, but uses the `ssh` and `scp` commands directly. Of
course this approach comes with its own bag of issues, but hey, at least it
*should* work anywhere.

Requirements
------------

*   Python >= 2.6
*   `ssh` and `scp`-like commands installed on the local machine
