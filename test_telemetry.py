"""
Test script para simular el envío HTTP POST desde el ESP32
"""

import sys
import os
import json

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database

def test_database_and_payload():
    print("1. Limpiando base de datos...")
    database.reset_telemetry("Demo")
    
    # Payload exacto del ESP32
    payload = {
        "wifi_ok": True,
        "chiller_ok": True,
        "boiler_ok": False,
        "luces_ok": True,
        "despachos_frio": 12,
        "despachos_calor": 5
    }
    
    print("\n2. Guardando payload del ESP32:")
    print(json.dumps(payload, indent=2))
    
    rec_id = database.save_telemetry(payload, station="Demo")
    print(f"-> Registro guardado con ID: {rec_id}")
    
    print("\n3. Leyendo último registro guardado:")
    latest = database.get_latest_telemetry("Demo")
    print(json.dumps(latest, indent=2))
    
    # Verificaciones
    assert latest is not None
    assert latest["wifi_ok"] is True
    assert latest["chiller_ok"] is True
    assert latest["boiler_ok"] is False  # Boiler con falla!
    assert latest["luces_ok"] is True
    assert latest["despachos_frio"] == 12
    assert latest["despachos_calor"] == 5
    
    # Cálculo de Litros: cada despacho = 0.25 L
    litros_frio = latest["despachos_frio"] * 0.25
    litros_calor = latest["despachos_calor"] * 0.25
    print(f"\n4. Cálculos de volumen:")
    print(f"   Agua fría suministrada: {litros_frio:.2f} L (esperado: 3.00 L)")
    print(f"   Agua caliente suministrada: {litros_calor:.2f} L (esperado: 1.25 L)")
    assert litros_frio == 3.0
    assert litros_calor == 1.25

    print("\n✅ Todas las aserciones pasaron correctamente!")

if __name__ == "__main__":
    test_database_and_payload()
