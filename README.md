# GitHub Activity Analyzer

A Streamlit dashboard that analyzes a GitHub user's activity and visualizes:

- Commit patterns over time (heatmap)
- Weekly code additions/deletions (line chart)
- Top active repositories (pie chart)
- Summary metrics (total commits, active repositories, total lines added)

## Live Demo

Web URL: https://githu8-activity-analyzer.streamlit.app/

## Features

- Clean, responsive Streamlit UI with custom styling
- GitHub API data extraction using `PyGithub`
- Commit and code frequency processing with `pandas`
- Visual analytics using `matplotlib` and `seaborn`
- Progress logs shown in-app while data is being fetched

## Project Structure

```text
github-analyzer/
├── app.py               # Streamlit entrypoint and UI
├── data_extractor.py    # GitHub authentication + data extraction
├── data_processor.py    # Data transformation with pandas
├── visualizer.py        # Chart generation (heatmap/line/pie)
├── test_auth.py         # Quick token authentication check
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (local only)
```

## How It Works

1. **Input Username**: User enters a GitHub username in the Streamlit app.
2. **Extract Data** (`data_extractor.py`):
   - Loads `GITHUB_TOKEN` from `.env`
   - Authenticates with GitHub
   - Iterates through user repositories
   - Collects:
     - Commit metadata (`repo`, `date`)
     - Weekly code frequency (`week_timestamp`, `additions`, `deletions`)
3. **Process Data** (`data_processor.py`):
   - Converts raw lists to DataFrames
   - Parses timestamps/datetimes
   - Derives analysis columns for visualization
4. **Visualize Data** (`visualizer.py`):
   - Commit heatmap (day of week × week of year)
   - Additions vs deletions over time
   - Top 5 active repositories
5. **Render Dashboard** (`app.py`):
   - Displays key metrics and charts
   - Shows progress logs during fetch/processing

## Prerequisites

- Python 3.10+ (recommended)
- A GitHub Personal Access Token with read access to repositories/activity

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Tharindu-Nimsara/github-activity-analyzer.git
   cd github-activity-analyzer
   ```

2. Create and activate a virtual environment:

   **Windows (PowerShell):**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token
```

> Keep your token private. Do not commit `.env` to source control.

## Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Authentication Test (Optional)

Use the helper script to verify token setup:

```bash
python test_auth.py
```

Expected success output:

```text
Successfully authenticated as: <your_username>
```

## Dashboard Outputs

After generating a report, the app shows:

- **Key Metrics**
  - Total Commits Found
  - Active Repositories
  - Total Lines Added
- **Commit Activity Heatmap**
  - Commits by day of week and week of year
- **Code Frequency Over Time**
  - Weekly additions vs deletions
- **Top 5 Active Repositories**
  - Distribution by commit count

## Notes & Limitations

- GitHub API rate limits can affect data retrieval.
- Some repositories may not return stats (e.g., empty/inactive repos).
- Code frequency data depends on GitHub-generated repository statistics availability.

## Tech Stack

- **Frontend/App**: Streamlit
- **Data Access**: PyGithub, python-dotenv
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn

## Troubleshooting

- **"No data found or API limit reached"**
  - Check `GITHUB_TOKEN` validity and scopes.
  - Retry after API rate limit reset.
- **Authentication failed**
  - Recreate token and update `.env`.
  - Run `python test_auth.py` to verify credentials.
- **Missing dependencies**
  - Re-run `pip install -r requirements.txt` inside your active virtual environment.

## License

No license file is currently included in this repository.


## Author

Developed by Tharindu Nimsara.

## Demo video

https://github.com/user-attachments/assets/2018c7e4-5dc6-4310-92b6-c4f0f77d5a64

