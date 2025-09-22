# database.py

import sqlite3
import hashlib

def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def db_connect():
    """Creates a connection to the SQLite database."""
    return sqlite3.connect("events.db")

def create_tables():
    """Creates the necessary tables if they don't exist."""
    conn = db_connect()
    cursor = conn.cursor()
    
    # Users table (students, organizers)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )""")
    
    # Events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        event_date TEXT,
        organizer_id INTEGER,
        FOREIGN KEY(organizer_id) REFERENCES users(id)
    )""")
    
    # Registrations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        event_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(event_id) REFERENCES events(id)
    )""")
    
    # Feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        event_id INTEGER,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(event_id) REFERENCES events(id)
    )""")
    
    conn.commit()
    conn.close()

def add_user(username, password, role):
    """Adds a new user to the database."""
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hash_password(password), role))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User {username} already exists.")
    finally:
        conn.close()

def check_user(username, password):
    """Verifies user credentials and returns user info."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE username = ? AND password = ?", 
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def add_event(title, description, event_date, organizer_id):
    """Adds a new event to the database."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (title, description, event_date, organizer_id) VALUES (?, ?, ?, ?)", 
                   (title, description, event_date, organizer_id))
    conn.commit()
    conn.close()

def get_all_events():
    """Fetches all events from the database."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT e.id, e.title, e.description, e.event_date, u.username FROM events e JOIN users u ON e.organizer_id = u.id")
    events = cursor.fetchall()
    conn.close()
    return events

def get_organizer_events(organizer_id):
    """Fetches events created by a specific organizer."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, event_date FROM events WHERE organizer_id = ?", (organizer_id,))
    events = cursor.fetchall()
    conn.close()
    return events
    
def get_registered_users(event_id):
    """Fetches users registered for a specific event."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username FROM users u
        JOIN registrations r ON u.id = r.user_id
        WHERE r.event_id = ?
    """, (event_id,))
    users = cursor.fetchall()
    conn.close()
    return users
    
def get_user_registrations(user_id):
    """Fetches events a user is registered for."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.title, e.description, e.event_date FROM events e
        JOIN registrations r ON e.id = r.event_id
        WHERE r.user_id = ?
    """, (user_id,))
    registrations = cursor.fetchall()
    conn.close()
    return registrations

def is_user_registered(user_id, event_id):
    """Checks if a user is already registered for an event."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM registrations WHERE user_id = ? AND event_id = ?", (user_id, event_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None
    
def register_user_for_event(user_id, event_id):
    """Registers a user for an event."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registrations (user_id, event_id) VALUES (?, ?)", (user_id, event_id))
    conn.commit()
    conn.close()
    
def add_feedback(user_id, event_id, rating, comment):
    """Adds feedback for an event."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (user_id, event_id, rating, comment) VALUES (?, ?, ?, ?)", 
                   (user_id, event_id, rating, comment))
    conn.commit()
    conn.close()
    
def get_event_feedback(event_id):
    """Gets all feedback for a specific event."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT rating, comment FROM feedback WHERE event_id = ?", (event_id,))
    feedback = cursor.fetchall()
    conn.close()
    return feedback

# Setup initial database and add sample users
def setup_database():
    """Initializes the DB and adds sample users."""
    create_tables()
    # Add sample users if they don't exist
    add_user("organizer1", "pass123", "Organizer")
    add_user("student1", "pass123", "Student")

# Run setup when this module is imported for the first time
setup_database()