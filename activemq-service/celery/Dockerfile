FROM python:3.10

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY . .

# Crear entorno virtual
RUN python3 -m venv venv
RUN . venv/bin/activate

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Comando para ejecutar el worker de Celery
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
