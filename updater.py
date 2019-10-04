#!/usr/bin/env python3

import subprocess
import os


def update():
    process = subprocess.Popen(["git", "pull", "origin", "master"], stdout=subprocess.PIPE)
    output = process.communicate()[0]

