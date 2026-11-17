"""
SAN ECOLAND — Base de Datos de Telemetría (SQLite WAL)
Gestiona la persistencia thread-safe de eventos IoT enviados por el ESP32.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "telemetry.db"))


def get_connection() -> sqlite3.Connection:
    """Crea una conexión con timeout y modo WAL para alta concurrencia."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_db():
    """Inicializa las tablas de telemetría si no existen."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                station TEXT NOT NULL DEFAULT 'Demo',
                timestamp TEXT NOT NULL,
                wifi_ok INTEGER NOT NULL,
                chiller_ok INTEGER NOT NULL,
                boiler_ok INTEGER NOT NULL,
                luces_ok INTEGER NOT NULL,
                despachos_frio INTEGER NOT NULL,
                despachos_calor INTEGER NOT NULL,
                raw_payload TEXT
            );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_station_time ON telemetry(station, id DESC);")
        conn.commit()


def save_telemetry(data: Dict[str, Any], station: str = "Demo") -> int:
    """
    Inserta un nuevo registro de telemetría proveniente del ESP32.
    """
    init_db()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wifi_ok = 1 if data.get("wifi_ok") else 0
    chiller_ok = 1 if data.get("chiller_ok") else 0
    boiler_ok = 1 if data.get("boiler_ok") else 0
    luces_ok = 1 if data.get("luces_ok") else 0
    despachos_frio = int(data.get("despachos_frio", 0))
    despachos_calor = int(data.get("despachos_calor", 0))
    raw_payload = json.dumps(data)

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO telemetry 
            (station, timestamp, wifi_ok, chiller_ok, boiler_ok, luces_ok, despachos_frio, despachos_calor, raw_payload)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (station, ts, wifi_ok, chiller_ok, boiler_ok, luces_ok, despachos_frio, despachos_calor, raw_payload)
        )
        conn.commit()
        return cursor.lastrowid


def get_latest_telemetry(station: str = "Demo") -> Optional[Dict[str, Any]]:
    """Obtiene el último paquete de telemetría recibido para la estación."""
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, station, timestamp, wifi_ok, chiller_ok, boiler_ok, luces_ok, 
                   despachos_frio, despachos_calor, raw_payload
            FROM telemetry 
            WHERE station = ? 
            ORDER BY id DESC LIMIT 1
            """,
            (station,)
        ).fetchone()

        if not row:
            return None

        return {
            "id": row["id"],
            "station": row["station"],
            "timestamp": row["timestamp"],
            "wifi_ok": bool(row["wifi_ok"]),
            "chiller_ok": bool(row["chiller_ok"]),
            "boiler_ok": bool(row["boiler_ok"]),
            "luces_ok": bool(row["luces_ok"]),
            "despachos_frio": row["despachos_frio"],
            "despachos_calor": row["despachos_calor"],
            "raw_payload": row["raw_payload"],
        }


def get_telemetry_history(station: str = "Demo", limit: int = 50) -> List[Dict[str, Any]]:
    """Obtiene los últimos N registros en orden cronológico ascendente."""
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, station, timestamp, wifi_ok, chiller_ok, boiler_ok, luces_ok, 
                   despachos_frio, despachos_calor
            FROM (
                SELECT * FROM telemetry 
                WHERE station = ? 
                ORDER BY id DESC LIMIT ?
            )
            ORDER BY id ASC
            """,
            (station, limit)
        ).fetchall()

        return [
            {
                "id": r["id"],
                "station": r["station"],
                "timestamp": r["timestamp"],
                "wifi_ok": bool(r["wifi_ok"]),
                "chiller_ok": bool(r["chiller_ok"]),
                "boiler_ok": bool(r["boiler_ok"]),
                "luces_ok": bool(r["luces_ok"]),
                "despachos_frio": r["despachos_frio"],
                "despachos_calor": r["despachos_calor"],
            }
            for r in rows
        ]


def get_telemetry_stats(station: str = "Demo") -> Dict[str, Any]:
    """Calcula totales acumulados y conteos."""
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT 
                COUNT(*) as total_events,
                SUM(despachos_frio) as sum_frio,
                SUM(despachos_calor) as sum_calor,
                MAX(despachos_frio) as max_frio,
                MAX(despachos_calor) as max_calor
            FROM telemetry
            WHERE station = ?
            """,
            (station,)
        ).fetchone()

        latest = get_latest_telemetry(station)

        return {
            "total_events": row["total_events"] if row else 0,
            "sum_frio": row["sum_frio"] if row and row["sum_frio"] else 0,
            "sum_calor": row["sum_calor"] if row and row["sum_calor"] else 0,
            "max_frio": row["max_frio"] if row and row["max_frio"] else 0,
            "max_calor": row["max_calor"] if row and row["max_calor"] else 0,
            "latest": latest,
        }


def reset_telemetry(station: str = "Demo"):
    """Elimina los datos para pruebas en blanco."""
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM telemetry WHERE station = ?", (station,))
        conn.commit()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
