import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
import utils
import os
import email_notifications

# Version: 2.0 - Google Sheets + Email Checkboxes
# Password for operations
OPERATION_PASSWORD = "pellejo"

# Page Config
st.set_page_config(page_title="Reserva Barril Los Rehabilitados", page_icon="🍖", layout="wide")

# Custom CSS for background and styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url('assets/background.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 8px 16px;
    }
    h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

# Title with collage
col_title1, col_title2 = st.columns([2, 1])
with col_title1:
    st.title("🍖 Reserva Barril 'Los Rehabilitados'")
    st.markdown("### Sistema de Gestión de Reservas")
with col_title2:
    # 8-image collage in 2 rows of 4
    if all(os.path.exists(f'assets/collage_{i}.png') for i in range(1, 9)):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image('assets/collage_1.png', use_column_width=True)
            st.image('assets/collage_5.png', use_column_width=True)
        with col2:
            st.image('assets/collage_2.png', use_column_width=True)
            st.image('assets/collage_6.png', use_column_width=True)
        with col3:
            st.image('assets/collage_3.png', use_column_width=True)
            st.image('assets/collage_7.png', use_column_width=True)
        with col4:
            st.image('assets/collage_4.png', use_column_width=True)
            st.image('assets/collage_8.png', use_column_width=True)

# Users List with emails
# Users List with emails
USERS = {
    "Daniel Sierra": "dmsierra10@gmail.com",
    "Shirly Madiedo": "shirlymadiedo@gmail.com",
    "Fayder Arroyo": "fayderarroyo@gmail.com",
    "Rina Marmolejo": "rinamarmolejo9@gmail.com",
    "Maria Monica Rodriguez": "mamoca17@msn.com",
    "Lina Pertuz": "lpertuz17@gmail.com",
    "Kevin": "kevin9624@outlook.com"
}

# Default password for everyone (can be changed later)
DEFAULT_PASSWORD = "1234"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

def login():
    st.markdown("## 🔐 Iniciar Sesión")
    
    # Login form
    with st.form("login_form"):
        username = st.selectbox("Selecciona tu usuario", list(USERS.keys()))
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            # Check password (using secrets if available, else default)
            # In a real app, we would store hashed passwords
            # For now, we check against a simple rule or secrets
            
            valid_password = False
            
            # Check if user has specific password in secrets
            if "passwords" in st.secrets and username in st.secrets["passwords"]:
                if password == st.secrets["passwords"][username]:
                    valid_password = True
            # Fallback to default password
            elif password == DEFAULT_PASSWORD:
                valid_password = True
                
            if valid_password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("✅ Login exitoso!")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.rerun()

# Main App Logic
if not st.session_state['logged_in']:
    login()
    st.stop()  # Stop execution here if not logged in

# --- APP CONTENT (Only visible if logged in) ---

# Sidebar with user info
with st.sidebar:
    st.write(f"👤 **Usuario:** {st.session_state['username']}")
    if st.button("cerrar sesión"):
        logout()

USER_NAMES = list(USERS.keys())

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📅 Reservar & Mis Reservas", "📆 Calendario", "📜 Reglamento", "📋 Historial"])

# --- TAB 1: RESERVAR & MIS RESERVAS (SIDE BY SIDE) ---
with tab1:
    # Split into two columns
    col_left, col_right = st.columns(2)
    
    # LEFT COLUMN: RESERVAR
    with col_left:
        st.header("Hacer una Reserva")
        
        col1, col2 = st.columns(2)
        with col1:
            # Auto-select logged in user
            st.info(f"👤 Reservando como: **{st.session_state['username']}**")
            selected_user = st.session_state['username']
        with col2:
            # Min date is today
            selected_date = st.date_input("Selecciona la fecha", min_value=date.today())
        
        # Email notification option
        send_email = st.checkbox("📧 Enviar notificación por email", value=True, key="send_email_reserve")

        if st.button("Confirmar Reserva", type="primary", use_container_width=True):
            # No password needed, user is logged in
            success, message = utils.add_reservation(selected_user, selected_date)
            if success:
                st.success(f"✅ {message}")
                st.balloons()
                # Try to send email notification (optional)
                if send_email:
                    try:
                        email_notifications.send_reservation_email(
                            selected_user, 
                            USERS[selected_user], 
                            selected_date.isoformat(), 
                            "created"
                        )
                        email_notifications.send_group_notification(
                            USERS, 
                            selected_date.isoformat(), 
                            selected_user, 
                            "created"
                        )
                        st.info("📧 Email enviado al grupo")
                    except Exception as e:
                        st.warning(f"⚠️ No se pudo enviar email: {e}")
            else:
                st.error(f"❌ {message}")
    
    # RIGHT COLUMN: MIS RESERVAS
    with col_right:
        st.header("Mis Reservas Activas")
        
        # Show only logged in user's reservations by default
        current_user = st.session_state['username']
        
        # Email notification option for cancellations
        send_cancel_email = st.checkbox("📧 Enviar email al cancelar", value=True, key="send_email_cancel")
        
        all_reservations = utils.get_all_reservations()
        # Filter for current user
        user_reservations = [r for r in all_reservations if r['user'] == current_user]
        
        # Sort by date
        user_reservations.sort(key=lambda x: x['date'])

        if not user_reservations:
            st.info("No tienes reservas registradas.")
        else:
            for res in user_reservations:
                with st.container():
                    col_res1, col_res2 = st.columns([3, 1])
                    with col_res1:
                        st.write(f"📅 **Fecha:** {res['date']}")
                    with col_res2:
                        # Unique key for button using date and user
                        if st.button("Cancelar", key=f"cancel_{res['date']}_{res['user']}"):
                            # No password needed
                            success, msg = utils.cancel_reservation(res['user'], res['date'])
                            if success:
                                st.success(msg)
                                # Try to send cancellation email (optional)
                                if send_cancel_email:
                                    try:
                                        email_notifications.send_reservation_email(
                                            res['user'], 
                                            USERS[res['user']], 
                                            res['date'], 
                                            "cancelled"
                                        )
                                        email_notifications.send_group_notification(
                                            USERS, 
                                            res['date'], 
                                            res['user'], 
                                            "cancelled"
                                        )
                                        st.info("📧 Email de cancelación enviado")
                                    except Exception as e:
                                        st.warning(f"⚠️ No se pudo enviar email: {e}")
                                st.rerun()
                            else:
                                st.error(msg)

