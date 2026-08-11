import os
import subprocess
from datetime import datetime, timedelta

# Settings
days_to_backdate = 365
dummy_file = "contribution_history.txt"

# Ensure we are in a git repository
if not os.path.exists('.git'):
    print("Error: You must run this script inside a Git repository.")
    exit()

print(f"Starting to generate commits for the last {days_to_backdate} days...")
start_date = datetime.now() - timedelta(days=days_to_backdate)

for i in range(days_to_backdate + 1):
    commit_date = start_date + timedelta(days=i)
    date_str = commit_date.strftime("%Y-%m-%d 12:00:00")
    
    # Write a small change to a file so Git has something to commit
    with open(dummy_file, "a") as f:
        f.write(f"Contribution on {date_str}\n")
    
    # Stage the file
    subprocess.run(["git", "add", dummy_file], stdout=subprocess.DEVNULL)
    
    # Set the environment variables to trick Git into using the past date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    # Create the commit
    subprocess.run(
        ["git", "commit", "-m", f"Automated commit for {date_str}"], 
        env=env, 
        stdout=subprocess.DEVNULL
    )
    
    print(f"Created commit for {date_str}")

print("\nAll commits created successfully!")
print("Now run: git push origin main")
