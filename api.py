"""
XENDAR — API REST de Telemetría IoT
Endpoint para recepción de datos HTTP POST desde el ESP32 (Valija IoT).
Ruta requerida: /api/telemetria
Soporta: Telemetría de hardware, contadores de agua y Botón de Pánico (Pin 18).
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import database

# Intentar usar FastAPI con Pydantic; si no estuviera instalado localmente, fallback a Starlette
try:
    from fastapi import FastAPI, HTTPException, Request, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field

    USE_FASTAPI = True

    class TelemetryPayload(BaseModel):
        wifi_ok: bool = Field(..., description="Estado del módulo WiFi")
        chiller_ok: bool = Field(..., description="Estado del Chiller (Agua fría)")
        boiler_ok: bool = Field(..., description="Estado del Boiler (Agua caliente)")
        luces_ok: bool = Field(..., description="Estado del sistema de luces")
        despachos_frio: int = Field(..., ge=0, description="Cantidad de despachos de agua fría")
        despachos_calor: int = Field(..., ge=0, description="Cantidad de despachos de agua caliente")
        panico_activo: bool = Field(default=False, description="Estado del Botón de Pánico / Emergencia (Pin 18)")

        class Config:
            json_schema_extra = {
                "example": {
                    "wifi_ok": True,
                    "chiller_ok": True,
                    "boiler_ok": False,
                    "luces_ok": True,
                    "despachos_frio": 12,
                    "despachos_calor": 5,
                    "panico_activo": False
                }
            }

    app = FastAPI(
        title="Xendar — IoT Telemetry API",
        version="2.1.0",
        description="API para recepción de eventos y telemetría de la Valija IoT ESP32 (Xendar)",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {
            "service": "Xendar IoT Telemetry API",
            "station": "Demo",
            "endpoint": "/api/telemetria",
            "docs": "/docs",
            "status": "online"
        }

    @app.get("/health")
    def health():
        return {"status": "ok", "timestamp": datetime.now().isoformat()}

    @app.post("/api/telemetria", status_code=status.HTTP_201_CREATED)
    def receive_telemetry(payload: TelemetryPayload):
        data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
        record_id = database.save_telemetry(data, station="Demo")
        
        # Identificar alarmas de hardware (cuando un booleano es False)
        failing_modules = []
        if not data["wifi_ok"]:
            failing_modules.append("wifi")
        if not data["chiller_ok"]:
            failing_modules.append("chiller")
        if not data["boiler_ok"]:
            failing_modules.append("boiler")
        if not data["luces_ok"]:
            failing_modules.append("luces")

        return {
            "status": "ok",
            "message": "Telemetría registrada exitosamente",
            "record_id": record_id,
            "station": "Demo",
            "panico_activo": data.get("panico_activo", False),
            "has_faults": len(failing_modules) > 0,
            "failing_modules": failing_modules,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    @app.get("/api/telemetria/latest")
    def get_latest():
        latest = database.get_latest_telemetry("Demo")
        if not latest:
            return JSONResponse(
                status_code=200,
                content={"status": "waiting", "message": "Esperando primer envío del ESP32", "data": None}
            )
        return {"status": "ok", "data": latest}

    @app.get("/api/telemetria/history")
    def get_history(limit: int = 50):
        history = database.get_telemetry_history("Demo", limit=limit)
        return {"status": "ok", "count": len(history), "data": history}

    @app.post("/api/telemetria/reset")
    def reset_data():
        database.reset_telemetry("Demo")
        return {"status": "ok", "message": "Datos de telemetría de estación Demo reseteados"}

except ImportError:
    # Fallback Starlette nativo
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware

    USE_FASTAPI = False

    async def root(request):
        return JSONResponse({
            "service": "Xendar IoT Telemetry API (Starlette mode)",
            "station": "Demo",
            "endpoint": "/api/telemetria",
            "status": "online"
        })

    async def health(request):
        return JSONResponse({"status": "ok", "timestamp": datetime.now().isoformat()})

    async def receive_telemetry(request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"status": "error", "message": "JSON inválido"}, status_code=400)

        required_keys = ["wifi_ok", "chiller_ok", "boiler_ok", "luces_ok", "despachos_frio", "despachos_calor"]
        missing = [k for k in required_keys if k not in body]
        if missing:
            return JSONResponse(
                {"status": "error", "message": f"Faltan campos obligatorios: {', '.join(missing)}"},
                status_code=422
            )

        data = {
            "wifi_ok": bool(body["wifi_ok"]),
            "chiller_ok": bool(body["chiller_ok"]),
            "boiler_ok": bool(body["boiler_ok"]),
            "luces_ok": bool(body["luces_ok"]),
            "despachos_frio": int(body["despachos_frio"]),
            "despachos_calor": int(body["despachos_calor"]),
            "panico_activo": bool(body.get("panico_activo", False)),
        }

        record_id = database.save_telemetry(data, station="Demo")

        failing_modules = []
        if not data["wifi_ok"]:
            failing_modules.append("wifi")
        if not data["chiller_ok"]:
            failing_modules.append("chiller")
        if not data["boiler_ok"]:
            failing_modules.append("boiler")
        if not data["luces_ok"]:
            failing_modules.append("luces")

        return JSONResponse({
            "status": "ok",
            "message": "Telemetría registrada exitosamente",
            "record_id": record_id,
            "station": "Demo",
            "panico_activo": data["panico_activo"],
            "has_faults": len(failing_modules) > 0,
            "failing_modules": failing_modules,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }, status_code=201)

    async def get_latest(request):
        latest = database.get_latest_telemetry("Demo")
        return JSONResponse({"status": "ok", "data": latest})

    async def get_history(request):
        history = database.get_telemetry_history("Demo", limit=50)
        return JSONResponse({"status": "ok", "count": len(history), "data": history})

    async def reset_data(request):
        database.reset_telemetry("Demo")
        return JSONResponse({"status": "ok", "message": "Datos de telemetría de estación Demo reseteados"})

    routes = [
        Route("/", endpoint=root, methods=["GET"]),
        Route("/health", endpoint=health, methods=["GET"]),
        Route("/api/telemetria", endpoint=receive_telemetry, methods=["POST"]),
        Route("/api/telemetria/latest", endpoint=get_latest, methods=["GET"]),
        Route("/api/telemetria/history", endpoint=get_history, methods=["GET"]),
        Route("/api/telemetria/reset", endpoint=reset_data, methods=["POST"]),
    ]

    middleware = [
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    ]

    app = Starlette(debug=True, routes=routes, middleware=middleware)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"Iniciando API de telemetría en http://0.0.0.0:{port}")
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
