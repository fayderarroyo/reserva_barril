"""
Email notification module for Reserva Barril.
This is optional functionality - requires SMTP configuration.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration (OPTIONAL - configure these if you want email notifications)
SMTP_SERVER = "smtp.gmail.com"  # Change if using different provider
SMTP_PORT = 587

# Use Streamlit secrets in production, fallback to hardcoded for local
try:
    import streamlit as st
    SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
    SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]
except:
    # Fallback for local development
    SENDER_EMAIL = "rehabilitados2025@gmail.com"
    SENDER_PASSWORD = "Uribeparaco2025"

def send_reservation_email(user_name, user_email, reservation_date, action="created"):
    """
    Send email notification for reservation actions.
    
    Args:
        user_name: Name of the user
        user_email: Email of the user
        reservation_date: Date of reservation
        action: "created" or "cancelled"
    
    Returns:
        True if email sent successfully, False otherwise
    """
    
    # Skip if email not configured
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = user_email
        
        if action == "created":
            msg['Subject'] = f"🍖 Reserva Confirmada - Barril Los Rehabilitados"
            body = f"""
Hola {user_name},

¡Tu reserva ha sido confirmada! 🎉

📅 Fecha: {reservation_date}
⏰ Horario: 10:00 AM - 10:00 AM (día siguiente)

Recuerda:
✅ Recoger el barril en la fecha indicada
✅ Verificar todos los accesorios al recibirlo
✅ Devolverlo limpio y seco
✅ Informar al grupo si necesitas cancelar

¡Disfruta tu asado!

---
Los Rehabilitados
            """
        else:  # cancelled
            msg['Subject'] = f"❌ Reserva Cancelada - Barril Los Rehabilitados"
            body = f"""
Hola {user_name},

Tu reserva ha sido cancelada.

📅 Fecha cancelada: {reservation_date}

La fecha ahora está disponible para otros miembros del grupo.

---
Los Rehabilitados
            """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_group_notification(all_users_dict, reservation_date, user_name, action="created"):
    """
    Send notification to all group members about a reservation change.
    
    Args:
        all_users_dict: Dictionary of {name: email}
        reservation_date: Date of reservation
        user_name: Name of user who made/cancelled reservation
        action: "created" or "cancelled"
    """
    
    # Skip if email not configured
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['Bcc'] = ", ".join(all_users_dict.values())  # BCC to all members
        
        if action == "created":
            msg['Subject'] = f"📅 Nueva Reserva - {user_name}"
            body = f"""
Hola equipo,

{user_name} ha reservado el barril para:

📅 Fecha: {reservation_date}

Revisa el calendario para ver las fechas disponibles.

---
Los Rehabilitados
            """
        else:
            msg['Subject'] = f"🔓 Fecha Disponible - {reservation_date}"
            body = f"""
Hola equipo,

{user_name} ha cancelado su reserva.

📅 Fecha ahora disponible: {reservation_date}

¡Puedes reservar esta fecha si te interesa!

---
Los Rehabilitados
            """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"Error sending group notification: {e}")
        return False
