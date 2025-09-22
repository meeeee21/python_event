# main.py

import streamlit as st
import database as db  # Importing our custom module

st.set_page_config(page_title="Campus Event Manager", layout="centered")

def login():
    st.title("🎓 Campus Event Manager")
    st.write("Welcome! Please log in to continue.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = db.check_user(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user[0]
                st.session_state["username"] = user[1]
                st.session_state["role"] = user[2]
                st.rerun() 
            else:
                st.error("Invalid username or password.")

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Main app logic
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
else:
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    st.sidebar.write(f"Role: **{st.session_state['role']}**")
    if st.sidebar.button("Logout"):
        logout()
    st.header("Please select a page from the sidebar.")