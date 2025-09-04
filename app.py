import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar credenciales desde .env
load_dotenv()
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

st.set_page_config(page_title="Encuesta Clínica Río Blanco", layout="centered")

# Logo institucional
st.image("logo_crb.png", width=200)

st.title("Encuesta de Satisfacción Usuaria")
st.write("Clínica Río Blanco – Comprometidos con la calidad y seguridad del paciente")

# -------------------------------
# Aviso de privacidad con checkbox
# -------------------------------
st.subheader("Aviso de Privacidad")
st.markdown("""
En cumplimiento de la **Ley N° 21.719 sobre Protección y Tratamiento de los Datos Personales**, 
informamos que los datos de esta encuesta serán utilizados únicamente para evaluar la satisfacción usuaria, 
identificar oportunidades de mejora y elaborar reportes internos de carácter anónimo.

Al marcar la casilla a continuación, usted declara:

**“He leído y comprendido el Aviso de Privacidad y consiento expresamente el tratamiento de mis datos personales por parte de Clínica Río Blanco para los fines señalados.”**
""")

consentimiento = st.checkbox("Acepto el Aviso de Privacidad (obligatorio)", value=False)

# -------------------------------
# Formulario de encuesta
# -------------------------------
st.subheader("Formulario de Encuesta")

nombre = st.text_input("Identificación (Nombre/RUT)")
correo = st.text_input("Correo electrónico")
fecha_atencion = datetime.today().strftime('%Y-%m-%d')

expectativas = st.text_area("¿Qué esperas de una toma de muestras?")
cumplio = st.radio("¿Tu atención cumplió con lo que esperabas?", ["Sí", "No", "Parcialmente"])
mejora = st.text_area("¿Cómo podríamos mejorar para cumplir con lo que esperabas?")
comentario = st.text_area("Comentario adicional")

# -------------------------------
# Botón de envío
# -------------------------------
if st.button("Enviar encuesta"):
    if not consentimiento:
        st.error("⚠️ Debe aceptar el Aviso de Privacidad para enviar la encuesta.")
    else:
        # Guardar respuestas en CSV
        data = {
            "Nombre/RUT": [nombre],
            "Correo": [correo],
            "Fecha atención": [fecha_atencion],
            "Expectativas": [expectativas],
            "Cumplió": [cumplio],
            "Mejora": [mejora],
            "Comentario": [comentario],
            "Consentimiento": ["Aceptado" if consentimiento else "No aceptado"],
            "Fecha registro": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        }
        df = pd.DataFrame(data)
        file_exists = os.path.isfile("respuestas_encuesta.csv")
        df.to_csv("respuestas_encuesta.csv", mode="a", header=not file_exists, index=False)

        # Enviar correo
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = SMTP_USER
        msg['Subject'] = "Nueva respuesta encuesta CRB"

        body = f"""
        Nueva respuesta registrada:

        Nombre/RUT: {nombre}
        Correo: {correo}
        Fecha atención: {fecha_atencion}
        Expectativas: {expectativas}
        Cumplió: {cumplio}
        Mejora: {mejora}
        Comentario: {comentario}
        Consentimiento: {"Aceptado" if consentimiento else "No aceptado"}
        """
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            server.quit()
            st.success("✅ Encuesta enviada correctamente. ¡Gracias por tu opinión!")
        except Exception as e:
            st.error(f"❌ Error al enviar el correo: {e}")
