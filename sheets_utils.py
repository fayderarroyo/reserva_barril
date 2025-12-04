import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from datetime import datetime
import streamlit as st

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1NFfol3Incp-80m4JYojoJ--yzQYY2IgWvWz5GiUcQGY/edit?usp=sharing"
SHEET_KEY = "1NFfol3Incp-80m4JYojoJ--yzQYY2IgWvWz5GiUcQGY"

def get_connection():
    """Get Google Sheets connection using public access."""
    try:
        # Use anonymous access for public sheets
        gc = gspread.auth.Client(auth=None)
        gc.http_client.auth = None
        sheet = gc.open_by_key(SHEET_KEY)
        return sheet
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return None

def load_reservations():
    """Load reservations from Google Sheets."""
    try:
        sheet = get_connection()
        if not sheet:
            return []
        
        # Get "Reservas" worksheet
        worksheet = sheet.worksheet("Reservas")
        data = worksheet.get_all_records()
        
        # Convert to format expected by app
        reservations = []
        for row in data:
            if row.get('usuario') and row.get('fecha'):
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
        sheet = get_connection()
        if not sheet:
            return False
        
        # Get or create worksheet
        try:
            worksheet = sheet.worksheet("Reservas")
        except:
            worksheet = sheet.add_worksheet(title="Reservas", rows=100, cols=10)
        
        # Clear existing data
        worksheet.clear()
        
        # Prepare DataFrame
        data = []
        for res in reservations:
            data.append({
                'usuario': res['user'],
                'fecha': res['date'],
                'creado': res.get('created_at', '')
            })
        
        df = pd.DataFrame(data)
        
        # Write to sheet
        set_with_dataframe(worksheet, df, include_index=False, include_column_header=True)
        return True
    except Exception as e:
        print(f"Error saving to Sheets: {e}")
        return False

def load_history():
    """Load history from Google Sheets."""
    try:
        sheet = get_connection()
        if not sheet:
            return []
        
        # Get "Historial" worksheet
        worksheet = sheet.worksheet("Historial")
        data = worksheet.get_all_records()
        
        # Convert to format expected by app
        history = []
        for row in data:
            if row.get('timestamp'):
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
        sheet = get_connection()
        if not sheet:
            return False
        
        # Get or create worksheet
        try:
            worksheet = sheet.worksheet("Historial")
        except:
            worksheet = sheet.add_worksheet(title="Historial", rows=1000, cols=10)
        
        # Clear existing data
        worksheet.clear()
        
        # Prepare DataFrame
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
        set_with_dataframe(worksheet, df, include_index=False, include_column_header=True)
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
