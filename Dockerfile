FROM python:3.11-slim

# Instalar Nginx y dependencias de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Permisos de ejecución para el script de inicio
RUN chmod +x start.sh

# Puerto estándar que Railway mapea mediante $PORT
EXPOSE 8080

CMD ["./start.sh"]
