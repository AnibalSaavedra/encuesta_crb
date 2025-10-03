# Encuesta Satisfacción CRB – con REPORTE_TO configurable

## Credenciales (dos opciones)
**A) Local con `.env`** (incluido):
```env
SMTP_USER="estudios.preventivos@gmail.com"
SMTP_PASS="utki wdeg orrl inmq"
REPORTE_TO="estudios.preventivos@gmail.com"
```
> La app limpia espacios en `SMTP_PASS` automáticamente.

**B) Streamlit Cloud – `Settings → Secrets`**:
```toml
SMTP_USER = "estudios.preventivos@gmail.com"
SMTP_PASS = "utki wdeg orrl inmq"
REPORTE_TO = "estudios.preventivos@gmail.com"
```

## Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notas
- Cambia el correo de reportes solo editando `REPORTE_TO` (en `.env` o `st.secrets`), sin tocar el código.
- Los resultados quedan en `respuestas_encuesta.csv` (modo append).
