✂️ Duky Barber — Sistema de Reservas Online

Aplicación web fullstack desarrollada para automatizar la gestión de citas de una barbería. El cliente puede reservar su turno online 24/7, y el barbero gestiona todo desde un panel de administración.

🌐 Demo en vivo: dukybarber.es


🚀 Funcionalidades

Para el cliente


Reserva de citas online con selección de fecha y hora disponible
Validación de teléfono con formato español (+34)
Email de confirmación automático al reservar
Mapa de Google Maps con la ubicación de la barbería
Código QR para acceso rápido desde móvil
Diseño responsive (móvil, tablet, escritorio)


Para el barbero (Panel Admin)


Dashboard con estadísticas de reservas (total, pendientes, confirmadas, canceladas)
Confirmar o cancelar reservas con mensaje personalizado al cliente
Email automático al cliente al confirmar o cancelar
Configuración del negocio (nombre, horario, días de trabajo, duración de citas)
Generador de QR descargable e imprimible
Notificación badge en tiempo real de reservas pendientes



🛠️ Stack tecnológico

Frontend


React 18 + Vite
CSS Modules con variables CSS personalizadas
Fuentes: Bebas Neue + DM Sans
Iconos: Font Awesome
Mapa: Google Maps Embed API


Backend


Python + Flask
SQLite + Flask-SQLAlchemy
Flask-CORS para comunicación frontend/backend
Resend para emails transaccionales
Gunicorn como servidor WSGI


Deploy


Frontend: Vercel (deploy automático desde GitHub)
Backend: Render (plan gratuito)
Dominio: dukybarber.es (Nominalia)



📁 Estructura del proyecto

app.barber/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx        # Navegación con scroll activo
│   │   ├── Hero.jsx          # Sección principal con logo
│   │   ├── Servicios.jsx     # Catálogo con buscador y filtros
│   │   ├── ServiceCard.jsx   # Tarjeta de servicio
│   │   ├── Reserva.jsx       # Formulario de reserva con slots
│   │   └── Footer.jsx        # Footer con mapa y contacto
│   ├── data/
│   │   └── servicios.js      # Datos de servicios (fácil de editar)
│   └── hooks/
│       └── useServicios.js   # Lógica de filtrado
│
duky-backend/
├── models/
│   ├── reserva.py            # Modelo de reserva
│   └── configuracion.py      # Configuración del negocio
├── routes/
│   ├── reservas.py           # API REST de reservas y slots
│   ├── admin.py              # Panel de administración
│   └── email_service.py      # Emails con Resend
└── templates/admin/
    ├── login.html            # Login del admin
    ├── panel.html            # Dashboard de reservas
    ├── configuracion.html    # Configuración del negocio
    └── qr.html               # Generador de QR


⚙️ Instalación local

Frontend

bashcd app.barber
npm install
npm run dev

Backend

bashcd duky-backend
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus credenciales
python run.py

Variables de entorno (.env)

FLASK_ENV=development
SECRET_KEY=tu-clave-secreta
RESEND_API_KEY=tu-api-key-resend
ADMIN_EMAIL=email-del-barbero@gmail.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu-password
APP_URL=https://dukybarber.es


📬 Contacto

Desarrollado por Israel De Oca


LinkedIn: linkedin.com/in/tu-perfil
GitHub: github.com/Israelapp



Este proyecto fue desarrollado como solución real para una barbería en España, automatizando la gestión de citas y eliminando la necesidad de reservas por teléfono.