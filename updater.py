#!/usr/bin/env python3

import subprocess


def update():
    process = subprocess.Popen(["git", "pull", "github", "master"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def reboot():
    process = subprocess.Popen(["sudo", "reboot"], stdout=subprocess.PIPE)


if __name__ == '__main__':
    update()
    reboot()
