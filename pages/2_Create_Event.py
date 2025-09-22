# pages/2_Create_Event.py

import streamlit as st
import database as db

if "role" not in st.session_state or st.session_state["role"] != "Organizer":
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("🎉 Create a New Event")

with st.form("create_event_form", clear_on_submit=True):
    title = st.text_input("Event Title", placeholder="e.g., Annual Tech Fest")
    description = st.text_area("Event Description", placeholder="Describe the event, schedule, speakers, etc.")
    event_date = st.date_input("Event Date")
    
    submitted = st.form_submit_button("Create Event")
    
    if submitted:
        if not title or not description:
            st.error("Please fill out all fields.")
        else:
            organizer_id = st.session_state["user_id"]
            db.add_event(title, description, event_date.strftime("%Y-%m-%d"), organizer_id)
            st.success(f"Event '{title}' created successfully!")