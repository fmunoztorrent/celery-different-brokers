FROM python:3.9-slim

# Crear un usuario no root
RUN groupadd -r celery && useradd -r -g celery celery

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos y la configuración de Celery al contenedor
COPY requirements.txt requirements.txt
COPY celeryconfig.py celeryconfig.py

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Cambiar el usuario a celery
USER celery

# Establecer el comando por defecto para ejecutar Celery
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
