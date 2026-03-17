import os
from dotenv import load_dotenv
from github import Github, Auth

# Load the .env file
load_dotenv()

# Get the token
token = os.getenv("GITHUB_TOKEN")

# Authenticate and test using the new method
try:
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user()
    print(f"Successfully authenticated as: {user.login}")
except Exception as e:
    print(f"Authentication failed: {e}")