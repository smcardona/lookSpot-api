FROM python:3.10-slim

# Exposa el port per HTTPS
EXPOSE 443

# Instala las dependencias del sistema necesarias para MariaDB
RUN apt update && apt install -y libmariadb-dev gcc

WORKDIR /app

# Copia les dependències (requirements.txt) dins del contenidor
COPY api/requirements.txt /app/requirements.txt

# Instal·la les dependències necessàries
RUN pip install --no-cache-dir -r requirements.txt

# Copia tota l'aplicació FastAPI dins del contenidor
COPY api /app/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/api/ssl/key.pem", "--ssl-certfile", "/app/api/ssl/cert.pem"]
