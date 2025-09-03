# Encuesta de Satisfacción – Clínica Río Blanco (Streamlit)

Aplicación en Streamlit que recoge respuestas de usuarios mediante un formulario actualizado, guarda los datos en un CSV y envía un resumen por correo Gmail (SMTP).

## Campos del formulario
- Identificación (Nombre / RUT)
- Correo electrónico
- Fecha de atención (automática)
- Expectativas
- Cumplimiento de expectativas (Sí / Parcialmente / No)
- Mejoras sugeridas
- Comentario adicional

## Archivos
- `app.py` → Lógica de Streamlit. Guarda en CSV y envía por correo.
- `requirements.txt` → Dependencias necesarias.
- `.env` → Configuración de credenciales para uso local.
- `logo_crb.png` → Logo institucional.
- `respuestas_encuesta.csv` → Se crea automáticamente con las respuestas.

---
## Uso local (Windows / PowerShell)

```powershell
cd "C:\ruta\encuesta_satisfaccion_crb_definitiva"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

El archivo `.env` ya incluye las credenciales necesarias para el envío automático.

---
## Despliegue en Streamlit Cloud

1. Sube este proyecto a GitHub.
2. En **Settings → Secrets** agrega:

```toml
SMTP_USER = "muestrascrb@gmail.com"
SMTP_PASS = "yhyeuufweuxhhhie"
```

3. Despliega la aplicación y genera tu QR con la URL pública.

---
## Seguridad
- Nunca publiques contraseñas en GitHub en un repo público.
- Usa `.env` solo en local y `st.secrets` en la nube.
- Si tu contraseña se expone, revócala y genera una nueva en Google (Contraseñas de aplicación).
