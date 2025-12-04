# Website Integration Guide

## Option 1: Embed with iframe (Recommended)

Add this code to your CV website where you want the app to appear:

```html
<div class="reserva-barril-container">
    <h2>🍖 Reserva Barril Los Rehabilitados</h2>
    <iframe 
        src="https://your-app-name.streamlit.app/?embedded=true" 
        width="100%" 
        height="800px" 
        frameborder="0"
        style="border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    </iframe>
</div>

<style>
.reserva-barril-container {
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px;
}

.reserva-barril-container h2 {
    text-align: center;
    margin-bottom: 20px;
}

/* Responsive */
@media (max-width: 768px) {
    .reserva-barril-container iframe {
        height: 600px;
    }
}
</style>
```

## Option 2: Link Button

Add a prominent button to your website:

```html
<div class="project-card">
    <h3>🍖 Reserva Barril</h3>
    <p>Sistema de gestión de reservas para barril compartido del grupo "Los Rehabilitados"</p>
    <a href="https://your-app-name.streamlit.app" target="_blank" class="btn-primary">
        Abrir Aplicación
    </a>
</div>

<style>
.project-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 12px;
    color: white;
    margin: 20px 0;
    text-align: center;
}

.btn-primary {
    display: inline-block;
    padding: 12px 30px;
    background: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 6px;
    font-weight: bold;
    margin-top: 15px;
    transition: transform 0.2s;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
</style>
```

## Option 3: Projects Section

Add to your projects portfolio:

```html
<section id="projects">
    <div class="project-grid">
        <!-- Your other projects -->
        
        <div class="project-item">
            <div class="project-image">
                <img src="path/to/barril-screenshot.png" alt="Reserva Barril">
            </div>
            <div class="project-content">
                <h3>🍖 Reserva Barril Los Rehabilitados</h3>
                <p>Sistema web de gestión de reservas con:</p>
                <ul>
                    <li>✅ Calendario compartido</li>
                    <li>📧 Notificaciones por email</li>
                    <li>📋 Historial de cambios</li>
                    <li>🔒 Protección con contraseña</li>
                </ul>
                <div class="tech-stack">
                    <span class="tech-badge">Python</span>
                    <span class="tech-badge">Streamlit</span>
                    <span class="tech-badge">Email API</span>
                </div>
                <div class="project-links">
                    <a href="https://your-app-name.streamlit.app" target="_blank">
                        Ver Demo
                    </a>
                    <a href="https://github.com/YOUR_USERNAME/reserva-barril" target="_blank">
                        GitHub
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
```

## Integration with Your CV Website

Based on your existing CV website structure:

### 1. Add to Navigation (if applicable)
```html
<nav>
    <a href="#about">Sobre Mí</a>
    <a href="#experience">Experiencia</a>
    <a href="#projects">Proyectos</a>
    <a href="#reserva-barril">Reserva Barril</a> <!-- New -->
</nav>
```

### 2. Create Dedicated Section
```html
<section id="reserva-barril" class="full-width-section">
    <div class="container">
        <h2>🍖 Proyecto: Reserva Barril</h2>
        <p class="subtitle">Sistema de gestión colaborativa</p>
        
        <iframe 
            src="https://your-app-name.streamlit.app/?embedded=true" 
            width="100%" 
            height="900px" 
            frameborder="0">
        </iframe>
        
        <div class="project-details">
            <h3>Características</h3>
            <ul>
                <li>Gestión de reservas con validación de reglas</li>
                <li>Notificaciones automáticas por email</li>
                <li>Historial completo de cambios</li>
                <li>Interfaz responsive y moderna</li>
            </ul>
        </div>
    </div>
</section>
```

## Mobile Optimization

Make sure the iframe is responsive:

```css
.reserva-barril-container iframe {
    width: 100%;
    min-height: 800px;
    border: none;
    border-radius: 8px;
}

@media (max-width: 768px) {
    .reserva-barril-container iframe {
        min-height: 600px;
    }
}

@media (max-width: 480px) {
    .reserva-barril-container iframe {
        min-height: 500px;
    }
}
```

## Screenshot for Portfolio

Take a screenshot of the app and add it to your portfolio:

1. Open the deployed app
2. Take a screenshot (use browser dev tools for consistent size)
3. Save as `barril-screenshot.png`
4. Add to your website's images folder
5. Use in project cards/portfolio

## SEO Optimization

Add meta tags to the page:

```html
<meta name="description" content="Sistema de gestión de reservas para barril compartido - Proyecto de Fayder Arroyo">
<meta name="keywords" content="Python, Streamlit, Web App, Gestión de Reservas">
```

## Analytics (Optional)

Track visits to your embedded app:

```html
<script>
// Track when users interact with the iframe
document.querySelector('iframe').addEventListener('load', function() {
    // Your analytics code here
    console.log('Reserva Barril app loaded');
});
</script>
```
