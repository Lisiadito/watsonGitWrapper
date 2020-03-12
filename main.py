#!/usr/bin/env python3

import subprocess
from time import sleep
from signal import signal, SIGINT
from sys import exit
from PyInquirer import prompt

run_main_loop = True
path = ''
project = ''
git_command = ''
initial_branch = ''
first_start = True


def handler(signal_received, frame):
    global run_main_loop
    if run_main_loop == True:
        askQuestion()
        run_main_loop = False
    else:
        subprocess.run(['watson stop'], shell=True)
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        exit(0)


def start():
    start_questions = [
        {
            'type': 'input',
            'name': 'project',
            'message': 'What is the name of the project?'
        },
        {
            'type': 'input',
            'name': 'path',
            'message': 'What is the path to the git repository?',
        }
    ]

    answers = prompt(start_questions)
    global path
    global project
    global git_command
    global initial_branch
    path = answers['path']
    project = answers['project']
    git_command = "if branch=$(git -C {path} symbolic-ref --short -q HEAD); then echo $branch; else echo ''; fi".format(path=path)
    initial_branch = subprocess.check_output(
        [git_command], shell=True, text=True).strip()


def askQuestion():
    questions = [
        {
            'type': 'list',
            'name': 'target',
            'message': 'What do you want to track?',
            'choices': [
                'Track repository',
                'Track only project'
            ]
        }
    ]

    answers = prompt(questions)
    global first_start
    first_start = True

    if (answers.get('target') == 'Track repository'):
        runWatson(True)
    elif (answers.get('target') == 'Track only project'):
        runWatson(False)
    else:
        global run_main_loop
        run_main_loop = False
        handler(None, None)


def runWatson(withTag):
    global run_main_loop
    global first_start
    run_main_loop = True
    if first_start == True:
        if withTag:
            subprocess.run(['watson start {project} +{branch}'.format(
                project=project, branch=initial_branch)], shell=True)
        else:
            subprocess.run(
                ['watson start {project}'.format(project=project)], shell=True)

    first_start = False

    while True:
        if isBranchChanged() == True:
            if withTag:
                subprocess.run(['watson start {project} +{branch}'.format(
                    project=project, branch=initial_branch)], shell=True)
            else:
                subprocess.run(
                    ['watson start {project}'.format(project=project)], shell=True)
        sleep(5)


def isBranchChanged():
    global initial_branch
    branch = subprocess.check_output(
        [git_command], shell=True, text=True).strip()
    if branch != initial_branch:
        initial_branch = branch
        return True
    else:
        return False


# listen for ctrl+c to stop tiime tracking
signal(SIGINT, handler)
start()
askQuestion()
