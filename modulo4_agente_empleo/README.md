# 🧭 Roadmap del Módulo 4: Agente IA para búsqueda laboral

> ✅ Meta: Crear un sistema donde el usuario pueda cargar su perfil, conectarse a LinkedIn, buscar empleos, postularse de forma automática y hacer seguimiento, todo desde una interfaz web.

---

## 🛠️ Fase 1: Base funcional (MVP mínimo)

🔧 _Objetivo: tener una app usable con login, carga de perfil y respuesta básica del agente._

| Paso | Tarea                                    | Mejora integrada                          |
| ---- | ---------------------------------------- | ----------------------------------------- |
| 1️⃣   | Crear login de usuario (JWT)             | 🔐 Login con Google (Auth0/Firebase)      |
| 2️⃣   | Formulario de preferencias de búsqueda   | ✅ Validación básica                      |
| 3️⃣   | Carga de CV PDF y extracción de texto    | 📄 Soporte para múltiples versiones de CV |
| 4️⃣   | Agente responde consulta básica          | 🎭 Mock con historial inicial             |
| 5️⃣   | Mostrar respuesta del agente en frontend | 💬 UI limpia con feedback visual          |

---

## 🔍 Fase 2: Matching real + redacción automática

🔧 _Objetivo: el agente busca trabajos reales y redacta correos personalizados._

| Paso | Tarea                                 | Mejora integrada                             |
| ---- | ------------------------------------- | -------------------------------------------- |
| 6️⃣   | Scraping/API de ofertas               | 🔔 Notificaciones si hay match               |
| 7️⃣   | Matching semántico CV ↔ job           | 🧠 Vector store y memoria personalizada      |
| 8️⃣   | Scoring de compatibilidad             | 📊 Mostrar métricas en el frontend           |
| 9️⃣   | Redacción automática de postulaciones | 📄 Personalización según estilo del usuario  |
| 🔟   | Interfaz para revisar y enviar mails  | 🧩 Posibilidad de edición manual del mensaje |

---

## 📩 Fase 3: Postulación + seguimiento

| Paso | Tarea                                 | Mejora integrada                             |
| ---- | ------------------------------------- | -------------------------------------------- |
| 1️⃣1️⃣ | Envío real de correos                 | 🛡️ Opción de envío programado o manual       |
| 1️⃣2️⃣ | Mensajes en LinkedIn (automatización) | 🔐 Cifrado seguro de credenciales            |
| 1️⃣3️⃣ | Registro de acciones                  | 🧾 Panel histórico con filtros y exportación |
| 1️⃣4️⃣ | Dashboard de seguimiento              | 📈 Métricas y alertas de oportunidades       |

---

## 🤖 Fase 4: Agente autónomo + configuración avanzada

| Paso | Tarea                               | Mejora integrada                           |
| ---- | ----------------------------------- | ------------------------------------------ |
| 1️⃣5️⃣ | Activar modo automático             | 🎛️ Configuración por horarios/días         |
| 1️⃣6️⃣ | Agente toma decisiones y actúa solo | 🤖 Lógica basada en umbrales y contexto    |
| 1️⃣7️⃣ | Panel de control y configuración    | 🌐 Panel editable con frecuencia y canales |

---

## 🔐 Mejoras transversales (disponibles desde cualquier fase)

| Mejora                         | Implementación recomendada                   |
| ------------------------------ | -------------------------------------------- |
| 🔐 Login con Google/Auth0      | Desde Fase 1 si hay tiempo                   |
| 📄 CVs múltiples por usuario   | Desde Fase 1 o 2                             |
| 🧾 Encriptado de credenciales  | Desde Fase 3, obligatorio si usamos LinkedIn |
| 🔔 Notificaciones por Telegram | Desde Fase 2, útil para alerta de match      |
| 📈 Métricas y logs             | Desde Fase 3 o 4                             |
