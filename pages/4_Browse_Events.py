# pages/4_Browse_Events.py

import streamlit as st
import database as db
from datetime import datetime

if "role" not in st.session_state or st.session_state["role"] != "Student":
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("🔍 Browse and Register for Events")

# --- RECURSIVE FUNCTION ---
# This function demonstrates recursion as required by the project guidelines.
# While a simple loop is more Pythonic for this task, this fulfills the requirement.
def recursive_search(events, search_term, index=0, results=None):
    """Recursively searches for events matching the search term."""
    if results is None:
        results = []
    if index >= len(events):
        return results
    
    event_title = events[index][1]
    if search_term.lower() in event_title.lower():
        results.append(events[index])
        
    return recursive_search(events, search_term, index + 1, results)

all_events = db.get_all_events()

# --- LAMBDA FUNCTION ---
# This demonstrates a lambda function for inline sorting as required.
all_events_sorted = sorted(all_events, key=lambda event: datetime.strptime(event[3], "%Y-%m-%d"))

# Search and Filter UI
col1, col2 = st.columns([3, 1])
with col1:
    search_term = st.text_input("Search for an event by title")
with col2:
    filter_option = st.selectbox("Sort by", ["Date (Upcoming First)", "Date (Oldest First)"])

# Apply sorting
if filter_option == "Date (Oldest First)":
    all_events_sorted.reverse()

# Apply recursive search if a search term is provided
if search_term:
    display_events = recursive_search(all_events_sorted, search_term)
    if not display_events:
        st.warning(f"No events found matching '{search_term}'.")
else:
    display_events = all_events_sorted

# Display Events
if not display_events:
    st.info("There are no events to display.")
else:
    for event in display_events:
        event_id, title, description, event_date, organizer = event
        with st.container(border=True):
            st.subheader(title)
            st.caption(f"Organized by: {organizer} | Date: {event_date}")
            st.write(description)
            
            user_id = st.session_state["user_id"]
            if db.is_user_registered(user_id, event_id):
                st.success("✅ You are registered for this event.")
            else:
                if st.button("Register Now", key=f"register_{event_id}"):
                    db.register_user_for_event(user_id, event_id)
                    st.success(f"Successfully registered for '{title}'!")
                    st.rerun()