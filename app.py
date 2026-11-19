import streamlit as st  # type: ignore
import preprocessor, helper
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="WhatsApp Chat Analyser", layout="wide")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* ── Sidebar ─────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }

    /* Sidebar app title */
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: 0.02em;
        margin-bottom: 0.2rem;
    }
    .sidebar-subtitle {
        font-size: 0.72rem;
        color: #94a3b8;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 1.4rem;
    }

    /* Sidebar upload label */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label p {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
    }

    /* Sidebar selectbox label */
    [data-testid="stSidebar"] .stSelectbox label p {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
    }

    /* Sidebar selectbox box */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        color: #f1f5f9 !important;
    }

    /* Sidebar file uploader box */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background-color: #1e293b !important;
        border: 1px dashed #475569 !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
    }

    /* Sidebar divider */
    .sidebar-divider {
        border: none;
        border-top: 1px solid #334155;
        margin: 1rem 0;
    }

    /* Run Analysis button */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        width: 100%;
        padding: 0.65rem 1rem;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        cursor: pointer;
        transition: opacity 0.2s, transform 0.1s;
        box-shadow: 0 2px 8px rgba(37,99,235,0.35);
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(0);
    }

    /* Sidebar info chip */
    .info-chip {
        display: inline-block;
        background: #1e3a5f;
        color: #93c5fd;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 3px 10px;
        border-radius: 999px;
        border: 1px solid #2563eb44;
        margin-bottom: 1rem;
    }

    /* ── Main Area ───────────────────────────────────────── */
    .main { background-color: #f8fafc; }

    /* Section labels */
    .section-title {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 0.5rem;
        margin-top: 0.1rem;
    }

    /* Page title */
    .page-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.1rem;
    }
    .page-meta {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 0.5rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        box-shadow: 0 1px 4px rgba(15,23,42,0.06);
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.7rem !important;
        color: #64748b !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }

    /* Divider */
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib theme ──────────────────────────────────────────────────────────
mpl.rcParams.update({
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.grid':         False,
    'axes.labelcolor':   '#374151',
    'xtick.color':       '#6b7280',
    'ytick.color':       '#6b7280',
    'xtick.labelsize':   7,
    'ytick.labelsize':   7,
    'font.family':       'DejaVu Sans',
    'figure.facecolor':  '#ffffff',
    'axes.facecolor':    '#ffffff',
})

BLUE   = '#2563eb'
PURPLE = '#7c3aed'
TEAL   = '#0891b2'
AMBER  = '#d97706'
RED    = '#dc2626'

def section(label):
    st.markdown(f'<p class="section-title">{label}</p>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">WhatsApp Chat Analyser</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Conversation Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload chat export", type=["txt"])

    if uploaded_file is not None:
        data = uploaded_file.getvalue().decode("utf-8")
        df   = preprocessor.preprocess(data)

        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        
        user_list.sort()
        user_list.insert(0, "Overall")

        total_members = len(user_list) - 1  # exclude "Overall"
        st.markdown(f'<span class="info-chip">{total_members} members &nbsp;·&nbsp; {df.shape[0]:,} messages</span>',
                    unsafe_allow_html=True)

        selected_user = st.selectbox("Analyse by", user_list)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        run = st.button("Run Analysis")

# ── Main content ──────────────────────────────────────────────────────────────
if uploaded_file is not None and run:

    # Page title
    st.markdown('<p class="page-title">Chat Analysis</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="page-meta">Analysing: <strong>{selected_user}</strong> &nbsp;|&nbsp; '
        f'{df.shape[0]:,} messages &nbsp;|&nbsp; {df[df["user"] != "group_notification"]["user"].nunique()} members</p>',
        unsafe_allow_html=True
    )
    st.divider()

    # ── Summary ───────────────────────────────────────────────────────────────
    section("Summary")
    num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Messages", f"{num_messages:,}")
    c2.metric("Total Words",    f"{words:,}")
    c3.metric("Media Shared",   f"{num_media:,}")
    c4.metric("Links Shared",   f"{num_links:,}")

    st.divider()

    # ── Timelines ─────────────────────────────────────────────────────────────
    section("Timelines")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Monthly Timeline**")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(timeline['time'], timeline['message'],
                color=BLUE, linewidth=1.8, marker='o', markersize=3)
        ax.fill_between(range(len(timeline)), timeline['message'], alpha=0.08, color=BLUE)
        ax.set_xticks(range(len(timeline)))
        ax.set_xticklabels(timeline['time'], rotation=45, ha='right', fontsize=7)
        ax.set_ylabel("Messages")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    with c2:
        st.markdown("**Daily Timeline**")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(daily['only_date'], daily['message'], color=TEAL, linewidth=0.9)
        ax.fill_between(daily['only_date'], daily['message'], alpha=0.07, color=TEAL)
        plt.xticks(rotation=45, ha='right', fontsize=6)
        ax.set_ylabel("Messages")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    st.divider()

    # ── Activity Map ──────────────────────────────────────────────────────────
    section("Activity Map")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**By Day of Week**")
        busy_day = helper.week_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(busy_day.index, busy_day.values, color=PURPLE, width=0.6)
        plt.xticks(rotation=30, ha='right', fontsize=7)
        ax.set_ylabel("Messages")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    with c2:
        st.markdown("**By Month**")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(busy_month.index, busy_month.values, color=AMBER, width=0.6)
        plt.xticks(rotation=30, ha='right', fontsize=7)
        ax.set_ylabel("Messages")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    with c3:
        st.markdown("**Hourly Heatmap**")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(user_heatmap, ax=ax, cmap='Blues',
                    linewidths=0.4, linecolor='#f8fafc',
                    cbar_kws={'shrink': 0.8})
        ax.set_xlabel("Hour Range", fontsize=7)
        ax.set_ylabel("Day", fontsize=7)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    st.divider()

    # ── Most Active Members ───────────────────────────────────────────────────
    if selected_user == 'Overall':
        section("Most Active Members")
        x, new_df = helper.most_busy_users(df)
        c1, c2 = st.columns([1.6, 1])

        with c1:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(x.index, x.values, color=RED, width=0.6)
            plt.xticks(rotation=30, ha='right', fontsize=7)
            ax.set_ylabel("Messages")
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

        with c2:
            st.dataframe(new_df, use_container_width=True, hide_index=True)

        st.divider()

    # ── Word Analysis ─────────────────────────────────────────────────────────
    section("Word Analysis")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Word Cloud**")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    with c2:
        st.markdown("**Top 20 Words**")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))        
        print(most_common_df.columns)
        print(most_common_df.head())
        ax.barh(most_common_df['word'][::-1],
                most_common_df['frequency'][::-1],
                color=TEAL,
                height=0.6)
        ax.set_xlabel("Frequency")
        ax.grid(axis='y', visible=False)
        plt.tight_layout()
        st.pyplot(fig);
        
    df_wc = helper.create_wordcloud(selected_user, df)

    if df_wc is not None:
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No meaningful words available for word cloud.")

    most_common_df = helper.most_common_words(selected_user, df)

    if not most_common_df.empty:
        fig, ax = plt.subplots()
        ax.bar(most_common_df['word'], most_common_df['frequency'])
        plt.xticks(rotation=90)
        st.pyplot(fig)
    else:
        st.info("No meaningful words available for this user.")