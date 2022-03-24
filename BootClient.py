from git import Repo
from git import RemoteProgress
from PyQt6 import QtWidgets

import sys

PATH_OF_GIT_REPO = r'C:\\Users\\mea25\\Desktop\\BootClient\\BootClient\\.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'Pyhon commit'

class ProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print("called")

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.git.add("env")
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        assert origin.exists()
        for push_info in origin.push(progress=ProgressPrinter()):
            print("%s; %s" % (push_info.ref, push_info.commit))
    except:
        print('Some error occured while pushing the code')    

def git_pull():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        origin = repo.remote(name='origin')
        origin.pull(progress=ProgressPrinter())
    except:
        print('Some error occured while pulling the code')

git_push()