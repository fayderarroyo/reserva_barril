# Deployment Guide - Streamlit Cloud

## Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)

## Step 1: Push to GitHub

### 1.1 Initialize Git Repository (if not done)
```bash
cd "C:\Users\Fayder Arroyo Herazo\Desktop\documentos Personales Fah\reserva-barril"
git init
git add .
git commit -m "Initial commit - Reserva Barril app"
```

### 1.2 Create GitHub Repository
1. Go to https://github.com/new
2. Name: `reserva-barril`
3. Description: "Sistema de gestión de reservas para barril compartido"
4. Make it **Private** (recommended for group use)
5. Click "Create repository"

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/reserva-barril.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign Up
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Authorize Streamlit

### 2.2 Deploy App
1. Click "New app"
2. Select your repository: `reserva-barril`
3. Branch: `main`
4. Main file path: `app.py`
5. Click "Advanced settings"

### 2.3 Add Secrets (Email Configuration)
In the "Secrets" section, add:

```toml
# Email configuration
SENDER_EMAIL = "rehabilitados2025@gmail.com"
SENDER_PASSWORD = "Uribeparaco2025"
```

> [!IMPORTANT]
> These secrets are encrypted and not visible in your code or GitHub

### 2.4 Deploy
1. Click "Deploy!"
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## Step 3: Update Email Configuration

You need to modify `email_notifications.py` to use Streamlit secrets:

```python
import streamlit as st

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Use Streamlit secrets in production, fallback to hardcoded for local
try:
    SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
    SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]
except:
    # Fallback for local development
    SENDER_EMAIL = "rehabilitados2025@gmail.com"
    SENDER_PASSWORD = "Uribeparaco2025"
```

## Step 4: Share with Your Group

Once deployed, share the URL with your group:
- URL: `https://your-app-name.streamlit.app`
- Password for operations: `pellejo`

## Updating the App

Whenever you make changes:
```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will automatically redeploy within 1-2 minutes!

## Troubleshooting

### App Won't Start
- Check the logs in Streamlit Cloud dashboard
- Verify all files are committed to GitHub
- Check that `requirements.txt` is correct

### Email Not Working
- Verify secrets are set correctly
- Check Gmail app password is valid
- Test locally first

### Data Not Persisting
- `reservations.json` and `history.json` are in Git
- Changes will persist across deployments
- For production, consider upgrading to a database

## Custom Domain (Optional)

Streamlit Cloud allows custom domains on paid plans. For free tier, use the provided `.streamlit.app` URL.

## Security Notes

- ✅ App is password-protected for operations
- ✅ Email credentials are encrypted in Streamlit secrets
- ✅ Repository can be private
- ⚠️ Shared password ("pellejo") - consider individual accounts later
