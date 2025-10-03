# Encuesta Satisfacción CRB – compatibilidad SMTP (SSL y STARTTLS)

## Configuración de Google (obligatorio)
1) Habilita **Verificación en 2 pasos** en la cuenta `estudios.preventivos@gmail.com`.
2) Crea una **Contraseña de aplicación** (tipo: Mail / Dispositivo: Other).
3) Copia esa contraseña aquí como `SMTP_PASS` (sin espacios).

## Secrets en Streamlit Cloud
```toml
SMTP_USER = "estudios.preventivos@gmail.com"
SMTP_PASS = "utkiwdegorrlinmq"
REPORTE_TO = "estudios.preventivos@gmail.com"
```

## Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Anotaciones
- La app prueba **SSL (465)** y, si falla, **STARTTLS (587)**.
- Si ves `535 5.7.8 Username and Password not accepted`, revisa:
  - Que el **SMTP_USER** coincide con la cuenta que generó la **contraseña de aplicación**.
  - Que pegaste la contraseña **sin espacios**.
  - Que en **Settings → Secrets** no haya comillas curvas o caracteres extraños.
