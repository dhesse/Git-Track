#!/usr/bin/env python
from git import Repo
import datetime
import os
import pickle
import sys
import time
import subprocess

from issue_db.issue_db import IssueDB, Issue

COMMANDS = ("show", "add", "info", "rm", "close", "showall", "re-add",
            "edit", "prio")

def print_help():
    print (
        "usage: %s command\n"
        "commands:\n"
        "     show       Show all open issues.\n"
        "     showall    Show all issues.\n"
        "     info id    More information on issue with id.\n"
        "     add        Add issue.\n"
        "     re-add     Set the isue sha to current HEAD's.\n"
        "                Useful if you did a git commit --amend.\n"
        "     edit       Edit issue message corresponding to id.\n"
        "     close id   Close issue with id.\n"
        "     rm id      Remove issue with id.\n"
        "     prio id p  Set priority of id to integer value p.\n") % sys.argv[0]
    
if __name__ == "__main__":
    ISSUES = IssueDB()
    ARGS = sys.argv
    ARGS += ["",""]
    CMD, OPT = ARGS[1:3]
    if CMD not in COMMANDS:
        print_help()
    else:
        if CMD == 'show':
            print ISSUES
        elif CMD == 'add':
            ISSUES.add_issue()
        elif CMD == 'info':
            ISSUES.info(OPT)
        elif CMD == 'rm':
            ISSUES.remove(OPT)
        elif CMD == 'close':
            ISSUES.close(OPT)
        elif CMD == 'showall':
            print ISSUES.show_all()
        elif CMD == 're-add':
            ISSUES.re_add(OPT)
        elif CMD == 'edit':
            ISSUES.edit(OPT)
        elif CMD == 'prio':
            ISSUES.set_prio(OPT, ARGS[3])
