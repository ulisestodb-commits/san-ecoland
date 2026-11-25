"""
Simulador de ESP32 para enviar telemetría a la API de Xendar.
Uso:
    python simulate_esp32.py [URL_DESTINO] [--panic]
Ejemplo local:
    python simulate_esp32.py http://localhost:8000/api/telemetria
    python simulate_esp32.py http://localhost:8000/api/telemetria --panic
Ejemplo Railway:
    python simulate_esp32.py https://san-ecoland.up.railway.app/api/telemetria
    python simulate_esp32.py https://san-ecoland.up.railway.app/api/telemetria --panic
"""

import sys
import json
import urllib.request
import urllib.error

DEFAULT_URL = "http://localhost:8000/api/telemetria"

def send_telemetry(url=DEFAULT_URL, panic=False):
    payload = {
        "wifi_ok": True,
        "chiller_ok": True,
        "boiler_ok": False,
        "luces_ok": True,
        "despachos_frio": 12,
        "despachos_calor": 5,
        "panico_activo": panic
    }

    print(f"\n📡 Enviando telemetría a: {url}")
    print(f"🚨 Estado de Pánico: {'ACTIVADO' if panic else 'Normal (Inactivo)'}")
    print("📦 Payload:")
    print(json.dumps(payload, indent=2))

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_code = response.getcode()
            res_body = response.read().decode("utf-8")
            print(f"\n✅ Respuesta del Servidor (Status {res_code}):")
            print(json.dumps(json.loads(res_body), indent=2))
    except urllib.error.HTTPError as e:
        print(f"\n❌ Error HTTP {e.code}: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"\n❌ Error de conexión: {e.reason}")
        print("Asegúrate de que el backend de FastAPI esté corriendo (ej. 'uvicorn api:app --port 8000')")

if __name__ == "__main__":
    args = sys.argv[1:]
    is_panic = "--panic" in args
    target_args = [a for a in args if a != "--panic"]
    target_url = target_args[0] if len(target_args) > 0 else DEFAULT_URL
    send_telemetry(target_url, panic=is_panic)
