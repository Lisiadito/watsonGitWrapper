#!/usr/bin/env python3

import subprocess
import argparse
from time import sleep
from signal import signal, SIGINT
from sys import exit
from pynput import keyboard

def on_press(key):
    try:
        if key.char == 'r':
            print()
            subprocess.run(['watson start {project}'.format(project=project)], shell=True)
        elif key.char == 't':
            print()
            initial_branch = subprocess.check_output([git_command], shell=True, text=True).strip()
            subprocess.run(['watson start {project} +{branch}'.format(project=project, branch=initial_branch)], shell=True)
    except AttributeError:
        pass

def handler(signal_received, frame):
    print()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    subprocess.run(['watson stop'], shell=True)
    exit(0)

#listen for ctrl+c to stop tiime tracking
signal(SIGINT, handler)

#listen to key to reset timetracking to no tag
listener = keyboard.Listener(on_press=on_press)
listener.start()

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