# --- TAB 2: CALENDARIO ---
with tab2:
    st.header("Disponibilidad")
    
    reservations = utils.get_all_reservations()
    if reservations:
        df = pd.DataFrame(reservations)
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df[['date', 'user']]
        df.columns = ['Fecha', 'Reservado por']
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Calendar visual (simple list for now, or use a calendar component if installed)
        # For simplicity in standard streamlit, a dataframe or table is best.
    else:
        st.info("No hay reservas futuras.")

# --- TAB 3: REGLAMENTO ---
with tab3:
    st.header("🔥 Reglamento de uso del Barril “Los Rehabilitados”")
    st.markdown("""
    **1. Reservas**
    *   Las reservas se hacen únicamente a través de esta aplicación.
    *   Una reserva equivale a 24 horas (10:00 am – 10:00 am dia siguiente).
    *   **Solo se permite una reserva activa por persona a la vez.**

    **2. Modificaciones y cancelaciones**
    *   Solo el responsable que hizo la reserva puede modificar o cancelar su turno.
    *   Al cancelar, el evento se eliminará automáticamente.
    *   *Se sugiere que las cancelaciones de último momento se informen por WhatsApp.*

    **3. Entrega y condiciones de uso**
    *   El Barril debe entregarse **limpio, seco y sin residuos**.
    *   El barril debe recogerlo la persona que hizo la reserva.
    *   **Inventario:** 1 kit de 5 pinchos, 1 accesorio para pollo, 1 choricera pequeña, 1 multiusos de 3 puestos, 1 barril de 28 lb con todos sus elementos.
    *   En caso de daño o pérdida, el responsable asume el costo.

    **4. Garantía y mantenimiento**
    *   No usar gasolina ni químicos inflamables.
    *   Solo debe usarse en lugares ventilados o exteriores.

    **5. Respeto por el grupo**
    *   Todos los miembros deben respetar el orden de las reservas.
    *   **Prohibido el préstamo a terceras personas.**
    """)

# --- TAB 4: HISTORIAL ---
with tab4:
    st.header("📋 Historial de Cambios")
    
    history = utils.get_history()
    
    if not history:
        st.info("No hay cambios registrados aún.")
    else:
        st.write(f"**Total de cambios:** {len(history)}")
        
        for entry in history:
            # Parse timestamp
            try:
                timestamp = datetime.fromisoformat(entry['timestamp'])
                time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            except:
                time_str = entry['timestamp']
            
            # Create colored container based on action
            if entry['action'] == 'created':
                icon = "✅"
                action_text = "Reservó"
                color = "#28a745"  # Green
            else:
                icon = "❌"
                action_text = "Canceló"
                color = "#dc3545"  # Red
            
            # Display entry
            st.markdown(f"""
            <div style="
                padding: 10px; 
                margin: 5px 0; 
                border-left: 4px solid {color}; 
                background-color: rgba(255,255,255,0.05);
                border-radius: 4px;
            ">
                <strong>{icon} {entry['user']}</strong> {action_text} el <strong>{entry['date']}</strong><br>
                <small style="color: #888;">🕐 {time_str}</small>
            </div>
            """, unsafe_allow_html=True)

