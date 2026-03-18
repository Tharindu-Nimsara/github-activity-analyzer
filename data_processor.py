import pandas as pd

def process_commits(commit_data):
    """Converts raw commit lists into a clean DataFrame."""
    if not commit_data:
        return pd.DataFrame()
    
    # 1. Load data into Pandas
    df = pd.DataFrame(commit_data)
    
    # 2. Convert raw strings to Datetime objects
    df['date'] = pd.to_datetime(df['date'], utc=True)
    
    # 3. Extract time components for the heatmap
    df['date_only'] = df['date'].dt.date
    df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['week'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year
    
    return df

def process_code_frequency(code_freq_data):
    """Converts raw code frequency lists into a clean DataFrame."""
    if not code_freq_data:
        return pd.DataFrame()
        
    df = pd.DataFrame(code_freq_data)
    
    # 1. Convert GitHub UNIX timestamps to Datetime
    df['week_timestamp'] = pd.to_datetime(df['week_timestamp'], unit='s')
    
    # 2. Calculate net code (Note: GitHub deletions are already negative numbers)
    df['net_code'] = df['additions'] + df['deletions']
    
    return df

# Quick test to verify it works with your extractor
if __name__ == "__main__":
    from data_extractor import fetch_github_data
    
    username = "Tharindu-Nimsara" 
    commits_raw, code_freq_raw = fetch_github_data(username)
    
    if commits_raw:
        commits_df = process_commits(commits_raw)
        print("\n--- Processed Commits DataFrame ---")
        print(commits_df.head()) # Shows the first 5 rows
        
    if code_freq_raw:
        code_freq_df = process_code_frequency(code_freq_raw)
        print("\n--- Processed Code Frequency DataFrame ---")
        print(code_freq_df.head())