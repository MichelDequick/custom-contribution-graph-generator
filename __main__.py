import os
import progressbar
import argparse
from git import *
from argparse import RawTextHelpFormatter
from datetime import datetime
from datetime import timedelta
from lib.pixelgrid import PixelGrid

# Generate bogus commit function
def generate_bogus_commits(repo, date, amount):
    commit_date = date.strftime('%Y-%m-%d %H:%M:%S')
    os.environ['GIT_AUTHOR_DATE'] = commit_date
    os.environ['GIT_COMMITTER_DATE'] = commit_date
    for i in range(amount):
        repo.index.commit('bogus-commit', commit_date=commit_date)

# Argument definiton
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Gennerate repository with bogus commits for a custom contribution graph',
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument('repo_name', type=str,
                    help='repository to create')
parser.add_argument('-m', '--max-commits-a-day', type=int,
                    default='100',
                    help='Maximum amount of commits a day \n(Default: 100)')
parser.add_argument('-y', '--year', type=int,
                    default='2020',
                    help='specify a specific year \nExample: 2010, 2018, 2020 \n(Default: one year ago today)')
args = parser.parse_args()

repo_name = args.repo_name
max_commits = args.max_commits_a_day

# Movinng working directory
headpath = os.path.abspath(__file__)
headdir = os.path.dirname(headpath)
os.chdir(headdir)

# Create repo that will contain bogus commits
repo = Repo.init(os.path.join(repo_name))

# Set start date
if args.year:
    start_date = datetime(args.year, 1, 1)
else:
    start_date = datetime.today() - timedelta(days=364)

# Move to first suunday after start day
while start_date.weekday() != 6:
    start_date += timedelta(days=1)

# Prompt for user drawing
os.system('cls')
print('Use GUI to draw your custom banner')
grid = PixelGrid((52, 7), 0.9).getGrid()

# Print user drawing in console
print('Your design: \n')
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] != 0:
            print('██', end='')
        else:
            print('░░', end='')
    print()
print()

# Create commits
print('creating commits...')
current_date = start_date
for j in progressbar.progressbar(range(len(grid[0]))):
    for i in range(len(grid)):
        if grid[i][j] != 0:
            generate_bogus_commits(repo, current_date, max_commits)
        current_date += timedelta(days=1)

# Done!
print('Now push the "' + str(repo_name) + '" repository to github!')
