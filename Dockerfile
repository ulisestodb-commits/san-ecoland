FROM python:3.11-slim

# Instalar Nginx, curl y herramientas de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Limpiar configuraciones por defecto de Nginx en Debian
RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/conf.d/default.conf

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
EXPOSE 8080 8501

CMD ["./start.sh"]
