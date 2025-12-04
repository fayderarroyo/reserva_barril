import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1NFfol3Incp-80m4JYojoJ--yzQYY2IgWvWz5GiUcQGY/edit?gid=897113735#gid=897113735"
RESERVATIONS_SHEET = "Reservas"
HISTORY_SHEET = "Historial"

def get_google_sheet():
    """
    Connect to Google Sheets using public URL.
    """
    try:
        import streamlit as st
        # For Streamlit Cloud, we'll use st.connection
        # For now, using public sheet access
        gc = gspread.oauth()
        sheet = gc.open_by_url(SHEET_URL)
        return sheet
    except:
        # Fallback: try to open as public sheet
        gc = gspread.service_account()
        sheet = gc.open_by_url(SHEET_URL)
        return sheet

def load_reservations():
    """Load reservations from Google Sheets."""
    try:
        sheet = get_google_sheet()
        worksheet = sheet.worksheet(RESERVATIONS_SHEET)
        data = worksheet.get_all_records()
        
        # Convert to format expected by app
        reservations = []
        for row in data:
            if row.get('usuario') and row.get('fecha'):
                reservations.append({
                    'user': row['usuario'],
                    'date': row['fecha'],
                    'created_at': row.get('creado', '')
                })
        return reservations
    except Exception as e:
        print(f"Error loading from Sheets: {e}")
        return []

def save_reservations(reservations):
    """Save reservations to Google Sheets."""
    try:
        sheet = get_google_sheet()
        
        # Get or create worksheet
        try:
            worksheet = sheet.worksheet(RESERVATIONS_SHEET)
            worksheet.clear()
        except:
            worksheet = sheet.add_worksheet(title=RESERVATIONS_SHEET, rows=100, cols=10)
        
        # Prepare data
        headers = ['usuario', 'fecha', 'creado']
        data = [headers]
        
        for res in reservations:
            data.append([
                res['user'],
                res['date'],
                res.get('created_at', '')
            ])
        
        # Write to sheet
        worksheet.update('A1', data)
        return True
    except Exception as e:
        print(f"Error saving to Sheets: {e}")
        return False

def load_history():
    """Load history from Google Sheets."""
    try:
        sheet = get_google_sheet()
        worksheet = sheet.worksheet(HISTORY_SHEET)
        data = worksheet.get_all_records()
        
        # Convert to format expected by app
        history = []
        for row in data:
            if row.get('timestamp'):
                history.append({
                    'timestamp': row['timestamp'],
                    'action': row.get('accion', ''),
                    'user': row.get('usuario', ''),
                    'date': row.get('fecha', ''),
                    'details': row.get('detalles', '')
                })
        return history
    except Exception as e:
        print(f"Error loading history from Sheets: {e}")
        return []

def save_history(history):
    """Save history to Google Sheets."""
    try:
        sheet = get_google_sheet()
        
        # Get or create worksheet
        try:
            worksheet = sheet.worksheet(HISTORY_SHEET)
            worksheet.clear()
        except:
            worksheet = sheet.add_worksheet(title=HISTORY_SHEET, rows=1000, cols=10)
        
        # Prepare data
        headers = ['timestamp', 'accion', 'usuario', 'fecha', 'detalles']
        data = [headers]
        
        for entry in history:
            data.append([
                entry.get('timestamp', ''),
                entry.get('action', ''),
                entry.get('user', ''),
                entry.get('date', ''),
                entry.get('details', '')
            ])
        
        # Write to sheet
        worksheet.update('A1', data)
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
