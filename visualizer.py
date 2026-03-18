import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_commit_heatmap(commits_df):
    """Generates a heatmap of commits by day of week and week of year."""
    if commits_df.empty:
        return None
        
    # Group by week and day_of_week, count commits
    heatmap_data = commits_df.groupby(['day_of_week', 'week']).size().unstack(fill_value=0)
    
    # Ensure all 7 days are present
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    heatmap_data = heatmap_data.reindex(range(7), fill_value=0)
    heatmap_data.index = days

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 3))
    sns.heatmap(heatmap_data, cmap="Greens", linewidths=.5, ax=ax, cbar_kws={'label': 'Commits'})
    ax.set_title("Commit Activity Heatmap")
    ax.set_xlabel("Week of Year")
    ax.set_ylabel("")
    
    return fig

def plot_code_frequency(code_freq_df):
    """Generates a line chart showing lines added vs deleted over time."""
    if code_freq_df.empty:
        return None

    # Group by week and sum additions/deletions
    weekly_data = code_freq_df.groupby('week_timestamp')[['additions', 'deletions']].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Plot additions (green) and deletions (red)
    ax.plot(weekly_data['week_timestamp'], weekly_data['additions'], label='Additions', color='green')
    ax.plot(weekly_data['week_timestamp'], weekly_data['deletions'], label='Deletions', color='red')
    
    # Format the chart
    ax.set_title("Code Frequency (Additions vs Deletions)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Lines of Code")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    
    return fig

def plot_repo_distribution(commits_df):
    """Generates a pie chart of the top 5 most active repositories."""
    if commits_df.empty:
        return None

    # Count commits per repo, get top 5
    repo_counts = commits_df['repo'].value_counts().head(5)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(repo_counts.values, labels=repo_counts.index, autopct='%1.1f%%', startangle=90, cmap="Set3")
    ax.set_title("Top 5 Active Repositories")
    
    return fig