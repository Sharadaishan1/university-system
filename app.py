import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="UniEvent System", layout="wide")

DATA_FILE = "events.csv"

# Load existing events or create empty DataFrame
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Event Name", "Category", "Date", "Venue", "Description"])

# Save events to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

st.title("🎓 UniEvent System - University Event Finder")

# Sidebar - Add Event Form
st.sidebar.header("➕ Add New Event")
event_name = st.sidebar.text_input("Event Name")
category = st.sidebar.selectbox("Category", ["Academic", "Sports", "Cultural", "Tech", "Workshops"])
date = st.sidebar.date_input("Event Date")
venue = st.sidebar.text_input("Venue")
description = st.sidebar.text_area("Description")

if st.sidebar.button("Add Event"):
    if event_name and venue:
        new_event = pd.DataFrame({
            "Event Name": [event_name],
            "Category": [category],
            "Date": [str(date)],
            "Venue": [venue],
            "Description": [description]
        })
        df = pd.concat([df, new_event], ignore_index=False)
        save_data(df)
        st.sidebar.success(f"Successfully added '{event_name}'!")
        st.rerun()
    else:
        st.sidebar.error("Please fill in Event Name and Venue!")

# Search & Filter Section
st.header("📌 Upcoming Events")

col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input("🔍 Search Event Name or Venue")
with col2:
    filter_category = st.selectbox("Filter by Category", ["All"] + list(df["Category"].unique() if not df.empty else []))

# Apply Filters
filtered_df = df.copy()
if search_query and not filtered_df.empty:
    filtered_df = filtered_df[
        filtered_df["Event Name"].str.contains(search_query, case=False, na=False) |
        filtered_df["Venue"].str.contains(search_query, case=False, na=False)
    ]
if filter_category != "All" and not filtered_df.empty:
    filtered_df = filtered_df[filtered_df["Category"] == filter_category]

# Display Events
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"🗓️ {row['Event Name']} - ({row['Category']})"):
            st.write(f"**Date:** {row['Date']}")
            st.write(f"**Venue:** {row['Venue']}")
            st.write(f"**Description:** {row['Description']}")
else:
    st.info("No events found matching your criteria.")
