import git

# rorepo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with
repo = git.Repo()
modified_files = len(repo.index.diff(None))
count_staged_files = len(repo.index.diff("HEAD"))
print(modified_files, count_staged_files)