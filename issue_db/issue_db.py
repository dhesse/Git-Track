"The central pieces of code..."

from __future__ import with_statement
from git import Repo
from git.exc import InvalidGitRepositoryError
import datetime
import os
import pickle
import time
import subprocess
import sys


ISSUE_FILE = '.issues'

def catch_id_err(func):
    "Decorator to catch errors from wrong ids."
    def _safe(self, my_id, *args, **kwargs):
        "Id-safe version of ..."
        try:
            func(self, int(my_id), *args, **kwargs)
        except KeyError:
            print "%s: no such issue!" % my_id
        except ValueError: # comes from int(...)
            print "No or invalid id given!"
    return _safe

def safe_tmp_textfile(func):
    '''Make sure that the __issue__.msg file does not exitst (and if so,
    move it to a bakcup. Delete it after funciton call.'''
    def _safe(self, *args, **kwargs):
        "Cleanup the file __issue__.msg before and after call."
        if os.path.exists("__issue__.msg"):
            os.rename("__issue__.msg", "__issue__.msg~")
        func(self, *args, **kwargs)
        if os.path.exists("__issue__.msg"):
            os.remove("__issue__.msg")
    return _safe

class IssueDB(object):
    "'Database' managing the issues."
    def __init__(self):
        try:
            Repo('.')
            try: 
                Repo('.').head.commit.hexsha
            except ValueError:
                print "git repository .git has no head commit!"
                sys.exit()
        except InvalidGitRepositoryError:
            print "No git repository fond in .git!"
            sys.exit()
        if os.path.exists(ISSUE_FILE):
            with open(ISSUE_FILE,'r') as issues:
                self.issue_db = pickle.load(issues)
        else:
            self.issue_db = {}
        if self.issue_db:
            self.max_id = max(self.issue_db)
        else:
            self.max_id = 0
    def __str__(self):
        "Prints all active issues."
        return (
            "\t".join(("id","Date", "Commit", "Status", "Prio", "Comment")) +
            "\n" + "-" * 70 + "\n" + 
            "\n".join(str(issue) for issue in sorted(self.issue_db.values())[::-1]
                      if issue.status == 'open'))
    def show_all(self):
        "Prints also closed issues."
        return (
            "\t".join(("id","Date", "Commit", "Status", "Prio", "Comment")) +
            "\n" + "-" * 70 + "\n" + 
            "\n".join(str(issue) for issue in self.issue_db.values()))
    def __repickle(self):
        "Rewrite database."
        with open(ISSUE_FILE, 'w') as issues:
            pickle.dump(self.issue_db, issues, -1)
    @staticmethod
    def __get_head_sha():
        "Get head commit's sha."
        return Repo('.').head.commit.hexsha
    @safe_tmp_textfile    
    def add_issue(self):
        "Add an issue."
        editor = os.getenv('EDITOR').split() or ['emacs']
        subprocess.call(editor + ['__issue__.msg'])
        if os.path.exists('__issue__.msg'):
            message = open('__issue__.msg','r')
            msg = message.read()
            sha = self.__get_head_sha()
            self.max_id += 1
            self.issue_db[self.max_id] = Issue(self.max_id, sha, msg)
            self.__repickle()
            message.close()
            print 'Added issue\n', self.issue_db[self.max_id]
        else:
            print 'Abort: Empty message!'
    @catch_id_err
    def set_prio(self, issue_id, prio):
        try:
            self.issue_db[issue_id].priority = int(prio)
            self.__repickle()
        except ValueError:
            print "Priority must be integer!"
    @catch_id_err
    def info(self, issue_id):
        "Get info on a specific issue."
        self.issue_db[issue_id].more_info()
    @catch_id_err
    def remove(self, issue_id):
        "Remove a specific issue."
        del self.issue_db[issue_id]
        self.__repickle()
    @catch_id_err
    def close(self, issue_id):
        "Close a specific issue."
        self.issue_db[issue_id].closedsha = self.__get_head_sha()
        self.issue_db[issue_id].status = 'closed'
        self.__repickle()
    @catch_id_err
    def re_add(self, issue_id):
        "Reset the sha to the latest commit."
        self.issue_db[issue_id].commitsha = self.__get_head_sha()
        self.__repickle()
    @safe_tmp_textfile
    @catch_id_err
    def edit(self, issue_id):
        "Change the message of an existing issue."
        with open('__issue__.msg', 'w') as message:
            message.write(self.issue_db[issue_id].msg)
        editor = os.getenv('EDITOR').split() or ['emacs']
        subprocess.call(editor + ['__issue__.msg'])
        message = open('__issue__.msg','r')
        msg = message.read()
        self.issue_db[issue_id].msg = msg
        self.__repickle()
        message.close()
            
class Issue(object):
    "Issue object."
    def __init__(self, myid, commitsha, msg):
        self.myid = myid
        self.commitsha = commitsha
        self.closedsha = ""
        self.msg = msg
        self.issued = datetime.datetime.now()
        self.status = 'open'
        self.priority = 3
    def __str__(self):
        msg = self.msg.split("\n")[0] # get the first line
        return "\t".join((
            "%03i" % self.myid,
             self.issued.strftime("%b %d"),
             self.commitsha[:5],
             self.status,
             str(self.priority),
             len(msg) > 30 and msg[:27] + "..." or msg))
    def __gt__(self, other):
        return self.myid > other.myid if self.priority == \
               other.priority else self.priority > other.priority
    def get_commit(self, sha = ""):
        "Get the corresponding commit object."
        repo = Repo('.')
        return repo.commit(sha or self.commitsha)
    def more_info(self):
        "Print detailed informaiton."
        print "Issue " + "%03i" % self.myid
        print "-"*70
        print ("Status: %s\n"
               "Date:   %s\n"
               "%s") % (
            self.status, self.issued.strftime("%a %b %d %H:%M %Y"),
            self.msg)
        if self.closedsha:
            print "-"*70
            print "Closed with:"
            self.__print_info(self.get_commit(self.closedsha))
        print "-"*70
        print "Opened:"
        self.__print_info(self.get_commit())
        
    @staticmethod
    def __print_info(commit):
        "Print info on commit."
        print ("commit  %s\n"
               "Author: %s\n"
               "Date:   %s\n") % (
            commit.hexsha, str(commit.author),
            time.asctime(time.gmtime(commit.committed_date)))
        print commit.message
    
