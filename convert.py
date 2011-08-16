#!/usr/bin/env python
"""Converts an old version's data base to the recent format.

The database of the rc-1 did not have a priority field. This script
just adds this to all issues."""

import os
import pickle

ISSUE_FILE = '.issues'

if __name__ == "__main__":
    with open(ISSUE_FILE,'r') as issues:
        DB = pickle.load(issues)
        for issue in DB.values():
            if not hasattr(issue, 'priority'):
                issue.priority = 3
    with open(ISSUE_FILE, 'w') as issues:
        pickle.dump(DB, issues, -1)
        
