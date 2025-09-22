# pages/3_Manage_Events.py

import streamlit as st
import pandas as pd
import database as db

if "role" not in st.session_state or st.session_state["role"] != "Organizer":
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("📋 Manage Your Events")

organizer_id = st.session_state["user_id"]
events = db.get_organizer_events(organizer_id)

if not events:
    st.info("You have not created any events yet.")
else:
    event_titles = [event[1] for event in events]
    selected_event_title = st.selectbox("Select an event to manage", event_titles)
    
    selected_event_id = None
    for event in events:
        if event[1] == selected_event_title:
            selected_event_id = event[0]
            break

    if selected_event_id:
        st.subheader(f"Managing: {selected_event_title}")
        
        tab1, tab2 = st.tabs(["Registered Students", "Feedback & Ratings"])

        with tab1:
            st.write("List of students registered for this event.")
            registered_users = db.get_registered_users(selected_event_id)
            if registered_users:
                df_users = pd.DataFrame(registered_users, columns=["Username"])
                st.dataframe(df_users, use_container_width=True)
            else:
                st.info("No students have registered for this event yet.")
        
        with tab2:
            st.write("Feedback received for this event.")
            feedback = db.get_event_feedback(selected_event_id)
            if feedback:
                df_feedback = pd.DataFrame(feedback, columns=["Rating (out of 5)", "Comment"])
                st.dataframe(df_feedback, use_container_width=True)
            else:
                st.info("No feedback has been submitted for this event yet.")