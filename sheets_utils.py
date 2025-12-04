from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import streamlit as st

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1NFfol3Incp-80m4JYojoJ--yzQYY2IgWvWz5GiUcQGY/edit?gid=897113735#gid=897113735"

def get_connection():
    """Get Google Sheets connection."""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return None

def load_reservations():
    """Load reservations from Google Sheets."""
    try:
        conn = get_connection()
        if not conn:
            return []
        
        # Read from "Reservas" worksheet
        df = conn.read(worksheet="Reservas", usecols=[0, 1, 2])
        
        if df.empty:
            return []
        
        # Convert to format expected by app
        reservations = []
        for _, row in df.iterrows():
            if pd.notna(row.get('usuario')) and pd.notna(row.get('fecha')):
                reservations.append({
                    'user': str(row['usuario']),
                    'date': str(row['fecha']),
                    'created_at': str(row.get('creado', ''))
                })
        return reservations
    except Exception as e:
        print(f"Error loading from Sheets: {e}")
        return []

def save_reservations(reservations):
    """Save reservations to Google Sheets."""
    try:
        conn = get_connection()
        if not conn:
            return False
        
        # Convert to DataFrame
        data = []
        for res in reservations:
            data.append({
                'usuario': res['user'],
                'fecha': res['date'],
                'creado': res.get('created_at', '')
            })
        
        df = pd.DataFrame(data)
        
        # Write to sheet
        conn.update(worksheet="Reservas", data=df)
        return True
    except Exception as e:
        print(f"Error saving to Sheets: {e}")
        return False

def load_history():
    """Load history from Google Sheets."""
    try:
        conn = get_connection()
        if not conn:
            return []
        
        # Read from "Historial" worksheet
        df = conn.read(worksheet="Historial", usecols=[0, 1, 2, 3, 4])
        
        if df.empty:
            return []
        
        # Convert to format expected by app
        history = []
        for _, row in df.iterrows():
            if pd.notna(row.get('timestamp')):
                history.append({
                    'timestamp': str(row['timestamp']),
                    'action': str(row.get('accion', '')),
                    'user': str(row.get('usuario', '')),
                    'date': str(row.get('fecha', '')),
                    'details': str(row.get('detalles', ''))
                })
        return history
    except Exception as e:
        print(f"Error loading history from Sheets: {e}")
        return []

def save_history(history):
    """Save history to Google Sheets."""
    try:
        conn = get_connection()
        if not conn:
            return False
        
        # Convert to DataFrame
        data = []
        for entry in history:
            data.append({
                'timestamp': entry.get('timestamp', ''),
                'accion': entry.get('action', ''),
                'usuario': entry.get('user', ''),
                'fecha': entry.get('date', ''),
                'detalles': entry.get('details', '')
            })
        
        df = pd.DataFrame(data)
        
        # Write to sheet
        conn.update(worksheet="Historial", data=df)
        return True
    except Exception as e:
        print(f"Error saving history to Sheets: {e}")
        return False

def add_history_entry(action, user_name, reservation_date, details=""):
    """Add an entry to the history log."""
    history = load_history()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "user": user_name,
        "date": reservation_date,
        "details": details
    }
    history.append(entry)
    save_history(history)
