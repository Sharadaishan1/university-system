import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="UniEvent System",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .header-card {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .header-card h1 { color: white !important; font-weight: 800; margin-bottom: 0.5rem; }
    .header-card p { font-size: 1.1rem; opacity: 0.9; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #4F46E5; }
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e5e7eb; }
    </style>
""", unsafe_allow_html=True)

EVENTS_FILE = "events.csv"
RSVP_FILE = "rsvps.csv"

# Data Loaders
def load_events():
    if os.path.exists(EVENTS_FILE):
        return pd.read_csv(EVENTS_FILE)
    return pd.DataFrame(columns=["Event Name", "Category", "Date", "Venue", "Description"])

def load_rsvps():
    if os.path.exists(RSVP_FILE):
        return pd.read_csv(RSVP_FILE)
    return pd.DataFrame(columns=["Event Name", "Student Name", "Student ID", "Email"])

def save_events(df):
    df.to_csv(EVENTS_FILE, index=False)

def save_rsvps(df):
    df.to_csv(RSVP_FILE, index=False)

df_events = load_events()
df_rsvps = load_rsvps()

# Banner Header
st.markdown("""
    <div class="header-card">
        <h1>🎓 UniEvent System</h1>
        <p>Discover events, register your spot, and keep track of campus activities!</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar - Add Event
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
        df_events = pd.concat([df_events, new_event], ignore_index=True)
        save_events(df_events)
        st.sidebar.success(f"Successfully added '{event_name}'!")
        st.rerun()
    else:
        st.sidebar.error("Please fill in Event Name and Venue!")

# Stats
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.metric("Total Events", len(df_events))
with col_stat2:
    st.metric("Total Registrations", len(df_rsvps))
with col_stat3:
    st.metric("Categories", len(df_events["Category"].unique()) if not df_events.empty else 0)

st.divider()

# Search & Filter
st.subheader("🔍 Explore & Register for Events")
col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input("Search by Event Name or Venue", placeholder="Type event name or venue...")
with col2:
    filter_category = st.selectbox("Filter by Category", ["All"] + list(df_events["Category"].unique() if not df_events.empty else []))

# Filter Logic
filtered_df = df_events.copy()
if search_query and not filtered_df.empty:
    filtered_df = filtered_df[
        filtered_df["Event Name"].str.contains(search_query, case=False, na=False) |
        filtered_df["Venue"].str.contains(search_query, case=False, na=False)
    ]
if filter_category != "All" and not filtered_df.empty:
    filtered_df = filtered_df[filtered_df["Category"] == filter_category]

# Events List with RSVP Form
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"📌 {row['Event Name']} — [{row['Category']}]"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"📅 **Date:** {row['Date']}")
                st.write(f"📍 **Venue:** {row['Venue']}")
                st.write(f"📝 **Description:** {row['Description']}")
            
            with col_b:
                # RSVP Section
                st.subheader("🎟️ Register for this Event")
                with st.form(key=f"rsvp_form_{idx}"):
                    student_name = st.text_input("Full Name")
                    student_id = st.text_input("Student ID Number")
                    email = st.text_input("Email Address")
                    submit_rsvp = st.form_submit_button("Confirm RSVP")

                    if submit_rsvp:
                        if student_name and email:
                            new_rsvp = pd.DataFrame({
                                "Event Name": [row["Event Name"]],
                                "Student Name": [student_name],
                                "Student ID": [student_id],
                                "Email": [email]
                            })
                            df_rsvps = pd.concat([df_rsvps, new_rsvp], ignore_index=True)
                            save_rsvps(df_rsvps)
                            st.success("RSVP Successful! See you at the event.")
                            st.rerun()
                        else:
                            st.error("Please enter Name and Email!")

            # Delete Button
            st.divider()
            if st.button(f"🗑️ Delete Event '{row['Event Name']}'", key=f"del_{idx}"):
                df_events = df_events.drop(idx).reset_index(drop=True)
                save_events(df_events)
                st.success("Event deleted!")
                st.rerun()
else:
    st.info("No events found.")

# View RSVPs Admin Table
st.divider()
st.subheader("📋 Registered Students (Admin View)")
if not df_rsvps.empty:
    st.dataframe(df_rsvps, use_container_width=True)
else:
    st.write("No RSVPs recorded yet.")
