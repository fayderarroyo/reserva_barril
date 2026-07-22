# 🍖 Reserva Barril "Los Rehabilitados"

Sistema de gestión de reservas para el barril compartido del grupo.

## 🚀 Inicio Rápido

### Instalación

```bash
cd reserva-barril
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 👥 Usuarios Registrados

- Daniel Sierra
- Shirly Madiedo
- Fayder Arroyo
- Rina Marmolejo
- Maria Monica Rodriguez
- Lina Pertuz
- Kevin

## 📋 Funcionalidades

### ✅ Hacer Reservas
- Selecciona tu nombre
- Elige la fecha deseada
- Confirma la reserva
- Solo una reserva activa por persona

### 📅 Ver Calendario
- Consulta todas las reservas
- Verifica disponibilidad
- Planifica con anticipación

### ❌ Cancelar Reservas
- Solo puedes cancelar tus propias reservas
- La fecha queda disponible inmediatamente
- Se recomienda avisar al grupo por WhatsApp

### 📜 Reglamento
- Consulta las reglas completas
- Inventario de accesorios
- Condiciones de uso

## 🔔 Notificaciones (Opcional)

El sistema incluye soporte para notificaciones por email. Ver [EMAIL_CONFIG.md](EMAIL_CONFIG.md) para instrucciones de configuración.

## 📁 Estructura del Proyecto

```
reserva-barril/
├── app.py                      # Aplicación principal
├── utils.py                    # Lógica de reservas
├── email_notifications.py      # Sistema de emails (opcional)
├── reservations.json           # Base de datos
├── assets/                     # Imágenes
│   ├── background.png
│   └── hero.png
├── requirements.txt
├── EMAIL_CONFIG.md
└── README.md
```

## 🎨 Características

- ✨ Interfaz moderna con imágenes temáticas
- 🎯 Validación automática de reglas
- 💾 Almacenamiento persistente
- 📧 Notificaciones por email (opcional)
- 🌙 Tema oscuro elegante

## 🛠️ Tecnologías

- **Python 3.x**
- **Streamlit** - Framework web
- **Pandas** - Manejo de datos
- **JSON** - Almacenamiento

## 📞 Soporte

Para problemas o sugerencias, contacta a cualquier miembro del grupo.

---

**Los Rehabilitados** 🍖
