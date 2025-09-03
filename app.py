import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ---------- Carga de credenciales ----------
load_dotenv(override=True)
SMTP_USER = os.getenv("SMTP_USER") or st.secrets.get("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS") or st.secrets.get("SMTP_PASS")

if SMTP_PASS:
    SMTP_PASS = SMTP_PASS.replace(" ", "")

# ---------- Configuración de página ----------
st.set_page_config(page_title="Encuesta de Satisfacción", page_icon="🧪", layout="centered")

st.image("logo_crb.png", width=200)
st.title("Encuesta de Satisfacción – Toma de Muestras")
st.write("Tu opinión es muy importante para mejorar nuestro servicio. Completa esta encuesta en menos de 2 minutos.")

# ---------- Formulario ----------
nombre_rut = st.text_input("Identificación (Nombre / RUT)")
correo = st.text_input("Correo electrónico (opcional)")
fecha_atencion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.text_input("Fecha de atención", value=fecha_atencion, disabled=True)

expectativas = st.text_area("1. ¿Qué esperas de una toma de muestras? (Expectativas)", placeholder="Ej.: rapidez, trato amable, información clara...")
cumplimiento = st.radio("2. ¿Tu atención cumplió con lo que esperabas?", ["Sí", "Parcialmente", "No"], horizontal=True)
mejoras = st.text_area("3. ¿Cómo podríamos mejorar, para cumplir con lo que esperabas?")
comentario = st.text_area("Comentario adicional (opcional)")

if st.button("Enviar respuesta", type="primary", use_container_width=True):
    if not nombre_rut.strip():
        st.error("⚠️ Debes ingresar tu nombre o RUT antes de enviar.")
    else:
        nueva_respuesta = {
            "Fecha": fecha_atencion,
            "Nombre/RUT": nombre_rut.strip(),
            "Correo": correo.strip(),
            "Expectativas": (expectativas or "").strip(),
            "Cumplimiento": cumplimiento,
            "Mejoras": (mejoras or "").strip(),
            "Comentario": (comentario or "").strip(),
        }

        try:
            df = pd.read_csv("respuestas_encuesta.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Fecha","Nombre/RUT","Correo","Expectativas","Cumplimiento","Mejoras","Comentario"])
        df = pd.concat([df, pd.DataFrame([nueva_respuesta])], ignore_index=True)
        df.to_csv("respuestas_encuesta.csv", index=False, encoding="utf-8-sig")

        # Envío de correo
        try:
            if not (SMTP_USER and SMTP_PASS):
                raise RuntimeError("Faltan SMTP_USER/SMTP_PASS (usa .env, variables de entorno o st.secrets)")

            cuerpo = f"""
Nueva respuesta recibida

Fecha: {nueva_respuesta['Fecha']}
Nombre/RUT: {nueva_respuesta['Nombre/RUT']}
Correo: {nueva_respuesta['Correo']}
Expectativas: {nueva_respuesta['Expectativas']}
Cumplimiento: {nueva_respuesta['Cumplimiento']}
Mejoras: {nueva_respuesta['Mejoras']}
Comentario: {nueva_respuesta['Comentario']}
"""
            msg = MIMEText(cuerpo, _charset="utf-8")
            msg["Subject"] = "Nueva respuesta – Encuesta de Satisfacción (Toma de Muestras)"
            msg["From"] = SMTP_USER
            msg["To"] = SMTP_USER

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)

            st.success("✅ ¡Gracias por tu opinión! Tu respuesta ha sido registrada y enviada al correo.")
        except Exception as e:
            st.warning(f"⚠️ Respuesta guardada pero no se pudo enviar el correo. Detalle: {e}")
