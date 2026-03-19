import streamlit as st
from data_extractor import fetch_github_data
from data_processor import process_commits, process_code_frequency
from visualizer import plot_commit_heatmap, plot_code_frequency, plot_repo_distribution

# 1. Page Configuration
st.set_page_config(page_title="GitHub Analyzer", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] {
            position: relative;
            overflow: hidden;
            background:
                radial-gradient(1200px 500px at 90% -10%, rgba(56, 189, 248, 0.12), transparent 60%),
                radial-gradient(900px 450px at -10% 20%, rgba(99, 102, 241, 0.14), transparent 60%),
                linear-gradient(180deg, #020617 0%, #020617 100%);
        }
        [data-testid="stAppViewContainer"]::before,
        [data-testid="stAppViewContainer"]::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
        }
        [data-testid="stAppViewContainer"]::before {
            opacity: 0.28;
            background-image:
                radial-gradient(circle at 15% 20%, rgba(56, 189, 248, 0.8) 1.2px, transparent 2px),
                radial-gradient(circle at 75% 35%, rgba(129, 140, 248, 0.75) 1px, transparent 2px),
                radial-gradient(circle at 45% 80%, rgba(94, 234, 212, 0.75) 1.1px, transparent 2px);
            background-size: 220px 220px, 260px 260px, 300px 300px;
            animation: particlesDrift 28s linear infinite;
        }
        [data-testid="stAppViewContainer"]::after {
            opacity: 0.2;
            background-image:
                radial-gradient(circle at 25% 30%, rgba(56, 189, 248, 0.6) 0.9px, transparent 2px),
                radial-gradient(circle at 85% 70%, rgba(34, 211, 238, 0.6) 0.9px, transparent 2px);
            background-size: 320px 320px, 360px 360px;
            animation: particlesDriftReverse 36s linear infinite;
        }
        @keyframes particlesDrift {
            from { transform: translateY(0px) translateX(0px); }
            to { transform: translateY(-80px) translateX(40px); }
        }
        @keyframes particlesDriftReverse {
            from { transform: translateY(0px) translateX(0px); }
            to { transform: translateY(70px) translateX(-35px); }
        }
        .block-container {
            position: relative;
            z-index: 1;
            padding-top: 1.5rem;
            padding-bottom: 4.5rem;
            font-size: 1.1rem;
        }
        .hero-card {
            background: linear-gradient(135deg, rgba(37,99,235,0.18), rgba(6,182,212,0.16));
            border: 1px solid rgba(125, 211, 252, 0.32);
            border-radius: 18px;
            padding: 1.35rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 0 28px rgba(56, 189, 248, 0.10);
        }
        .hero-card h2 {
            font-size: 2.3rem;
            letter-spacing: 0.3px;
        }
        .hero-card p {
            font-size: 1.12rem;
        }
        .input-panel {
            border-radius: 18px;
            border: 1px solid rgba(125, 211, 252, 0.26);
            background: linear-gradient(160deg, rgba(15,23,42,0.82), rgba(30,41,59,0.52));
            box-shadow: 0 0 24px rgba(14, 165, 233, 0.14);
            padding: 1.25rem 1rem 1.1rem 1rem;
            margin: 0.4rem 0 1.1rem 0;
        }
        .input-panel h3 {
            margin: 0;
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            color: #e2e8f0;
        }
        .input-panel p {
            margin: 0.35rem 0 0.7rem 0;
            text-align: center;
            color: #cbd5e1;
            font-size: 1.22rem;
        }
        .metric-shell {
            border: 1px solid rgba(148,163,184,0.25);
            border-radius: 14px;
            padding: 0.2rem 0.4rem;
            background: rgba(15,23,42,0.02);
        }
        .stSubheader {
            font-size: 1.55rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 1.08rem;
        }
        [data-testid="stMetricValue"] {
            font-size: 2rem;
        }
        .stTextInput > div {
            max-width: 560px;
            margin-left: auto;
            margin-right: auto;
        }
        .stTextInput label {
            font-size: 1.55rem;
            font-weight: 600;
            text-align: center;
            display: block;
        }
        .stTextInput label p {
            font-size: 1.55rem !important;
            margin-bottom: 0.35rem;
        }
        .stTextInput input {
            border: 1px solid rgba(125, 211, 252, 0.45) !important;
            background: rgba(15, 23, 42, 0.74) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.12), 0 0 16px rgba(56, 189, 248, 0.12);
            font-size: 1.34rem !important;
            height: 3.5rem !important;
            line-height: 3.5rem !important;
            padding: 0 0.9rem !important;
            box-sizing: border-box;
            text-align: center;
        }
        .stTextInput input::placeholder {
            line-height: 3.5rem;
            text-align: center;
        }
        .stButton {
            display: flex;
            justify-content: center;
            margin-top: 0.35rem;
        }
        .stButton > button {
            min-width: 270px;
            min-height: 3.35rem;
            font-size: 1.5rem;
            font-weight: 700;
            border-radius: 12px;
            color: #e2e8f0;
            border: 1px solid rgba(125, 211, 252, 0.65);
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.28), rgba(59, 130, 246, 0.22));
            box-shadow: 0 0 10px rgba(56,189,248,0.34), inset 0 0 10px rgba(125,211,252,0.12);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            animation: aiGlow 2.3s ease-in-out infinite;
        }
        .stButton > button:hover {
            transform: translateY(-1px) scale(1.01);
            box-shadow: 0 0 16px rgba(56,189,248,0.55), inset 0 0 12px rgba(125,211,252,0.22);
        }
        @keyframes aiGlow {
            0% { box-shadow: 0 0 8px rgba(56,189,248,0.25), inset 0 0 9px rgba(125,211,252,0.10); }
            50% { box-shadow: 0 0 20px rgba(56,189,248,0.58), inset 0 0 14px rgba(125,211,252,0.24); }
            100% { box-shadow: 0 0 8px rgba(56,189,248,0.25), inset 0 0 9px rgba(125,211,252,0.10); }
        }
        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
            .hero-card {
                padding: 1rem 0.8rem;
            }
            .hero-card h2 {
                font-size: 1.9rem;
            }
            .input-panel h3 {
                font-size: 1.5rem;
            }
            .stTextInput > div {
                max-width: 100%;
            }
            .stButton > button {
                min-width: 200px;
                width: 100%;
            }
        }
        .app-footer {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 999;
            padding: 0.65rem 1rem;
            border-top: 1px solid rgba(148,163,184,0.25);
            background: rgba(2, 6, 23, 0.86);
            backdrop-filter: blur(4px);
            text-align: center;
            font-size: 0.9rem;
            opacity: 0.85;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h2 style="margin:0;">📊 GitHub Activity Analyzer</h2>
        <p style="margin:0.45rem 0 0 0; opacity:0.9;">
            Analyze developer productivity, commit history, and code frequency with a clean, responsive dashboard.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 2. User Input
# Defaulting to your username for easy testing
center_col_left, center_col_mid, center_col_right = st.columns([1, 2, 1])
with center_col_mid:
    st.markdown(
        """
        <div class="input-panel">
            <h3>⚡ GitHub Activity Scan</h3>
            <p>Enter a username and generate a smart activity report.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    username = st.text_input("Enter a GitHub Username:", value="", placeholder="")
    btn_left, btn_mid, btn_right = st.columns([1, 1, 1])
    with btn_mid:
        generate_clicked = st.button("Generate Report")

# 3. Trigger Dashboard Generation
if generate_clicked:
    if not username:
        st.warning("Please enter a username.")
    else:
        progress_container = st.container()
        progress_placeholder = progress_container.empty()
        progress_lines = []

        def on_progress(message):
            progress_lines.append(message)
            progress_placeholder.code("\n".join(progress_lines[-12:]), language="text")

        with st.spinner(f"Fetching and processing data for {username}..."):
            # Execute Phase 2: Extraction
            commits_raw, code_freq_raw = fetch_github_data(username, progress_callback=on_progress)
            
            if not commits_raw and not code_freq_raw:
                st.error("No data found or API limit reached. Check your terminal for details.")
            else:
                # Execute Phase 3: Processing
                commits_df = process_commits(commits_raw)
                code_freq_df = process_code_frequency(code_freq_raw)
                
                # 4. Render Top-Level Metrics
                st.subheader("Key Metrics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown('<div class="metric-shell">', unsafe_allow_html=True)
                    total_commits = len(commits_df) if not commits_df.empty else 0
                    st.metric("Total Commits Found", total_commits)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="metric-shell">', unsafe_allow_html=True)
                    active_repos = commits_df['repo'].nunique() if not commits_df.empty else 0
                    st.metric("Active Repositories", active_repos)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="metric-shell">', unsafe_allow_html=True)
                    total_added = code_freq_df['additions'].sum() if not code_freq_df.empty else 0
                    st.metric("Total Lines Added", f"{total_added:,}")
                    st.markdown('</div>', unsafe_allow_html=True)

                st.divider()

                # 5. Render Visualizations (Phase 4)
                st.subheader("Commit Activity Heatmap")
                if not commits_df.empty:
                    fig_heatmap = plot_commit_heatmap(commits_df)
                    if fig_heatmap:
                        st.pyplot(fig_heatmap, width='content')
                else:
                    st.info("No commit data available to generate heatmap.")
                
                st.divider()
                
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    st.subheader("Code Frequency Over Time")
                    if not code_freq_df.empty:
                        fig_code = plot_code_frequency(code_freq_df)
                        if fig_code:
                            st.pyplot(fig_code, width='stretch')
                    else:
                        st.info("No code frequency data available.")
                        
                with col_viz2:
                    st.subheader("Top 5 Active Repositories")
                    if not commits_df.empty:
                        fig_pie = plot_repo_distribution(commits_df)
                        if fig_pie:
                            st.pyplot(fig_pie, width='stretch')

                progress_placeholder.empty()

st.markdown(
    """
    <div class="app-footer">
        Built with ❤️ using Streamlit · GitHub Activity Analyzer
    </div>
    """,
    unsafe_allow_html=True,
)