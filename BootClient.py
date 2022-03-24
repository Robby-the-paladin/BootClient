from git import Repo

PATH_OF_GIT_REPO = r'C:\\Users\\mea25\\Desktop\\BootClient\\BootClient\\.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'Pyhon commit'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.git.add("BootClient.py")
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

git_push()