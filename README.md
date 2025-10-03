# Encuesta Satisfacción CRB – Fix logo + credenciales actualizadas

## Credenciales
**Local (.env incluido):**
```env
SMTP_USER="estudios.preventivos@gmail.com"
SMTP_PASS="utki wdeg orrl inmq"
REPORTE_TO="estudios.preventivos@gmail.com"
```

**Streamlit Cloud – `Settings → Secrets`:**
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
- Logo válido incluido (`logo_crb.png`) y manejo robusto ante errores (si falta o está corrupto, la app sigue).
- Resultados en `respuestas_encuesta.csv` (modo append).
