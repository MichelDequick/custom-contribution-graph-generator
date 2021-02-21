import os
from git import *
from datetime import datetime
from datetime import timedelta
from PixelGrid import PixelGrid
import progressbar

repo_name = "custom-contribution-graph-generator"
max_commits = 100   # commits per day

# Create a dummy repo
r = Repo.init(os.path.join(repo_name))

# Calculate start date
start_date = datetime.today() - timedelta(days=364) 
while start_date.weekday() != 6:    # Move one day forward untill sunday
    start_date += timedelta(days=1)

def create_bogus_commits(date, amount):
    commit_date = date.strftime('%Y-%m-%d %H:%M:%S')
    os.environ["GIT_AUTHOR_DATE"] = commit_date
    os.environ["GIT_COMMITTER_DATE"] = commit_date
    for i in range(amount):
        #r.index.add(dummy_file.name)
        r.index.commit("bogus-commit", commit_date=commit_date)

# Inital commit
create_bogus_commits(start_date - timedelta(days=1), 1)

# Prompt for a drawing
grid = PixelGrid((52, 7), 0.9).getGrid()

# Creating commits
print("creating commits...")
current_date = start_date
for j in progressbar.progressbar(range((len(grid[0])))):
    for i in range(len(grid)):
        if grid[i][j] != 0:
            create_bogus_commits(current_date, max_commits)
        current_date += timedelta(days=1)

print("Now push the repository to github!")