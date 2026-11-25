# ⚡ XENDAR | Smart & Sustentable — Tablero de Control Ejecutivo · Telemetría IoT

Plataforma de telemetría IoT en tiempo real para estaciones de hidratación inteligentes de **Xendar** ([xendar.com.ar](https://xendar.com.ar)), conectada con la **Valija IoT con ESP32** mediante peticiones HTTPS POST basadas en eventos hacia la estación **"Demo"**.

---

## 📐 Arquitectura de Producción (Railway)

```
[ ESP32 Valija IoT (Pin 18 Pánico) ]
               │
               │  HTTPS POST /api/telemetria (JSON)
               ▼
[ Nginx Reverse Proxy (Puerto dinámico $PORT) ]
    ├── /api/*   ──>  [ FastAPI (Puerto interno 8001) ]
    │                               │
    │                        (Escribe eventos)
    │                               ▼
    │                     [ SQLite (telemetry.db - Modo WAL) ]
    │                               ▲
    │                        (Lee telemetría)
    │                               │
    └── /*       ──>  [ Streamlit Dashboard (Puerto interno 8502) ]
```

- **Backend (FastAPI)**: Endpoint ligero `/api/telemetria` que valida la estructura del JSON y persiste cada evento con timestamp.
- **Base de Datos (SQLite WAL)**: `telemetry.db` en modo Write-Ahead Logging (`WAL`), con soporte nativo para contadores, fallas de hardware y Botón de Pánico.
- **Frontend Ejecutivo (Streamlit)**: Identidad corporativa de Xendar, tipografía *Inter*, KPIs de agua en Litros, grilla de 5 módulos de hardware y alerta de emergencia prioritaria de ancho completo ante eventos de pánico.
- **Despliegue en Railway**: Contenedor Docker único orquestando Nginx, FastAPI y Streamlit con healthcheck de inicio.

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
  "despachos_calor": 5,
  "panico_activo": false
}
```

### Mapeo de Componentes y Reglas de Negocio:

1. **Botón de Pánico / Emergencia (Pin 18)**:
   - `panico_activo == true`: Dispara un **banner de emergencia de ancho completo** en rojo pulsante (`#DC2626`) en el tope del dashboard y encabeza con máxima prioridad las **Alertas Activas** en la barra lateral.
2. **Contadores de Suministro (0.25 L por despacho)**:
   - **Agua caliente suministrada**: `despachos_calor * 0.25 L` (ej. 5 despachos = 1.25 L).
   - **Agua fría suministrada**: `despachos_frio * 0.25 L` (ej. 12 despachos = 3.00 L).
   - **Total agua suministrada**: suma de ambos volúmenes.
3. **Salud de Módulos de Hardware**:
   - `wifi_ok` (Pin 14): Módulo WiFi.
   - `chiller_ok` (Pin 27): Chiller (Agua Fría).
   - `boiler_ok` (Pin 19): Boiler (Agua Caliente).
   - `luces_ok` (Pin 13): Sistema de Iluminación.
   - Si cualquiera pasa a `false`, se resalta en rojo como falla detectada y se incorpora al panel de alertas activas.

---

## 🎨 Identidad Corporativa Xendar

- **Azul Marino Principal**: `#1E334D` (Sidebar, encabezados y métricas)
- **Azul Oscuro Profundo**: `#142336` (Hover y contrastes)
- **Turquesa Corporativo**: `#2B8A91` (Acentos activos, badges OK)
- **Aqua Claro**: `#48B5B8` (Detalles sobre fondo oscuro)
- **Fondo General**: `#F4F8FA`
- **Tarjetas**: Blancas `#FFFFFF`, bordes `#E2E8F0`, radio 14px
- **Tipografía**: *Inter* (Google Fonts)

---

## 🧪 Pruebas y Simulación

### Probar con Botón de Pánico Activo vía script:
```bash
python simulate_esp32.py http://localhost:8000/api/telemetria --panic
```

### Probar en Railway:
```bash
python simulate_esp32.py https://san-ecoland.up.railway.app/api/telemetria --panic
```

### Desde el Dashboard:
En la barra lateral, expandir **"🧪 Simulador de Hardware (ESP32)"** y hacer clic en **"🚨 Simular Botón de Pánico"** o **"🟢 Normalizar Pánico"**.
