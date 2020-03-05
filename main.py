#!/usr/bin/env python3

import subprocess
import argparse
from time import sleep
from signal import signal, SIGINT
from sys import exit

def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    subprocess.run(['watson stop'], shell=True)
    exit(0)

signal(SIGINT, handler)


parser = argparse.ArgumentParser()
parser.add_argument('project', help='Project name for watson tracking')
parser.add_argument('path', help='Path to the git directory you want to track')
args = parser.parse_args()
project = args.project

git_command = "if branch=$(git -C {path} symbolic-ref --short -q HEAD); then echo $branch; else echo ''; fi".format(path=args.path)

initial_branch = subprocess.check_output([git_command], shell=True, text=True).strip()

subprocess.run(['watson start {project} +{branch}'.format(project=project, branch=initial_branch)], shell=True)

while True:
    sleep(20)
    branch = subprocess.check_output([git_command], shell=True, text=True).strip()
    if branch != initial_branch:
        subprocess.run(['watson start {project} +{branch}'.format(project=project, branch=branch)], shell=True)
        initial_branch = branch
    else:
        pass

