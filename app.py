import streamlit as st
import pandas as pd

st.set_page_config(page_title="UniEvent System", layout="wide")

st.title("🎓 UniEvent System - University Event Finder")
st.write("Welcome to the University Event Finder App!")

# Sidebar for adding events
st.sidebar.header("Add New Event")
event_name = st.sidebar.text_input("Event Name")
category = st.sidebar.selectbox("Category", ["Academic", "Sports", "Cultural", "Tech"])
date = st.sidebar.date_input("Event Date")
venue = st.sidebar.text_input("Venue")

if st.sidebar.button("Add Event"):
    st.success(f"Event '{event_name}' added successfully!")

# Main area to view events
st.header("Upcoming Events")
st.info("No events registered yet. Use the sidebar to add events!")
