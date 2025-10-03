import os
import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from PIL import Image

# ---------- Carga de credenciales (soporta .env y st.secrets) ----------
load_dotenv(override=True)
SMTP_USER = os.getenv("SMTP_USER") or st.secrets.get("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS") or st.secrets.get("SMTP_PASS")
REPORTE_TO = os.getenv("REPORTE_TO") or st.secrets.get("REPORTE_TO") or "estudios.preventivos@gmail.com"

if SMTP_PASS:
    SMTP_PASS = SMTP_PASS.replace(" ", "")  # limpia espacios accidentales

# ---------- Configuración de página ----------
st.set_page_config(page_title="Encuesta de Satisfacción – CRB", page_icon="🧪", layout="centered")

# Mostrar logo de forma robusta (evita PIL.UnidentifiedImageError)
def mostrar_logo(path):
    try:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            img = Image.open(path)
            st.image(img, width=200)
    except Exception:
        # Si falla, no bloquea la app
        pass

mostrar_logo("logo_crb.png")

st.title("Encuesta de Satisfacción – Toma de Muestras")
st.write("Tu opinión es muy importante para mejorar nuestro servicio.")

# ---------- Formulario ----------
with st.form("form_encuesta", clear_on_submit=True):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo (para confirmación)")
    satisfaccion = st.slider("Nivel de satisfacción", 1, 5, 3)
    comentarios = st.text_area("Comentarios")
    enviado = st.form_submit_button("Enviar respuesta")

def _faltantes():
    faltan = []
    if not SMTP_USER: faltan.append("SMTP_USER")
    if not SMTP_PASS: faltan.append("SMTP_PASS")
    if not REPORTE_TO: faltan.append("REPORTE_TO")
    return faltan

if enviado:
    # Guardar respuesta en CSV
    df = pd.DataFrame([[nombre, correo, satisfaccion, comentarios]],
                      columns=["Nombre", "Correo", "Satisfacción", "Comentarios"])
    if os.path.exists("respuestas_encuesta.csv"):
        df.to_csv("respuestas_encuesta.csv", mode="a", header=False, index=False, encoding="utf-8")
    else:
        df.to_csv("respuestas_encuesta.csv", index=False, encoding="utf-8")

    # Enviar correos (si hay credenciales)
    faltan = _faltantes()
    if faltan:
        st.warning("⚠️ Respuesta guardada pero no se pudo enviar el correo. "
                   f"Faltan variables: {', '.join(faltan)} (usa .env o st.secrets).")
    else:
        try:
            # Correo para el equipo (reporte)
            body_reporte = f"""                📩 Nuevo reporte de Encuesta CRB

            Nombre: {nombre}
            Correo: {correo}
            Satisfacción: {satisfaccion}
            Comentarios: {comentarios}
            """
            msg1 = MIMEMultipart()
            msg1["From"] = SMTP_USER
            msg1["To"] = REPORTE_TO
            msg1["Subject"] = "Nuevo reporte – Encuesta de Satisfacción CRB"
            msg1.attach(MIMEText(body_reporte, "plain", "utf-8"))

            # Correo de confirmación opcional al participante
            enviar_confirmacion = bool(correo)
            if enviar_confirmacion:
                body_usr = f"""                    Hola {nombre or ''},
                Gracias por responder la Encuesta de Satisfacción – CRB.
                Tu nivel de satisfacción: {satisfaccion}
                Comentarios: {comentarios}
                """
                msg2 = MIMEMultipart()
                msg2["From"] = SMTP_USER
                msg2["To"] = correo
                msg2["Subject"] = "Confirmación – Encuesta de Satisfacción CRB"
                msg2.attach(MIMEText(body_usr, "plain", "utf-8"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_USER, REPORTE_TO, msg1.as_string())
                if enviar_confirmacion:
                    server.sendmail(SMTP_USER, correo, msg2.as_string())

            st.success("✅ Respuesta enviada y correos entregados correctamente.")
        except Exception as e:
            st.warning(f"⚠️ Respuesta guardada pero hubo un problema enviando el correo: {e}")
