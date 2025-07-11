# 🚀 Agente IA para Búsqueda Laboral

> Un sistema integral que ayuda a los usuarios a buscar empleo de manera más eficiente mediante inteligencia artificial, automatizando el proceso de búsqueda, postulación y seguimiento de ofertas laborales.

## 🎯 Características principales

- 🔐 Autenticación segura con JWT y soporte para inicio de sesión con Google
- 📝 Gestión de perfiles de usuario y preferencias de búsqueda
- 🤖 Asistente de IA para búsqueda y postulación a empleos
- 📊 Panel de control para seguimiento de postulaciones
- 🔔 Notificaciones de nuevas ofertas que coincidan con tu perfil

## 🚀 Comenzando

### Requisitos previos

- Python 3.8 o superior
- Node.js 16.x o superior
- npm o yarn
- Cuenta de Firebase para autenticación

### Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/agente-ia-busqueda-laboral.git
   cd agente-ia-busqueda-laboral
   ```

2. **Configura el backend**
   ```bash
   # Crea y activa un entorno virtual
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # o
   source venv/bin/activate  # Linux/Mac

   # Instala dependencias
   pip install -r requirements.txt
   ```

3. **Configura el frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Configura las variables de entorno**
   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   # Backend
   SECRET_KEY=tu_clave_secreta
   DATABASE_URL=sqlite:///./app.db
   
   # Firebase
   FIREBASE_API_KEY=tu_api_key_de_firebase
   FIREBASE_AUTH_DOMAIN=tu-proyecto.firebaseapp.com
   FIREBASE_PROJECT_ID=tu-proyecto
   FIREBASE_STORAGE_BUCKET=tu-proyecto.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=tu_sender_id
   FIREBASE_APP_ID=tu_app_id
   ```

## 🏃 Ejecutando la aplicación

1. **Inicia el backend**
   ```bash
   cd backend
   uvicorn main:app --reload --port 8001
   ```

2. **Inicia el frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Accede a la aplicación**
   Abre tu navegador en [http://localhost:5173](http://localhost:5173)

## 🏗️ Estructura del proyecto

```
agente-ia-busqueda-laboral/
├── backend/               # Backend en FastAPI
│   ├── auth/              # Lógica de autenticación
│   ├── models/            # Modelos de base de datos
│   ├── routes/            # Rutas de la API
│   ├── main.py            # Punto de entrada del backend
│   └── requirements.txt   # Dependencias de Python
│
├── frontend/              # Frontend en React + TypeScript
│   ├── public/            # Archivos estáticos
│   ├── src/               # Código fuente
│   │   ├── components/    # Componentes reutilizables
│   │   ├── pages/         # Páginas de la aplicación
│   │   ├── App.tsx        # Componente principal
│   │   └── ...
│   └── package.json       # Dependencias de Node.js
│
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

## 🔧 Tecnologías utilizadas

- **Backend**: Python, FastAPI, SQLAlchemy, JWT
- **Frontend**: React, TypeScript, Material-UI
- **Autenticación**: Firebase Authentication
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Despliegue**: Docker, Nginx

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee las [pautas de contribución](CONTRIBUTING.md) antes de enviar un pull request.

## 📞 Contacto

¿Tienes preguntas? No dudes en contactarnos en [tu@email.com](mailto:tu@email.com)
