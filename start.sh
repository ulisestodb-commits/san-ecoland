#!/usr/bin/env bash
set -e

# Railway asigna el puerto dinámicamente mediante $PORT
PORT=${PORT:-8080}
echo "=== Iniciando San Ecoland Telemetry en puerto Railway: $PORT ==="

# 1. Iniciar FastAPI en segundo plano (puerto interno 8000)
echo "Iniciando backend FastAPI / Uvicorn en puerto 8000..."
uvicorn api:app --host 127.0.0.1 --port 8000 &

# 2. Iniciar Streamlit en segundo plano (puerto interno 8501)
echo "Iniciando frontend Streamlit en puerto 8501..."
streamlit run app.py \
    --server.port=8501 \
    --server.address=127.0.0.1 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false &

# 3. Reemplazar puerto en nginx.conf dinámicamente
sed -i "s/listen 8080;/listen ${PORT};/g" /etc/nginx/nginx.conf

# 4. Iniciar Nginx en primer plano como punto de entrada único
echo "Iniciando Nginx reverse proxy en puerto $PORT..."
exec nginx -g 'daemon off;'
