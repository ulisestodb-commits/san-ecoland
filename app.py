"""
╔══════════════════════════════════════════════════════════════╗
║              XENDAR | Smart & Sustentable                    ║
║      Tablero de Control Ejecutivo · Telemetría IoT ESP32     ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import database

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Xendar | Smart & Sustentable · Telemetría IoT",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL STYLING — Identidad Corporativa Xendar (xendar.com.ar)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Importación de Tipografía Google Fonts: Inter ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Aplicación global de fuente ── */
    html, body, [class*="css"], .stApp, * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* ── Paleta de Colores Corporativa Xendar ── */
    :root {
        --navy:        #1E334D; /* Azul Marino Principal */
        --navy-dark:   #142336; /* Azul Oscuro Profundo (hover / contraste) */
        --teal:        #2B8A91; /* Turquesa Corporativo */
        --aqua:        #48B5B8; /* Aqua Claro */
        --bg:          #F4F8FA; /* Fondo general del dashboard */
        --bg-card:     #FFFFFF; /* Tarjetas blancas */
        --border:      #E2E8F0; /* Bordes sutiles */
        --shadow:      0 2px 10px rgba(30, 51, 77, 0.05);
        --danger:      #DC2626; /* Rojo de emergencia */
        --danger-bg:   #FEE2E2;
        --danger-border: #F87171;
        --text:        #1E334D;
        --muted:       #64748B;
    }

    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    /* ── Animación de Alerta de Pánico (Pulso) ── */
    @keyframes panic-pulse {
        0%, 100% {
            background-color: #DC2626;
            box-shadow: 0 0 22px rgba(220, 38, 38, 0.65);
            border-color: #F87171;
        }
        50% {
            background-color: #991B1B;
            box-shadow: 0 0 36px rgba(220, 38, 38, 0.9);
            border-color: #FECACA;
        }
    }

    .panic-banner-emergency {
        animation: panic-pulse 1.3s infinite ease-in-out;
        border: 2px solid #F87171;
        border-radius: 14px;
        padding: 16px 22px;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .panic-banner-emergency * {
        color: #FFFFFF !important;
    }

    /* ── Encabezados ── */
    .brand-title {
        font-size: 1.85rem;
        font-weight: 900;
        margin: 0;
        color: var(--navy);
        line-height: 1.2;
        letter-spacing: -0.01em;
    }
    .brand-subtitle {
        font-size: 0.98rem;
        font-weight: 600;
        color: var(--teal);
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-top: 3px;
    }
    .brand-desc {
        margin: 4px 0 0;
        color: var(--muted);
        font-size: 0.88rem;
    }
    .sec-label {
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 0 0 12px 2px;
    }

    /* ── Sidebar Xendar ── */
    div[data-testid="stSidebarContent"] {
        background: var(--navy) !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #CBD5E1 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #FFFFFF !important; }

    /* Alerta de Pánico en Sidebar */
    .sidebar-panic-alert {
        animation: panic-pulse 1.3s infinite ease-in-out;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        margin-bottom: 10px !important;
        border: 2px solid #FECACA !important;
    }
    .sidebar-panic-alert * { color: #FFFFFF !important; }

    /* Fila de alerta de hardware en Sidebar */
    .alert-row-danger {
        background: rgba(220, 38, 38, 0.22) !important;
        border: 1px solid rgba(220, 38, 38, 0.55) !important;
        border-left: 5px solid var(--danger) !important;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 8px;
    }
    .alert-row-danger .ar-name  { color: #FFFFFF !important; font-weight: 800; font-size: 0.92rem; margin-bottom: 2px; }
    .alert-row-danger .ar-issue { color: #FCA5A5 !important; font-size: 0.82rem; font-weight: 600; }

    .alert-row-ok {
        background: rgba(43, 138, 145, 0.18) !important;
        border: 1px solid rgba(72, 181, 184, 0.4) !important;
        border-left: 5px solid var(--teal) !important;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 8px;
    }
    .alert-row-ok .ar-name  { color: #FFFFFF !important; font-weight: 800; font-size: 0.92rem; }
    .alert-row-ok .ar-issue { color: #A5F3FC !important; font-size: 0.82rem; font-weight: 600; }

    /* ── Tarjetas Métricas (KPIs de Suministro) ── */
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: var(--shadow);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 900;
        color: var(--navy);
        line-height: 1.1;
    }
    .kpi-unit {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--teal);
    }
    .kpi-sub {
        font-size: 0.84rem;
        font-weight: 600;
        color: var(--muted);
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ── Tarjetas de Componentes de Hardware & Pánico ── */
    .hw-card-ok {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-top: 4px solid var(--teal);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: var(--shadow);
        height: 100%;
    }
    .hw-card-fail {
        background: #FFF5F5 !important;
        border: 2px solid var(--danger) !important;
        border-top: 5px solid var(--danger) !important;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(220, 38, 38, 0.22) !important;
        height: 100%;
    }
    .hw-card-panic {
        animation: panic-pulse 1.3s infinite ease-in-out;
        border: 2px solid #FECACA !important;
        border-radius: 14px;
        padding: 18px 20px;
        height: 100%;
    }
    .hw-card-panic * {
        color: #FFFFFF !important;
    }

    .hw-title {
        font-size: 0.88rem;
        font-weight: 800;
        color: var(--navy);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .hw-title-fail {
        font-size: 0.88rem;
        font-weight: 800;
        color: var(--danger) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    /* ── Badges de Estado ── */
    .badge-ok {
        background: #E6F5F6;
        color: #2B8A91;
        border: 1px solid #B8E4E7;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-fail {
        background: #FEE2E2;
        color: #991B1B;
        border: 1px solid #F87171;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-waiting {
        background: #E2E8F0;
        color: #475569;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-panic {
        background: #FFFFFF;
        color: #DC2626;
        font-weight: 900;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }

    .divider { border-top: 1px solid var(--border); margin: 22px 0; }

    #MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ESPECIFICACIONES DE MÓDULOS DE HARDWARE
# ─────────────────────────────────────────────────────────────
MODULE_SPECS = {
    "wifi_ok": {
        "name": "Módulo WiFi",
        "pin": "Pin 14",
        "icon": "📶",
        "desc_ok": "Conectividad normal · Señal estable",
        "desc_fail": "Módulo WiFi fuera de servicio · Sin telemetría remota",
    },
    "chiller_ok": {
        "name": "Chiller (Agua Fría)",
        "pin": "Pin 27",
        "icon": "🧊",
        "desc_ok": "Sistema de refrigeración operativo · Temperatura óptima",
        "desc_fail": "Módulo Chiller fuera de servicio · Suministro frío suspendido",
    },
    "boiler_ok": {
        "name": "Boiler (Agua Caliente)",
        "pin": "Pin 19",
        "icon": "🔥",
        "desc_ok": "Sistema térmico operativo · Caldera lista",
        "desc_fail": "Módulo Boiler fuera de servicio · Suministro caliente suspendido",
    },
    "luces_ok": {
        "name": "Sistema de Luces",
        "pin": "Pin 13",
        "icon": "💡",
        "desc_ok": "Iluminación operativa · Consumo nominal",
        "desc_fail": "Módulo de Iluminación fuera de servicio · Falla detectada",
    },
}


# ─────────────────────────────────────────────────────────────
# RENDERIZADORES VISUALES (HTML NATIVO)
# ─────────────────────────────────────────────────────────────
def render_kpi_card(title: str, litros: float, despachos: int, accent_color: str, icon: str) -> str:
    """Genera una tarjeta métrica ejecutiva de suministro con estética Xendar."""
    return f"""
    <div class="kpi-card" style="border-top: 4px solid {accent_color};">
        <div>
            <div class="kpi-title">{icon} {title}</div>
            <div class="kpi-value">{litros:.2f} <span class="kpi-unit">L</span></div>
        </div>
        <div class="kpi-sub">
            <span>💧 <strong>{despachos}</strong> despachos</span>
            <span style="font-size:0.75rem; color:#94A3B8;">(0.25 L c/u)</span>
        </div>
    </div>
    """


def render_panic_module_card(panico_activo: bool, is_waiting: bool = False) -> str:
    """Renderiza la tarjeta del Botón de Pánico en la grilla de módulos."""
    if is_waiting:
        return """
        <div class="kpi-card" style="border-top: 4px solid #94A3B8;">
            <div class="hw-title">🚨 Botón de Pánico</div>
            <div style="font-size:0.72rem; color:#94A3B8; margin-top:-6px; margin-bottom:8px;">PIN 18 · EMERGENCIA</div>
            <div style="margin: 8px 0;"><span class="badge-waiting">⏳ EN ESPERA</span></div>
            <div style="font-size:0.82rem; color:#64748B;">Esperando datos de la estación</div>
        </div>
        """

    if panico_activo:
        return """
        <div class="hw-card-panic">
            <div style="font-size:0.88rem; font-weight:900; letter-spacing:0.04em; text-transform:uppercase;">
                🚨 BOTÓN DE PÁNICO
            </div>
            <div style="font-size:0.72rem; color:#FEE2E2; margin-top:2px; margin-bottom:8px; font-weight:700;">
                PIN 18 · EMERGENCIA ACTIVA
            </div>
            <div style="margin: 8px 0;">
                <span class="badge-panic">🚨 ALERTA ACTIVADA</span>
            </div>
            <div style="font-size:0.82rem; font-weight:700;">
                ⚠ BOTÓN ACCIONADO · Protocolo de seguridad en curso
            </div>
        </div>
        """
    else:
        return """
        <div class="hw-card-ok">
            <div class="hw-title">🚨 Botón de Pánico</div>
            <div style="font-size:0.72rem; color:#94A3B8; margin-top:-6px; margin-bottom:8px;">PIN 18 · EMERGENCIA</div>
            <div style="margin: 8px 0;">
                <span class="badge-ok">● NORMAL / STANDBY</span>
            </div>
            <div style="font-size:0.82rem; color:#2B8A91; font-weight:600;">
                ✓ Monitoreo activo · Sin activación
            </div>
        </div>
        """


def render_hardware_card(key: str, is_ok: bool, is_waiting: bool = False) -> str:
    """Renderiza una tarjeta de módulo de hardware (WiFi, Chiller, Boiler, Luces)."""
    spec = MODULE_SPECS[key]
    name = spec["name"]
    pin = spec["pin"]
    icon = spec["icon"]

    if is_waiting:
        return f"""
        <div class="kpi-card" style="border-top: 4px solid #94A3B8;">
            <div class="hw-title">{icon} {name}</div>
            <div style="font-size:0.72rem; color:#94A3B8; margin-top:-6px; margin-bottom:8px;">{pin}</div>
            <div style="margin: 8px 0;"><span class="badge-waiting">⏳ EN ESPERA</span></div>
            <div style="font-size:0.82rem; color:#64748B;">Esperando datos de la estación</div>
        </div>
        """

    if is_ok:
        return f"""
        <div class="hw-card-ok">
            <div class="hw-title">{icon} {name}</div>
            <div style="font-size:0.72rem; color:#94A3B8; margin-top:-6px; margin-bottom:8px;">{pin}</div>
            <div style="margin: 8px 0;">
                <span class="badge-ok">● OPERATIVO</span>
            </div>
            <div style="font-size:0.82rem; color:#2B8A91; font-weight:600;">
                ✓ {spec['desc_ok']}
            </div>
        </div>
        """
    else:
        return f"""
        <div class="hw-card-fail">
            <div class="hw-title-fail">🚨 {icon} {name}</div>
            <div style="font-size:0.72rem; color:#DC2626; margin-top:-6px; margin-bottom:8px; font-weight:700;">{pin} · FUERA DE SERVICIO</div>
            <div style="margin: 8px 0;">
                <span class="badge-fail">✖ FALLA DETECTADA</span>
            </div>
            <div style="font-size:0.82rem; color:#DC2626; font-weight:700;">
                ⚠ {spec['desc_fail']}
            </div>
        </div>
        """


# ─────────────────────────────────────────────────────────────
# FRAGMENTO DE ALERTAS EN SIDEBAR (Auto-actualizable en tiempo real)
# ─────────────────────────────────────────────────────────────
@st.fragment(run_every="2s")
def render_sidebar_alerts():
    """Monitorea la base de datos y actualiza las alertas en la barra lateral en tiempo real."""
    latest = database.get_latest_telemetry("Demo")
    active_alarms = []
    panico_activo = False

    if latest:
        panico_activo = bool(latest.get("panico_activo", False))
        for k in ["wifi_ok", "chiller_ok", "boiler_ok", "luces_ok"]:
            if not latest.get(k, True):
                spec = MODULE_SPECS[k]
                active_alarms.append(spec["name"])

    n_total_alerts = (1 if panico_activo else 0) + len(active_alarms)
    alert_title_color = "#F87171" if n_total_alerts > 0 else "#48B5B8"
    alert_title_ico = "🚨" if n_total_alerts > 0 else "✅"

    st.markdown(
        f'<div style="font-size:0.8rem;font-weight:800;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:{alert_title_color};margin-bottom:10px;">'
        f'{alert_title_ico} Alertas Activas ({n_total_alerts})</div>',
        unsafe_allow_html=True,
    )

    # 1. ALERTA DE PÁNICO (MÁXIMA PRIORIDAD)
    if panico_activo:
        st.markdown(f"""
        <div class="sidebar-panic-alert">
            <div style="font-weight:900; font-size:0.92rem; letter-spacing:0.04em;">
                🚨 BOTÓN DE PÁNICO ACTIVADO
            </div>
            <div style="font-size:0.8rem; margin-top:3px; font-weight:600;">
                Pin 18 · Emergencia en Estación Demo
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.error("**EMERGENCIA: Botón de Pánico Activado**", icon="🚨")

    # 2. ALERTAS DE HARDWARE
    if len(active_alarms) > 0:
        for mod in active_alarms:
            st.markdown(f"""
            <div class="alert-row-danger">
                <div class="ar-name">Demo · {mod}</div>
                <div class="ar-issue">⚠ Falla de hardware · Fuera de servicio</div>
            </div>
            """, unsafe_allow_html=True)
            st.error(f"**Demo · {mod}** fuera de servicio", icon="🔴")

    # 3. ESTADO NORMAL
    if n_total_alerts == 0 and latest is not None:
        st.markdown("""
        <div class="alert-row-ok">
            <div class="ar-name">Demo · Sistemas OK</div>
            <div class="ar-issue">✓ Todos los módulos operativos · Sin emergencias</div>
        </div>
        """, unsafe_allow_html=True)
    elif latest is None:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
            <div style="color: #94A3B8; font-weight: 700; font-size: 0.85rem;">⏳ Esperando datos...</div>
            <div style="color: #64748B; font-size: 0.78rem; margin-top: 2px;">Sin paquetes recibidos aún</div>
        </div>
        """, unsafe_allow_html=True)

    if latest:
        st.markdown(f"""
        <div style="font-size:0.75rem; color:#8B9EC8; margin-top:6px; text-align:right;">
            Último POST: <strong>{latest['timestamp']}</strong>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FRAGMENTO PRINCIPAL DE TELEMETRÍA (Auto-actualizable)
