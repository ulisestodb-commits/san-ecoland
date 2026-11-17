"""
Script de desarrollo local para ejecutar FastAPI y Streamlit simultáneamente.
Uso: python run_local.py
"""

import subprocess
import sys
import time
import os

def run():
    print("=" * 60)
    print("🌿 SAN ECOLAND — Servidor Local de Desarrollo")
    print("=" * 60)
    print("Iniciando:")
    print("  • Backend FastAPI:   http://localhost:8000 (API: http://localhost:8000/api/telemetria)")
    print("  • Frontend Streamlit: http://localhost:8501")
    print("=" * 60)
    print("Presiona Ctrl+C para detener ambos servidores.\n")

    api_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
    )

    time.sleep(1)

    app_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"]
    )

    try:
        while True:
            time.sleep(1)
            if api_proc.poll() is not None:
                print("El proceso de FastAPI se detuvo.")
                break
            if app_proc.poll() is not None:
                print("El proceso de Streamlit se detuvo.")
                break
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")
    finally:
        api_proc.terminate()
        app_proc.terminate()
        print("Servidores detenidos.")

if __name__ == "__main__":
    run()
