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

# Custom CSS for styling
st.markdown("""
<style>
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
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117;
        color: #888;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# Title with Icons
st.markdown("<h1 style='text-align: center;'>🔥 🥩 🍖 🥓 🔥</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Reserva Barril 'Los Rehabilitados'</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Sistema de Gestión de Reservas</h3>", unsafe_allow_html=True)
st.divider()

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

# --- UNIFIED DASHBOARD LAYOUT ---

# Create two main columns
main_col1, main_col2 = st.columns([1, 1])

# --- LEFT COLUMN: ACTIONS (RESERVE & MY RESERVATIONS) ---
with main_col1:
    # SECTION 1: MAKE RESERVATION
    st.markdown("### 📝 Hacer una Reserva")
    with st.container(border=True):
        # Auto-select logged in user
        st.info(f"👤 Reservando como: **{st.session_state['username']}**")
        selected_user = st.session_state['username']
        
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

    st.markdown("---")

    # SECTION 2: MY ACTIVE RESERVATIONS
    st.markdown("### 🎫 Mis Reservas Activas")
    with st.container(border=True):
        # Show only logged in user's reservations
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
                col_res1, col_res2 = st.columns([3, 1])
                with col_res1:
                    st.write(f"📅 **{res['date']}**")
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
                st.divider()

# --- RIGHT COLUMN: CALENDAR & STATUS ---
with main_col2:
    st.header("📆 Calendario de Reservas")
    
    reservations = utils.get_all_reservations()
    
    # Custom Calendar Visualization
    # Create a dataframe for the calendar
    if reservations:
        df = pd.DataFrame(reservations)
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df.sort_values('date')
        
        # Highlight today
        today = date.today()
        
        # Display as a styled table
        st.markdown("### Próximas Reservas")
        
        # Filter for future reservations only
        future_reservations = df[df['date'] >= today]
        
        if not future_reservations.empty:
            st.dataframe(
                future_reservations[['date', 'user']].rename(columns={'date': 'Fecha', 'user': 'Reservado por'}),
                use_container_width=True,
                hide_index=True,
                height=400
            )
        else:
            st.info("No hay reservas futuras.")
    else:
        st.info("No hay reservas registradas.")

    # Rules Expander
    with st.expander("📜 Ver Reglamento"):
        st.markdown("""
        ### Reglamento de Uso
        1. **Duración:** Las reservas son por 24 horas (10:00 AM a 10:00 AM del día siguiente).
        2. **Límite:** Solo puedes tener **una reserva activa** a la vez.
        3. **Responsable:** Quien reserva es responsable del barril y sus accesorios.
        4. **Limpieza:** El barril debe entregarse limpio y seco.
        5. **Inventario:** Verificar el inventario al recibir y entregar.
        6. **Uso:** Prohibido prestar el barril a terceros fuera del grupo.
        """)

# --- HISTORIAL (EXPANDER AT BOTTOM) ---
with st.expander("📋 Ver Historial de Cambios"):
    history = utils.get_history()
    if history:
        for entry in history:
            icon = "🟢" if entry['action'] == "created" else "🔴"
            action_text = "Reserva creada" if entry['action'] == "created" else "Reserva cancelada"
            st.markdown(f"{icon} **{entry['date']}** - {action_text} por **{entry['user']}** ({entry['timestamp']})")
    else:
        st.info("No hay historial disponible.")
        

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 Fayder Arroyo — Data & BI · Innovación Tecnológica</p>
    <p>Desarrollado con pasión por la analítica y la tecnología.</p>
</div>
""", unsafe_allow_html=True)

