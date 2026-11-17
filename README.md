# 🌿 SAN ECOLAND — Telemetría IoT en Tiempo Real (Estación Demo)

Refactorización de la plataforma para conectar la **Valija IoT con ESP32** mediante eventos HTTP POST en tiempo real hacia una única estación denominada **"Demo"**, eliminando cualquier dato simulado o hardcodeado.

---

## 📐 Arquitectura del Sistema

```
[ ESP32 - Valija IoT ]
         │
         │  HTTP POST /api/telemetria (JSON)
         ▼
[ Nginx Reverse Proxy (Puerto $PORT Railway) ]
    ├── /api/*   ──>  [ FastAPI / Uvicorn (Puerto 8000) ]
    │                               │
    │                        (Escribe eventos)
    │                               ▼
    │                     [ SQLite (telemetry.db - WAL Mode) ]
    │                               ▲
    │                        (Lee telemetría)
    │                               │
    └── /*       ──>  [ Streamlit Dashboard (Puerto 8501) ]
```

- **Backend (FastAPI)**: Endpoint ultra ligero `/api/telemetria` que valida la estructura exacta del JSON y almacena cada evento con timestamp.
- **Base de Datos (SQLite WAL)**: `telemetry.db` configurada en modo Write-Ahead Logging (`WAL`), permitiendo lecturas concurrentes sin bloqueos de concurrencia entre FastAPI y Streamlit.
- **Frontend (Streamlit)**: Monitorea exclusivamente la estación **"Demo"**, calculando los KPIs de agua en litros y reflejando las fallas de hardware en rojo tanto en los componentes como en el panel lateral de alertas activas.
- **Despliegue en Railway**: Un único contenedor Docker orquesta FastAPI, Streamlit y Nginx, escuchando en el puerto dinámico `$PORT` de Railway.

---

## 📡 Estructura del JSON (ESP32)

El ESP32 envía peticiones `POST` a `/api/telemetria` con el siguiente cuerpo:

```json
{
  "wifi_ok": true,
  "chiller_ok": true,
  "boiler_ok": false,
  "luces_ok": true,
  "despachos_frio": 12,
  "despachos_calor": 5
}
```

### Mapeo de Componentes y Reglas de Negocio:
1. **Contadores de Suministro (0.25 L por despacho)**:
   - **Agua caliente suministrada**: `despachos_calor * 0.25 L` (ej. 5 despachos = 1.25 L).
   - **Agua fría suministrada**: `despachos_frio * 0.25 L` (ej. 12 despachos = 3.00 L).
2. **Alarmas de Hardware (Event-Driven)**:
   - Si `wifi_ok == false`: Módulo WiFi fuera de servicio (resaltado en rojo).
   - Si `chiller_ok == false`: Módulo Chiller fuera de servicio (resaltado en rojo).
   - Si `boiler_ok == false`: Módulo Boiler fuera de servicio (resaltado en rojo).
   - Si `luces_ok == false`: Módulo de Iluminación fuera de servicio (resaltado en rojo).
   - Cada falla activa se agrega a la barra lateral de **Alertas Activas**.

---

## 🚀 Ejecución en Desarrollo Local

### Opción A: Ejecutar todo con un comando
```bash
python run_local.py
```
Levanta FastAPI en `http://localhost:8000` y Streamlit en `http://localhost:8501`.

### Opción B: Ejecutar en terminales separadas
1. **Terminal 1 (Backend API)**:
   ```bash
   uvicorn api:app --reload --port 8000
   ```
2. **Terminal 2 (Frontend Dashboard)**:
   ```bash
   streamlit run app.py --server.port 8501
   ```

---

## 🧪 Simulación y Pruebas del ESP32

### Vía Python:
```bash
python simulate_esp32.py http://localhost:8000/api/telemetria
```

### Vía cURL (Windows PowerShell / Bash):
```bash
curl -X POST http://localhost:8000/api/telemetria \
  -H "Content-Type: application/json" \
  -d '{"wifi_ok": true, "chiller_ok": true, "boiler_ok": false, "luces_ok": true, "despachos_frio": 12, "despachos_calor": 5}'
```

### Desde el Dashboard:
El dashboard incluye en la barra lateral un menú desplegable **"🧪 Simulador de Hardware (ESP32)"** con botones para inyectar eventos de prueba (Falla en Boiler, 100% OK, Falla Múltiple y Limpieza de BD).

---

## ☁️ Despliegue en Railway

El proyecto incluye `Dockerfile`, `nginx.conf` y `start.sh`.

1. Subir los cambios a tu repositorio Git (GitHub/GitLab):
   ```bash
   git add .
   git commit -m "feat: endpoint telemetria esp32 y dashboard estacion demo"
   git push origin main
   ```
2. En Railway:
   - Tu proyecto detectará automáticamente el `Dockerfile`.
   - Railway asignará dinámicamente `$PORT` y Nginx enlazará dicho puerto con FastAPI (`/api/`) y Streamlit (`/`).
   - La URL pública será: `https://<tu-app>.up.railway.app`.

3. Endpoint público para el ESP32:
   ```
   POST https://<tu-app>.up.railway.app/api/telemetria
   ```

---

## 💻 Código de Ejemplo para ESP32 (Arduino / PlatformIO)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "TU_WIFI_SSID";
const char* password = "TU_WIFI_PASSWORD";
const char* serverUrl = "https://<tu-app>.up.railway.app/api/telemetria";

int despachos_frio = 12;
int despachos_calor = 5;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Conectado!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["wifi_ok"] = true;
    doc["chiller_ok"] = true;
    doc["boiler_ok"] = false;  // Falla simulada
    doc["luces_ok"] = true;
    doc["despachos_frio"] = despachos_frio;
    doc["despachos_calor"] = despachos_calor;

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);
    Serial.print("Código de respuesta HTTP: ");
    Serial.println(httpResponseCode);
    http.end();
  }
  delay(10000); // Enviar cada 10 segundos o por evento
}
```
