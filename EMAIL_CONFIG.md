# Configuración de Notificaciones por Email

## Configuración Opcional

El sistema incluye notificaciones por email, pero están **desactivadas por defecto**. La aplicación funciona perfectamente sin ellas.

## Cómo Activar las Notificaciones

### 1. Configurar Gmail (Recomendado)

Si quieres usar Gmail para enviar notificaciones:

1. **Crear una contraseña de aplicación:**
   - Ve a tu cuenta de Google: https://myaccount.google.com/
   - Seguridad → Verificación en 2 pasos (actívala si no está activa)
   - Seguridad → Contraseñas de aplicaciones
   - Genera una contraseña para "Correo"

2. **Editar `email_notifications.py`:**
   ```python
   SENDER_EMAIL = "tu_email@gmail.com"
   SENDER_PASSWORD = "tu_contraseña_de_aplicacion"
   ```

### 2. Usar Otro Proveedor

Si usas otro servicio (Outlook, Yahoo, etc.):

```python
# Para Outlook
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587

# Para Yahoo
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
```

## Qué Hacen las Notificaciones

### Email Individual
Cuando alguien hace o cancela una reserva, recibe un email con:
- ✅ Confirmación de la fecha
- 📋 Recordatorios de las reglas
- ℹ️ Información de contacto

### Email Grupal
Todos los miembros reciben una notificación cuando:
- 📅 Se hace una nueva reserva
- 🔓 Se libera una fecha

## Notificaciones por WhatsApp

Para WhatsApp, recomiendo usar **Twilio WhatsApp API** o simplemente:
- Crear un grupo de WhatsApp
- Copiar el mensaje de la app y pegarlo manualmente
- O usar un bot de WhatsApp (requiere configuración avanzada)

### Opción Simple: Mensaje Manual
La app ya muestra mensajes claros que puedes copiar y pegar en WhatsApp.
