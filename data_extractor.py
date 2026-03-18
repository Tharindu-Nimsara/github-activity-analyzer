import os
from dotenv import load_dotenv
from github import Github, Auth

# 1. Setup and Authenticate
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
auth = Auth.Token(token)
g = Github(auth=auth)

def fetch_github_data(target_username):
    print(f"Fetching data for user: {target_username}...\n")
    
    # Data storage lists
    commit_data = []
    code_freq_data = []

    try:
        user = g.get_user(target_username)
        repos = user.get_repos()

        for repo in repos:
            print(f"Analyzing repo: {repo.name}")
            
            # 2. Fetch Commits
            try:
                commits = repo.get_commits(author=target_username)
                for commit in commits:
                    commit_data.append({
                        "repo": repo.name,
                        "date": commit.commit.author.date
                    })
            except Exception as e:
                print(f"  - Skipping commits (Repo might be empty): {e}")

            # 3. Fetch Code Frequency
            try:
                # Returns list of [timestamp, additions, deletions] per week
                weeks = repo.get_stats_code_frequency() 
                if weeks:
                    for week in weeks:
                        code_freq_data.append({
                            "repo": repo.name,
                            "week_timestamp": week.week,
                            "additions": week.additions,
                            "deletions": week.deletions
                        })
            except Exception as e:
                print(f"  - Skipping code frequency: {e}")

        print("\nData extraction complete!")
        print(f"Total Commits Found: {len(commit_data)}")
        print(f"Total Weeks of Code Freq Found: {len(code_freq_data)}")
        
        return commit_data, code_freq_data

    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None, None

# Test the function (Replace with your GitHub username)
if __name__ == "__main__":
    my_username = "Tharindu-Nimsara" 
    commits, code_freq = fetch_github_data(my_username)