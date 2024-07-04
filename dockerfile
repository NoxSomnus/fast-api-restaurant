# Establece la imagen base
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt a /app
COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta app a /app en el contenedor
COPY app/ .

# Expone el puerto que utiliza tu aplicaciÃ³n FastAPI (por ejemplo, el puerto 8000)
EXPOSE 8000

# Ejecuta el servidor uvicorn con tu archivo main.py como punto de entrada
CMD ["uvicorn", "main:app"]