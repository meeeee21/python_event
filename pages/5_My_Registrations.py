# pages/5_My_Registrations.py

import streamlit as st
import qrcode
from io import BytesIO
import database as db
from datetime import datetime

if "role" not in st.session_state or st.session_state["role"] != "Student":
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("🎟️ My Registrations & Feedback")

user_id = st.session_state["user_id"]
registrations = db.get_user_registrations(user_id)

if not registrations:
    st.info("You haven't registered for any events yet.")
else:
    for reg in registrations:
        event_id, title, description, event_date_str = reg
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
        
        with st.expander(f"{title} - {event_date_str}"):
            st.write(description)
            
            # --- QR CODE GENERATION ---
            # Generates a QR code for event entry.
            qr_data = f"UserID:{user_id},EventID:{event_id},Event:{title}"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            
            st.image(buf, caption="Your QR Code Ticket", width=200)
            
            # --- FEEDBACK SYSTEM ---
            # Allows students to give feedback on past events.
            if event_date < datetime.now().date():
                st.subheader("Submit Feedback")
                with st.form(key=f"feedback_form_{event_id}"):
                    rating = st.slider("Your Rating (1-5)", 1, 5, 3)
                    comment = st.text_area("Your comments")
                    
                    feedback_submitted = st.form_submit_button("Submit Feedback")
                    if feedback_submitted:
                        db.add_feedback(user_id, event_id, rating, comment)
                        st.success("Thank you for your feedback!")
            else:
                st.info("Feedback can be submitted after the event has passed.")