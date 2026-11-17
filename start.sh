#!/usr/bin/env bash
set -e

PORT=${PORT:-8080}
echo "=== Iniciando San Ecoland Telemetry en puerto Railway: $PORT ==="

# 1. Iniciar FastAPI en segundo plano (puerto interno 8001)
echo "Iniciando backend FastAPI en puerto 8001..."
uvicorn api:app --host 127.0.0.1 --port 8001 &

# 2. Iniciar Streamlit en segundo plano (puerto interno 8502)
echo "Iniciando frontend Streamlit en puerto 8502..."
streamlit run app.py \
    --server.port=8502 \
    --server.address=127.0.0.1 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false &

# 3. Esperar que FastAPI y Streamlit estén listos antes de levantar Nginx
echo "Esperando que los servicios internos respondan..."
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:8001/health > /dev/null 2>&1 && curl -s http://127.0.0.1:8502/_stcore/health > /dev/null 2>&1; then
        echo "Servicios internos listos en el intento $i!"
        break
    fi
    sleep 1
done

# 4. Inyectar puerto dinámico en Nginx
sed -i "s/listen 8080;/listen ${PORT};/g" /etc/nginx/nginx.conf

# 5. Probar configuración de Nginx
nginx -t

# 6. Iniciar Nginx en primer plano
echo "Iniciando Nginx reverse proxy en puerto $PORT..."
exec nginx -g 'daemon off;'
