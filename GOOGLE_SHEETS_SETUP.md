# Configuración de Google Sheets en Streamlit Cloud

## Paso 1: Actualizar Secrets en Streamlit Cloud

1. Ve a tu app en Streamlit Cloud
2. Click en "⚙️ Settings"
3. Click en "Secrets"
4. **REEMPLAZA** todo el contenido con esto:

```toml
# Email configuration
SENDER_EMAIL = "rehabilitados2025@gmail.com"
SENDER_PASSWORD = "tu_contraseña_de_16_caracteres_aqui"

# Google Sheets configuration
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/1NFfol3Incp-80m4JYojoJ--yzQYY2IgWvWz5GiUcQGY/edit"
type = "public"
```

5. Click "Save"

## Paso 2: Preparar tu Google Sheet

Tu Google Sheet necesita tener estas pestañas con estos encabezados:

### Pestaña "Reservas"
| usuario | fecha | creado |
|---------|-------|--------|
|         |       |        |

### Pestaña "Historial"
| timestamp | accion | usuario | fecha | detalles |
|-----------|--------|---------|-------|----------|
|           |        |         |       |          |

## Paso 3: Verificar

1. La app se redeployará automáticamente
2. Espera 2-3 minutos
3. Haz una reserva de prueba
4. Verifica que aparezca en tu Google Sheet

## Solución de Problemas

Si no funciona:
- Verifica que el Sheet sea público (Editor para cualquiera con el link)
- Verifica que las pestañas se llamen exactamente "Reservas" e "Historial"
- Mira los logs en Streamlit Cloud para ver errores

## Fallback

Si Google Sheets no funciona, la app automáticamente usará JSON como antes (pero se perderán datos al redeploy).
