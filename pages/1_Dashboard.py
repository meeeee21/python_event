# pages/1_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import database as db

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in to view this page.")
    st.stop()

st.title("📊 Dashboard")

role = st.session_state.get("role")
user_id = st.session_state.get("user_id")

if role == "Organizer":
    st.header("Your Events Overview")
    events = db.get_organizer_events(user_id)
    if not events:
        st.info("You haven't created any events yet. Go to 'Create Event' to get started.")
    else:
        event_data = []
        for event in events:
            registrations = db.get_registered_users(event[0])
            feedback = db.get_event_feedback(event[0])
            avg_rating = sum([f[0] for f in feedback]) / len(feedback) if feedback else 0
            event_data.append({
                "Title": event[1],
                "Date": event[3],
                "Registrations": len(registrations),
                "Average Rating": f"{avg_rating:.2f}"
            })
        
        df = pd.DataFrame(event_data)
        st.dataframe(df, use_container_width=True)

        # Analytics chart
        st.header("Analytics")
        fig = px.bar(df, x="Title", y="Registrations", title="Registrations per Event", color="Title")
        st.plotly_chart(fig, use_container_width=True)

elif role == "Student":
    st.header("Your Upcoming Registered Events")
    registrations = db.get_user_registrations(user_id)
    
    if not registrations:
        st.info("You are not registered for any events. Go to 'Browse Events' to find some!")
    else:
        for reg in registrations:
            with st.container(border=True):
                st.subheader(reg[1])
                st.write(f"**Date:** {reg[3]}")
                st.write(reg[2])