import json
import os
from datetime import datetime, date

# Try to use Google Sheets, fallback to JSON
USE_SHEETS = False
try:
    import sheets_utils
    USE_SHEETS = True
    print("✅ Using Google Sheets for storage")
except Exception as e:
    print(f"⚠️ Google Sheets not available, using JSON: {e}")
    USE_SHEETS = False

# JSON file paths (fallback)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'reservations.json')
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.json')

def load_reservations():
    if USE_SHEETS:
        return sheets_utils.load_reservations()
    
    # Fallback to JSON
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_reservations(reservations):
    if USE_SHEETS:
        return sheets_utils.save_reservations(reservations)
    
    # Fallback to JSON
    with open(DATA_FILE, 'w') as f:
        json.dump(reservations, f, indent=4)

def load_history():
    if USE_SHEETS:
        return sheets_utils.load_history()
    
    # Fallback to JSON
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_history(history):
    if USE_SHEETS:
        return sheets_utils.save_history(history)
    
    # Fallback to JSON
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def add_history_entry(action, user_name, reservation_date, details=""):
    """
    Add an entry to the history log.
    
    Args:
        action: "created" or "cancelled"
        user_name: Name of the user
        reservation_date: Date of reservation
        details: Additional details (optional)
    """
    if USE_SHEETS:
        return sheets_utils.add_history_entry(action, user_name, reservation_date, details)
    
    # Fallback to JSON
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

def add_reservation(user_name, reservation_date):
    """
    Adds a reservation if valid.
    Returns (True, message) if successful.
    Returns (False, message) if failed.
    """
    reservations = load_reservations()
    reservation_date_str = reservation_date.isoformat()

    # 1. Check if date is already taken
    for res in reservations:
        if res['date'] == reservation_date_str:
            return False, f"La fecha {reservation_date_str} ya está reservada por {res['user']}."

    # 2. Check if user already has an active reservation
    # "Active" means a reservation in the future (including today)
    today_str = date.today().isoformat()
    for res in reservations:
        if res['user'] == user_name and res['date'] >= today_str:
            return False, f"El usuario {user_name} ya tiene una reserva activa ({res['date']}). Solo se permite una a la vez."

    # Add reservation
    new_res = {
        "user": user_name,
        "date": reservation_date_str,
        "created_at": datetime.now().isoformat()
    }
    reservations.append(new_res)
    save_reservations(reservations)
    
    # Log to history
    add_history_entry("created", user_name, reservation_date_str)
    
    return True, "Reserva exitosa."

def cancel_reservation(user_name, reservation_date_str):
    """
    Cancels a reservation for a specific user and date.
    """
    reservations = load_reservations()
    new_list = [r for r in reservations if not (r['user'] == user_name and r['date'] == reservation_date_str)]
    
    if len(new_list) < len(reservations):
        save_reservations(new_list)
        # Log to history
        add_history_entry("cancelled", user_name, reservation_date_str)
        return True, "Reserva cancelada."
    return False, "No se encontró la reserva o no tienes permiso."

def get_all_reservations():
    return load_reservations()

def get_history():
    """
    Get all history entries, sorted by timestamp (newest first).
    """
    history = load_history()
    history.reverse()  # Show newest first
    return history