# ─────────────────────────────────────────────────────────────
@st.fragment(run_every="2s")
def render_dashboard_content():
    """Lee directamente de la base de datos de eventos y grafica la estación Demo."""
    latest = database.get_latest_telemetry("Demo")
    history = database.get_telemetry_history("Demo", limit=30)
    is_blank = latest is None

    panico_activo = bool(latest.get("panico_activo", False)) if not is_blank else False

    # Detectar módulos con falla (booleanos en False)
    failing_modules = []
    if not is_blank:
        for k in ["wifi_ok", "chiller_ok", "boiler_ok", "luces_ok"]:
            if not latest.get(k, True):
                failing_modules.append(MODULE_SPECS[k]["name"])

    # ── 1. BANNER DE EMERGENCIA DE ANCHO COMPLETO (BOTÓN DE PÁNICO) ──
    if panico_activo:
        panic_time = latest.get("timestamp", datetime.now().strftime("%H:%M:%S"))
        st.markdown(f"""
        <div class="panic-banner-emergency">
            <div style="font-size: 2.3rem; line-height: 1;">🚨</div>
            <div style="flex: 1;">
                <div class="panic-banner-title">
                    ALERTA DE EMERGENCIA: BOTÓN DE PÁNICO ACTIVADO EN ESTACIÓN DEMO
                </div>
                <div class="panic-banner-sub">
                    Evento registrado a las <strong>{panic_time}</strong> · Valija IoT ESP32 (Pin 18) · Protocolo de seguridad y baliza activados
                </div>
            </div>
            <div style="background: rgba(0,0,0,0.25); border-radius: 8px; padding: 6px 14px; font-weight: 800; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase;">
                EN CURSO
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 2. HEADER DE ESTACIÓN DEMO (BRANDING XENDAR) ─────────
    last_seen_str = latest["timestamp"] if not is_blank else "Esperando primer evento..."
    status_tag = (
        '<span style="background:#FEE2E2;color:#991B1B;border:1px solid #F87171;padding:5px 14px;border-radius:12px;font-weight:800;font-size:0.8rem;">🚨 EMERGENCIA ACTIVA</span>'
        if panico_activo
        else (
            '<span style="background:#FEE2E2;color:#991B1B;border:1px solid #F87171;padding:5px 14px;border-radius:12px;font-weight:800;font-size:0.8rem;">🔴 CON ALERTAS ACTIVAS</span>'
            if len(failing_modules) > 0
            else (
                '<span style="background:#E6F5F6;color:#2B8A91;border:1px solid #B8E4E7;padding:5px 14px;border-radius:12px;font-weight:800;font-size:0.8rem;">🟢 SISTEMA 100% OPERATIVO</span>'
                if not is_blank
                else '<span style="background:#E2E8F0;color:#475569;padding:5px 14px;border-radius:12px;font-weight:800;font-size:0.8rem;">⏳ EN ESPERA</span>'
            )
        )
    )

    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:6px solid #2B8A91; border-radius:14px; padding:18px 24px; margin-bottom:20px; box-shadow:0 2px 10px rgba(30, 51, 77, 0.05);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div>
                <div style="font-size:0.75rem; color:#2B8A91; font-weight:800; letter-spacing:0.12em; text-transform:uppercase;">
                    NODO ACTIVO · HARDWARE TELEMETRY
                </div>
                <div style="font-size:1.85rem; font-weight:900; color:#1E334D; margin-top:2px;">
                    Estación Demo <span style="font-size:0.95rem; font-weight:500; color:#64748B;">(Valija IoT ESP32)</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="margin-bottom:4px;">{status_tag}</div>
                <div style="font-size:0.75rem; color:#94A3B8; font-weight:700; letter-spacing:0.05em;">ÚLTIMO HEARTBEAT (HTTP POST)</div>
                <div style="font-size:1.15rem; color:#1E334D; font-weight:800;">{last_seen_str}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Si la app arranca en blanco (sin telemetría aún)
    if is_blank:
        st.info(
            "⏳ **Esperando primera telemetría del ESP32** en la ruta `/api/telemetria`.\n\n"
            "La base de datos arranca en blanco. El tablero de control Xendar se actualizará en tiempo real "
            "automáticamente al recibir los paquetes HTTP POST desde la Valija IoT.",
            icon="ℹ️"
        )

    # Notificación de fallas de hardware secundarias (si no es pánico)
    if len(failing_modules) > 0 and not panico_activo:
        st.error(
            f"🚨 **ALERTA DE HARDWARE**: Módulos fuera de servicio detectados: **{', '.join(failing_modules)}**. "
            f"Revisión requerida.",
            icon="⚠️"
        )

    # ── 3. MÓDULO DE CONTADORES DE SUMINISTRO (KPIs) ─────────
    st.markdown('<p class="sec-label">💧 Suministro y Consumo de Agua (0.25 L por despacho)</p>', unsafe_allow_html=True)

    despachos_frio = latest["despachos_frio"] if not is_blank else 0
    despachos_calor = latest["despachos_calor"] if not is_blank else 0

    litros_frio = despachos_frio * 0.25
    litros_calor = despachos_calor * 0.25
    total_litros = litros_frio + litros_calor
    total_despachos = despachos_frio + despachos_calor

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            render_kpi_card(
                title="Agua Caliente Suministrada",
                litros=litros_calor,
                despachos=despachos_calor,
                accent_color="#E05638",
                icon="🔥",
            ),
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            render_kpi_card(
                title="Agua Fría Suministrada",
                litros=litros_frio,
                despachos=despachos_frio,
                accent_color="#2B8A91",
                icon="🧊",
            ),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            render_kpi_card(
                title="Total Agua Suministrada",
                litros=total_litros,
                despachos=total_despachos,
                accent_color="#1E334D",
                icon="🚰",
            ),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── 4. GRILLA DE ESTADO DE COMPONENTES (5 MÓDULOS) ────────
    st.markdown('<p class="sec-label">🩺 Estado Operativo de Hardware & Sistema de Emergencia</p>', unsafe_allow_html=True)

    c_panic, c_wifi, c_chiller, c_boiler, c_luces = st.columns(5)

    with c_panic:
        st.markdown(render_panic_module_card(panico_activo, is_waiting=is_blank), unsafe_allow_html=True)

    with c_wifi:
        is_ok = latest["wifi_ok"] if not is_blank else True
        st.markdown(render_hardware_card("wifi_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    with c_chiller:
        is_ok = latest["chiller_ok"] if not is_blank else True
        st.markdown(render_hardware_card("chiller_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    with c_boiler:
        is_ok = latest["boiler_ok"] if not is_blank else True
        st.markdown(render_hardware_card("boiler_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    with c_luces:
        is_ok = latest["luces_ok"] if not is_blank else True
        st.markdown(render_hardware_card("luces_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── 5. HISTORIAL DE EVENTOS EN TIEMPO REAL ───────────────
    st.markdown('<p class="sec-label">📋 Registro de Eventos Recibidos en Tiempo Real</p>', unsafe_allow_html=True)

    if history and len(history) > 0:
        df = pd.DataFrame(history)

        # Formateo de columnas para visualización ejecutiva
        df_display = pd.DataFrame()
        df_display["ID"] = df["id"]
        df_display["Fecha / Hora"] = df["timestamp"]
        df_display["🚨 Pánico"] = df["panico_activo"].map(lambda x: "🚨 ACTIVADO" if x else "Normal")
        df_display["Vol. Calor (L)"] = (df["despachos_calor"] * 0.25).map("{:.2f} L".format)
        df_display["Vol. Frío (L)"] = (df["despachos_frio"] * 0.25).map("{:.2f} L".format)
        df_display["Boiler"] = df["boiler_ok"].map(lambda x: "OK" if x else "FALLA")
        df_display["Chiller"] = df["chiller_ok"].map(lambda x: "OK" if x else "FALLA")
        df_display["WiFi"] = df["wifi_ok"].map(lambda x: "OK" if x else "FALLA")
        df_display["Luces"] = df["luces_ok"].map(lambda x: "OK" if x else "FALLA")

        st.dataframe(
            df_display.sort_values("ID", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("No hay registros aún en la base de datos. En cuanto el ESP32 envíe datos, se listarán automáticamente.")


# ─────────────────────────────────────────────────────────────
# MAIN ENTRYPOINT
# ─────────────────────────────────────────────────────────────
def main():
    # ── SIDEBAR (IDENTIDAD XENDAR) ───────────────────────────
    with st.sidebar:
        # Header Corporativo Xendar
        st.markdown("""
        <div style='text-align:center; padding:14px 0 16px;'>
            <div style='display:inline-flex; align-items:center; justify-content:center; width:46px; height:46px; background:#2B8A91; border-radius:12px; margin-bottom:10px; box-shadow:0 4px 14px rgba(0,0,0,0.3);'>
                <span style='font-size:1.6rem; color:#FFFFFF; font-weight:900;'>X</span>
            </div>
            <div style='font-size:1.45rem; font-weight:900; color:#FFFFFF; letter-spacing:0.06em; line-height:1.1;'>
                XENDAR
            </div>
            <div style='font-size:0.75rem; font-weight:700; color:#48B5B8; letter-spacing:0.12em; text-transform:uppercase; margin-top:4px;'>
                Smart & Sustentable
            </div>
            <div style='font-size:0.7rem; color:#94A3B8; margin-top:2px;'>
                Tablero de Control Ejecutivo
            </div>
        </div>
        <div style='border-top:1px solid rgba(255,255,255,0.1); margin:0 0 14px;'></div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.75rem;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;color:#8B9EC8;margin-bottom:6px;">📡 Estación Activa</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(43, 138, 145, 0.18); border: 1px solid rgba(72, 181, 184, 0.4); border-radius: 10px; padding: 10px 14px; margin-bottom: 14px;">
            <div style="font-size: 1.05rem; font-weight: 800; color: #FFFFFF;">Estación Demo</div>
            <div style="font-size: 0.76rem; color: #A5F3FC;">Valija IoT ESP32 · Pin 18 Activo</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.1);margin:12px 0;"></div>', unsafe_allow_html=True)

        # ── PANEL DE ALERTAS ACTIVAS EN SIDEBAR (Auto-refresh en tiempo real) ───
        render_sidebar_alerts()

        st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.1);margin:16px 0 12px;"></div>', unsafe_allow_html=True)

        # ── SECCIÓN DE PRUEBAS / SIMULADOR INTEGRADO ESP32 ─────
        with st.expander("🧪 Simulador de Hardware (ESP32)", expanded=False):
            st.caption("Pruebas interactivas de eventos para validar el tablero sin hardware físico.")

            # Botón de Pánico
            if st.button("🚨 Simular Botón de Pánico", use_container_width=True):
                database.save_telemetry({
                    "wifi_ok": True,
                    "chiller_ok": True,
                    "boiler_ok": False,
                    "luces_ok": True,
                    "despachos_frio": 12,
                    "despachos_calor": 5,
                    "panico_activo": True
                }, station="Demo")
                st.rerun()

            # Normalizar Pánico
            if st.button("🟢 Normalizar Pánico (Inactivo)", use_container_width=True):
                database.save_telemetry({
                    "wifi_ok": True,
                    "chiller_ok": True,
                    "boiler_ok": False,
                    "luces_ok": True,
                    "despachos_frio": 12,
                    "despachos_calor": 5,
                    "panico_activo": False
                }, station="Demo")
                st.rerun()

            # Simular Falla en Boiler
            if st.button("⚠️ Simular Falla (Boiler OFF)", use_container_width=True):
                database.save_telemetry({
                    "wifi_ok": True,
                    "chiller_ok": True,
                    "boiler_ok": False,
                    "luces_ok": True,
                    "despachos_frio": 12,
                    "despachos_calor": 5,
                    "panico_activo": False
                }, station="Demo")
                st.rerun()

            # Estado 100% OK
            if st.button("✅ Simular 100% OK (Todos ON)", use_container_width=True):
                database.save_telemetry({
                    "wifi_ok": True,
                    "chiller_ok": True,
                    "boiler_ok": True,
                    "luces_ok": True,
                    "despachos_frio": 20,
                    "despachos_calor": 15,
                    "panico_activo": False
                }, station="Demo")
                st.rerun()

            # Falla múltiple
            if st.button("Simular Falla Múltiple (Chiller + Boiler)", use_container_width=True):
                database.save_telemetry({
                    "wifi_ok": True,
                    "chiller_ok": False,
                    "boiler_ok": False,
                    "luces_ok": True,
                    "despachos_frio": 24,
                    "despachos_calor": 8,
                    "panico_activo": False
                }, station="Demo")
                st.rerun()

            # Reset base de datos
            if st.button("Limpiar Datos (Reset en blanco)", use_container_width=True):
                database.reset_telemetry("Demo")
                st.rerun()

        # Botón de refresco manual
        if st.button("🔄 Refrescar ahora", use_container_width=True):
            st.rerun()

        st.markdown(f"""
        <div style='border-top:1px solid rgba(255,255,255,0.1);margin-top:16px;padding-top:10px;
                    font-size:0.74rem;color:#8B9EC8;text-align:center;'>
            Endpoint: <code>/api/telemetria</code><br>
            Hora local: {datetime.now().strftime("%H:%M:%S")}
        </div>
        """, unsafe_allow_html=True)

    # ── HEADER PRINCIPAL DEL DASHBOARD ───────────────────────
    st.markdown("""
    <div style='padding:2px 0 16px;'>
        <h1 class='brand-title'>
            Xendar <span style="font-weight:400; color:#2B8A91;">| Smart & Sustentable</span>
        </h1>
        <div class='brand-subtitle'>Tablero de Control Ejecutivo · Telemetría IoT</div>
        <p class='brand-desc'>
            Monitoreo en tiempo real de dispensers de hidratación, salud de hardware y sistema de emergencia (Pin 18)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── CONTENIDO DINÁMICO DE TELEMETRÍA ─────────────────────
    render_dashboard_content()

    # ── FOOTER CORPORATIVO ────────────────────────────────────
    st.markdown(f"""
    <div style="margin-top:36px;padding:16px 0;border-top:1px solid #E2E8F0;
                display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;
                font-size:0.82rem;color:#64748B;">
        <span>⚡ <strong style="color:#1E334D;">Xendar</strong> · Soluciones Smart & Sustentables (xendar.com.ar)</span>
        <span>Telemetría ESP32 · Event-Driven Architecture</span>
        <span>Producción Railway</span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
