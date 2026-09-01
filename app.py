import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="UniEvent System",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for modern UI design
st.markdown("""
    <style>
    /* Main background & typography */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Custom Header Card */
    .header-card {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .header-card h1 {
        color: white !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .header-card p {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Metric cards for stats */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #4F46E5;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Event Expander Cards */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        font-weight: 600;
        color: #1f2937;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "events.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Event Name", "Category", "Date", "Venue", "Description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# Custom Styled Banner Header
st.markdown("""
    <div class="header-card">
        <h1>🎓 UniEvent System</h1>
        <p>Discover, explore, and participate in campus events effortlessly</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Form
st.sidebar.header("➕ Add New Event")
event_name = st.sidebar.text_input("Event Name")
category = st.sidebar.selectbox("Category", ["Academic", "Sports", "Cultural", "Tech", "Workshops"])
date = st.sidebar.date_input("Event Date")
venue = st.sidebar.text_input("Venue")
description = st.sidebar.text_area("Description")

if st.sidebar.button("Add Event", use_container_width=True):
    if event_name and venue:
        new_event = pd.DataFrame({
            "Event Name": [event_name],
            "Category": [category],
            "Date": [str(date)],
            "Venue": [venue],
            "Description": [description]
        })
        df = pd.concat([df, new_event], ignore_index=True)
        save_data(df)
        st.sidebar.success(f"Successfully added '{event_name}'!")
        st.rerun()
    else:
        st.sidebar.error("Please fill in Event Name and Venue!")

# Quick Stats Overview
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.metric("Total Events", len(df))
with col_stat2:
    st.metric("Categories", len(df["Category"].unique()) if not df.empty else 0)
with col_stat3:
    st.metric("Next Up", df["Event Name"].iloc[-1] if not df.empty else "None")

st.divider()

# Search & Filter
st.subheader("🔍 Find Events")
col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input("Search by Event Name or Venue", placeholder="Type event name or location...")
with col2:
    filter_category = st.selectbox("Filter by Category", ["All"] + list(df["Category"].unique() if not df.empty else []))

# Data Filter Logic
filtered_df = df.copy()
if search_query and not filtered_df.empty:
    filtered_df = filtered_df[
        filtered_df["Event Name"].str.contains(search_query, case=False, na=False) |
        filtered_df["Venue"].str.contains(search_query, case=False, na=False)
    ]
if filter_category != "All" and not filtered_df.empty:
    filtered_df = filtered_df[filtered_df["Category"] == filter_category]

# Display List
st.write("")
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"📌 {row['Event Name']} — [{row['Category']}]"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"📅 **Date:** {row['Date']}")
            with col_b:
                st.write(f"📍 **Venue:** {row['Venue']}")
            st.write(f"📝 **Description:** {row['Description']}")
else:
    st.info("No events found. Be the first to add one from the sidebar!")
