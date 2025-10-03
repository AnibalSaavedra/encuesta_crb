import os
import streamlit as st
import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from PIL import Image

# ---------- Carga de credenciales ----------
load_dotenv(override=True)
SMTP_USER = os.getenv("SMTP_USER") or st.secrets.get("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS") or st.secrets.get("SMTP_PASS")
REPORTE_TO = os.getenv("REPORTE_TO") or st.secrets.get("REPORTE_TO") or "estudios.preventivos@gmail.com"
if SMTP_PASS:
    SMTP_PASS = SMTP_PASS.replace(" ", "")  # elimina espacios

# ---------- Página ----------
st.set_page_config(page_title="Encuesta de Satisfacción – CRB", page_icon="🧪", layout="centered")
def mostrar_logo(path):
    try:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            st.image(Image.open(path), width=200)
    except Exception:
        pass

mostrar_logo("logo_crb.png")
st.title("Encuesta de Satisfacción – Toma de Muestras")
st.write("Tu opinión es muy importante para mejorar nuestro servicio.")

# ---------- Formulario (igual al original) ----------
with st.form("form_encuesta", clear_on_submit=True):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo (para confirmación)")
    satisfaccion = st.slider("Nivel de satisfacción", 1, 5, 3)
    comentarios = st.text_area("Comentarios")
    enviado = st.form_submit_button("Enviar respuesta")

def enviar_correo(recip, subject, body):
    # Intenta SSL:465 y luego STARTTLS:587
    ctx = ssl.create_default_context()
    # Primer intento: SSL 465
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
            server.login(SMTP_USER, SMTP_PASS)
            msg = MIMEMultipart()
            msg["From"] = SMTP_USER
            msg["To"] = recip
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            server.sendmail(SMTP_USER, recip, msg.as_string())
        return True, "SSL465 OK"
    except Exception as e_ssl:
        # Segundo intento: STARTTLS 587
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls(context=ctx)
                server.login(SMTP_USER, SMTP_PASS)
                msg = MIMEMultipart()
                msg["From"] = SMTP_USER
                msg["To"] = recip
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain", "utf-8"))
                server.sendmail(SMTP_USER, recip, msg.as_string())
            return True, "STARTTLS587 OK"
        except Exception as e_tls:
            return False, f"SSL:{e_ssl} | TLS:{e_tls}"

if enviado:
    # Guardar CSV
    df = pd.DataFrame([[nombre, correo, satisfaccion, comentarios]],
                      columns=["Nombre", "Correo", "Satisfacción", "Comentarios"])
    if os.path.exists("respuestas_encuesta.csv"):
        df.to_csv("respuestas_encuesta.csv", mode="a", header=False, index=False, encoding="utf-8")
    else:
        df.to_csv("respuestas_encuesta.csv", index=False, encoding="utf-8")

    if not (SMTP_USER and SMTP_PASS and REPORTE_TO):
        faltan = [k for k,v in {"SMTP_USER":SMTP_USER,"SMTP_PASS":SMTP_PASS,"REPORTE_TO":REPORTE_TO}.items() if not v]
        st.warning("⚠️ Respuesta guardada pero no se pudo enviar el correo. Faltan: " + ", ".join(faltan))
    else:
        body_rep = f"""            📩 Nuevo reporte de Encuesta CRB

        Nombre: {nombre}
        Correo: {correo}
        Satisfacción: {satisfaccion}
        Comentarios: {comentarios}
        """
        ok1, info1 = enviar_correo(REPORTE_TO, "Nuevo reporte – Encuesta de Satisfacción CRB", body_rep)
        ok2, info2 = (True, "skip")
        if correo:
            body_usr = f"""                Hola {nombre or ''},
            Gracias por responder la Encuesta de Satisfacción – CRB.
            Tu nivel de satisfacción: {satisfaccion}
            Comentarios: {comentarios}
            """
            ok2, info2 = enviar_correo(correo, "Confirmación – Encuesta de Satisfacción CRB", body_usr)

        if ok1 and ok2:
            st.success("✅ Respuesta enviada y correos entregados correctamente.")
        else:
            st.warning(f"⚠️ Respuesta guardada pero hubo un problema enviando el correo. Detalles: reporte={info1}, confirmación={info2}")
