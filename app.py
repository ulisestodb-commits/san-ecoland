"""
╔══════════════════════════════════════════════════════════════╗
║          SAN ECOLAND — Smart City Telemetry Dashboard        ║
║          Estación Demo · Valija IoT con ESP32 (Event-Driven) ║
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
    page_title="San Ecoland · Estación Demo ESP32",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL STYLING — Paleta San Ecoland: Blanco/Gris + Navy + Teal
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Escala base y variables ── */
    html { font-size: 16px !important; }
    :root {
        --bg:          #f0f4f9;
        --bg-card:     #ffffff;
        --sidebar-bg:  #0d1f52;
        --navy:        #0d1f52;
        --teal:        #1ab8cc;
        --teal-light:  #e6f8fb;
        --success:     #059669;
        --success-bg:  #d1fae5;
        --danger:      #dc2626;
        --danger-bg:   #fee2e2;
        --danger-border: #f87171;
        --warn:        #b45309;
        --warn-bg:     #fef3c7;
        --text:        #1e293b;
        --muted:       #64748b;
        --border:      #dde3ec;
        --shadow:      0 2px 8px rgba(13,31,82,0.06);
    }

    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    .stApp { background-color: var(--bg) !important; color: var(--text) !important; }

    /* ── Encabezados ── */
    .main-title {
        font-size: 1.95rem;
        font-weight: 800;
        margin: 0;
        color: var(--navy);
        line-height: 1.2;
    }
    .main-subtitle {
        font-size: 1.05rem;
        font-weight: 500;
        color: #64748b;
    }
    .main-desc {
        margin: 4px 0 0;
        color: var(--muted);
        font-size: 0.92rem;
    }
    .sec-label {
        font-size: 0.86rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 0 0 12px 2px;
    }

    /* ── Sidebar ── */
    div[data-testid="stSidebarContent"] {
        background: var(--sidebar-bg) !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #c8d4f0 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #ffffff !important; }

    /* Alertas en Sidebar */
    .alert-row-danger {
        background: rgba(239, 68, 68, 0.22) !important;
        border: 1px solid rgba(239, 68, 68, 0.55) !important;
        border-left: 5px solid #ef4444 !important;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 8px;
    }
    .alert-row-danger .ar-name  { color: #ffffff !important; font-weight: 800; font-size: 0.95rem; margin-bottom: 2px; }
    .alert-row-danger .ar-issue { color: #fca5a5 !important; font-size: 0.84rem; font-weight: 600; }

    .alert-row-ok {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        border-left: 5px solid #10b981 !important;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 8px;
    }
    .alert-row-ok .ar-name  { color: #ffffff !important; font-weight: 800; font-size: 0.95rem; }
    .alert-row-ok .ar-issue { color: #6ee7b7 !important; font-size: 0.84rem; font-weight: 600; }

    /* ── Tarjetas Métricas (KPIs) ── */
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
    }
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 2.35rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.88rem;
        font-weight: 600;
        color: #64748b;
        margin-top: 6px;
    }

    /* ── Tarjetas de Componentes de Hardware ── */
    .hw-card-ok {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-top: 4px solid var(--success);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: var(--shadow);
        height: 100%;
        transition: transform 0.15s ease;
    }
    .hw-card-fail {
        background: #fff5f5 !important;
        border: 2px solid #ef4444 !important;
        border-top: 5px solid #dc2626 !important;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(220, 38, 38, 0.22) !important;
        height: 100%;
        animation: pulse-border 2s infinite ease-in-out;
    }
    @keyframes pulse-border {
        0%, 100% { border-color: #ef4444; }
        50% { border-color: #b91c1c; }
    }

    .hw-title {
        font-size: 0.92rem;
        font-weight: 800;
        color: var(--navy);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }
    .hw-title-fail {
        font-size: 0.92rem;
        font-weight: 800;
        color: #b91c1c !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }

    /* ── Badges ── */
    .badge-ok {
        background: var(--success-bg);
        color: #065f46;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-fail {
        background: #fee2e2;
        color: #991b1b;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        border: 1px solid #f87171;
    }
    .badge-waiting {
        background: #e2e8f0;
        color: #475569;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .divider { border-top: 1px solid var(--border); margin: 24px 0; }
    
    #MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# COMPONENT DEFINITION & HARDWARE MAPPING
# ─────────────────────────────────────────────────────────────
MODULE_SPECS = {
    "wifi_ok": {
        "name": "Módulo WiFi",
        "icon": "📶",
        "desc_ok": "Conectividad normal · Señal estable",
        "desc_fail": "Módulo WiFi fuera de servicio · Sin telemetría remota",
    },
    "chiller_ok": {
        "name": "Chiller (Agua Fría)",
        "icon": "🧊",
        "desc_ok": "Sistema de refrigeración operativo · Temperatura óptima",
        "desc_fail": "Módulo Chiller fuera de servicio · Suministro de agua fría suspendido",
    },
    "boiler_ok": {
        "name": "Boiler (Agua Caliente)",
        "icon": "🔥",
        "desc_ok": "Sistema térmico operativo · Caldera lista",
        "desc_fail": "Módulo Boiler fuera de servicio · Suministro de agua caliente suspendido",
    },
    "luces_ok": {
        "name": "Sistema de Luces",
        "icon": "💡",
        "desc_ok": "Iluminación operativa · Consumo nominal",
        "desc_fail": "Módulo de Iluminación fuera de servicio · Falla detectada",
    },
}


# ─────────────────────────────────────────────────────────────
# VIEW RENDERERS (HTML NATIVO)
# ─────────────────────────────────────────────────────────────
def render_kpi_card(title: str, litros: float, despachos: int, color: str, icon: str) -> str:
    """Genera la tarjeta visual para cada KPI de suministro en Litros."""
    return f"""
    <div class="kpi-card" style="border-left: 5px solid {color};">
        <div>
            <div class="kpi-title">{icon} {title}</div>
            <div class="kpi-value" style="color: {color};">{litros:.2f} <span style="font-size:1.3rem;font-weight:600;color:#64748b;">L</span></div>
        </div>
        <div class="kpi-sub">
            💧 <strong>{despachos}</strong> despachos realizados (0.25 L c/u)
        </div>
    </div>
    """


def render_hardware_card(key: str, is_ok: bool, is_waiting: bool = False) -> str:
    """
    Renderiza un componente de hardware.
    Si is_ok es False, resalta en rojo indicando el módulo exacto fuera de servicio.
    """
    spec = MODULE_SPECS[key]
    name = spec["name"]
    icon = spec["icon"]

    if is_waiting:
        return f"""
        <div class="kpi-card" style="border-top: 4px solid #94a3b8;">
            <div class="hw-title">{icon} {name}</div>
            <div style="margin: 10px 0;"><span class="badge-waiting">⏳ EN ESPERA</span></div>
            <div style="font-size:0.88rem; color:#64748b;">Esperando primer paquete de telemetría del ESP32</div>
        </div>
        """

    if is_ok:
        return f"""
        <div class="hw-card-ok">
            <div class="hw-title">{icon} {name}</div>
            <div style="margin: 10px 0;">
                <span class="badge-ok">● ONLINE / OPERATIVO</span>
            </div>
            <div style="font-size:0.86rem; color:#059669; font-weight:600;">
                ✓ {spec['desc_ok']}
            </div>
        </div>
        """
    else:
        return f"""
        <div class="hw-card-fail">
            <div class="hw-title-fail">🚨 {icon} {name}</div>
            <div style="margin: 10px 0;">
                <span class="badge-fail">✖ FUERA DE SERVICIO</span>
            </div>
            <div style="font-size:0.86rem; color:#dc2626; font-weight:700;">
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
    if latest:
        for k in ["wifi_ok", "chiller_ok", "boiler_ok", "luces_ok"]:
            if not latest.get(k, True):
                spec = MODULE_SPECS[k]
                active_alarms.append(spec["name"])

    n_alerts = len(active_alarms)
    alert_title_color = "#f87171" if n_alerts > 0 else "#6ee7b7"
    alert_title_ico = "🚨" if n_alerts > 0 else "✅"

    st.markdown(
        f'<div style="font-size:0.82rem;font-weight:800;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:{alert_title_color};margin-bottom:10px;">'
        f'{alert_title_ico} Alertas Activas ({n_alerts})</div>',
        unsafe_allow_html=True,
    )

    if n_alerts > 0:
        for mod in active_alarms:
            st.markdown(f"""
            <div style="background: #dc2626; border: 1px solid #f87171; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; box-shadow: 0 4px 10px rgba(220,38,38,0.35);">
                <div style="color: #ffffff; font-weight: 800; font-size: 0.95rem;">🚨 Demo · {mod}</div>
                <div style="color: #fee2e2; font-size: 0.82rem; font-weight: 600; margin-top: 4px;">⚠ Falla de hardware · Fuera de servicio</div>
            </div>
            """, unsafe_allow_html=True)
            st.error(f"**Demo · {mod}** fuera de servicio", icon="🔴")
    elif latest is not None:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.18); border: 1px solid #10b981; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
            <div style="color: #ffffff; font-weight: 800; font-size: 0.95rem;">✅ Demo · Sistemas OK</div>
            <div style="color: #a7f3d0; font-size: 0.82rem; font-weight: 600; margin-top: 3px;">✓ Todos los módulos operativos</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
            <div style="color: #94a3b8; font-weight: 700; font-size: 0.9rem;">⏳ Esperando datos...</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-top: 2px;">Sin paquetes recibidos aún</div>
        </div>
        """, unsafe_allow_html=True)

    if latest:
        st.markdown(f"""
        <div style="font-size:0.75rem; color:#8b9ec8; margin-top:6px; text-align:right;">
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

    # Detectar módulos con falla (booleanos en False)
    failing_modules = []
    if not is_blank:
        for k in ["wifi_ok", "chiller_ok", "boiler_ok", "luces_ok"]:
            if not latest.get(k, True):
                failing_modules.append(MODULE_SPECS[k]["name"])

    # ── HEADER DE ESTACIÓN DEMO ──────────────────────────────
    last_seen_str = latest["timestamp"] if not is_blank else "Esperando primer evento..."
    status_tag = (
        '<span style="background:#fee2e2;color:#991b1b;padding:4px 12px;border-radius:12px;font-weight:700;font-size:0.82rem;">🔴 CON ALERTAS ACTIVAS</span>'
        if len(failing_modules) > 0
        else (
            '<span style="background:#d1fae5;color:#065f46;padding:4px 12px;border-radius:12px;font-weight:700;font-size:0.82rem;">🟢 SISTEMA 100% OPERATIVO</span>'
            if not is_blank
            else '<span style="background:#e2e8f0;color:#475569;padding:4px 12px;border-radius:12px;font-weight:700;font-size:0.82rem;">⏳ EN ESPERA</span>'
        )
    )

    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #dde3ec; border-left:6px solid #1ab8cc; border-radius:14px; padding:18px 24px; margin-bottom:20px; box-shadow:0 2px 8px rgba(13,31,82,0.06);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div>
                <div style="font-size:0.8rem; color:#94a3b8; font-weight:800; letter-spacing:0.1em; text-transform:uppercase;">
                    NODO ACTIVO · HARDWARE TELEMETRY
                </div>
                <div style="font-size:1.85rem; font-weight:800; color:#0d1f52; margin-top:2px;">
                    Estación Demo <span style="font-size:1rem; font-weight:500; color:#64748b;">(Valija IoT · ESP32)</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="margin-bottom:4px;">{status_tag}</div>
                <div style="font-size:0.8rem; color:#94a3b8; font-weight:600;">ÚLTIMO HEARTBEAT (HTTP POST)</div>
                <div style="font-size:1.15rem; color:#0d1f52; font-weight:700;">{last_seen_str}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Si la app arranca en blanco (sin telemetría aún)
    if is_blank:
        st.info(
            "⏳ **Esperando primera telemetría del ESP32** en la ruta `/api/telemetria`.\n\n"
            "La base de datos arranca en blanco. El dashboard se actualizará automáticamente en tiempo real "
            "en cuanto la Valija IoT envíe su primer paquete HTTP POST.",
            icon="ℹ️"
        )

    # ── NOTIFICACIÓN DE ALERTA EVENT-DRIVEN ────────────────────
    if len(failing_modules) > 0:
        st.error(
            f"🚨 **ALERTA CRÍTICA DE FALLA DE HARDWARE**: Se ha detectado que los siguientes módulos están "
            f"**fuera de servicio**: **{', '.join(failing_modules)}**. "
            f"El sistema ha registrado el evento de falla en tiempo real.",
            icon="⚠️"
        )
    elif not is_blank:
        st.success("✅ **Todos los módulos de hardware están funcionando correctamente.** Sin fallas activas.", icon="✅")

    # ── MÓDULO 1: CONTADORES (KPIs de Suministro) ─────────────
    st.markdown('<p class="sec-label">💧 Módulo de Contadores de Suministro (0.25 L por despacho)</p>', unsafe_allow_html=True)

    despachos_frio = latest["despachos_frio"] if not is_blank else 0
    despachos_calor = latest["despachos_calor"] if not is_blank else 0

    # Cada despacho corresponde a 0.25 L
    litros_frio = despachos_frio * 0.25
    litros_calor = despachos_calor * 0.25
    total_litros = litros_frio + litros_calor
    total_despachos = despachos_frio + despachos_calor

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            render_kpi_card(
                title="agua caliente suministrada",
                litros=litros_calor,
                despachos=despachos_calor,
                color="#e05638",
                icon="🔥",
            ),
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            render_kpi_card(
                title="agua fría suministrada",
                litros=litros_frio,
                despachos=despachos_frio,
                color="#1ab8cc",
                icon="🧊",
            ),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            render_kpi_card(
                title="Total agua suministrada",
                litros=total_litros,
                despachos=total_despachos,
                color="#0d1f52",
                icon="🚰",
            ),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── MÓDULO 2: ALARMAS DE HARDWARE (Event-Driven) ───────────
    st.markdown('<p class="sec-label">🩺 Módulo de Alarmas & Estado de Componentes de Hardware</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)

    with h1:
        is_ok = latest["wifi_ok"] if not is_blank else True
        st.markdown(render_hardware_card("wifi_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    with h2:
        is_ok = latest["chiller_ok"] if not is_blank else True
        st.markdown(render_hardware_card("chiller_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    with h3:
        is_ok = latest["boiler_ok"] if not is_blank else True
        st.markdown(render_hardware_card("boiler_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    with h4:
        is_ok = latest["luces_ok"] if not is_blank else True
        st.markdown(render_hardware_card("luces_ok", is_ok, is_waiting=is_blank), unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── HISTORIAL DE EVENTOS Y TELEMETRÍA ─────────────────────
    st.markdown('<p class="sec-label">📋 Registro de Eventos Recibidos en Tiempo Real</p>', unsafe_allow_html=True)

    if history and len(history) > 0:
        df = pd.DataFrame(history)
        df_display = df.rename(columns={
            "id": "ID",
            "timestamp": "Fecha / Hora",
            "wifi_ok": "WiFi OK",
            "chiller_ok": "Chiller OK",
            "boiler_ok": "Boiler OK",
            "luces_ok": "Luces OK",
            "despachos_frio": "Desp. Frío (und)",
            "despachos_calor": "Desp. Calor (und)",
        })
        # Agregar columnas de litros calculados
        df_display["Vol. Frío (L)"] = (df_display["Desp. Frío (und)"] * 0.25).map("{:.2f} L".format)
        df_display["Vol. Calor (L)"] = (df_display["Desp. Calor (und)"] * 0.25).map("{:.2f} L".format)

        cols_order = [
            "ID", "Fecha / Hora", "Vol. Calor (L)", "Vol. Frío (L)",
            "Boiler OK", "Chiller OK", "WiFi OK", "Luces OK"
        ]
        st.dataframe(
            df_display[cols_order].sort_values("ID", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("No hay registros en la base de datos. En cuanto el ESP32 envíe datos, aparecerán aquí.")


# ─────────────────────────────────────────────────────────────
# MAIN ENTRYPOINT
# ─────────────────────────────────────────────────────────────
def main():
    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:14px 0 18px;'>
            <div style='font-size:2.2rem;'>🌿</div>
            <div style='font-size:1.25rem; font-weight:800; color:#1ab8cc; letter-spacing:0.05em;'>SAN ECOLAND</div>
            <div style='font-size:0.75rem; color:#8b9ec8; letter-spacing:0.1em; text-transform:uppercase; margin-top:2px;'>
                Valija IoT · ESP32 Telemetry
            </div>
        </div>
        <div style='border-top:1px solid rgba(255,255,255,0.1); margin:0 0 16px;'></div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.78rem;font-weight:800;letter-spacing:0.14em;text-transform:uppercase;color:#8b9ec8;margin-bottom:8px;">📡 Estación Activa</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(26, 184, 204, 0.15); border: 1px solid rgba(26, 184, 204, 0.4); border-radius: 8px; padding: 10px 14px; margin-bottom: 16px;">
            <div style="font-size: 1.05rem; font-weight: 800; color: #ffffff;">Demo</div>
            <div style="font-size: 0.78rem; color: #a5f3fc;">ESP32 Event-Driven Hardware</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.1);margin:14px 0;"></div>', unsafe_allow_html=True)

        # ── PANEL DE ALERTAS ACTIVAS EN SIDEBAR (Auto-refresh en tiempo real) ───
        render_sidebar_alerts()

        st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.1);margin:18px 0 14px;"></div>', unsafe_allow_html=True)

        # ── SECCIÓN DE PRUEBAS / SIMULACIÓN ESP32 ──────────────
        with st.expander("🧪 Simulador de Hardware (ESP32)", expanded=False):
            st.caption("Permite inyectar eventos de prueba para validar la UI sin hardware físico.")

            # Payload oficial con falla en Boiler
            if st.button("Simular Falla (Boiler OFF)", use_container_width=True):
                database.save_telemetry({
                    "wifi_ok": True,
                    "chiller_ok": True,
                    "boiler_ok": False,
                    "luces_ok": True,
                    "despachos_frio": 12,
                    "despachos_calor": 5
                }, station="Demo")
                st.rerun()

            # Estado 100% OK
            if st.button("Simular 100% OK (Todos ON)", use_container_width=True):
                database.save_telemetry({
                    "wifi_ok": True,
                    "chiller_ok": True,
                    "boiler_ok": True,
                    "luces_ok": True,
                    "despachos_frio": 20,
                    "despachos_calor": 15
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
                    "despachos_calor": 8
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
        <div style='border-top:1px solid rgba(255,255,255,0.1);margin-top:20px;padding-top:12px;
                    font-size:0.75rem;color:#6b82b0;text-align:center;'>
            Endpoint: <code>/api/telemetria</code><br>
            Reloj local: {datetime.now().strftime("%H:%M:%S")}
        </div>
        """, unsafe_allow_html=True)

    # ── HEADER PRINCIPAL ─────────────────────────────────────
    st.markdown("""
    <div style='padding:2px 0 14px;'>
        <h1 class='main-title'>
            🌿 San Ecoland
            <span class='main-subtitle'> / IoT Hardware Telemetry</span>
        </h1>
        <p class='main-desc'>
            Recepción de eventos en tiempo real desde el ESP32 · Estación Demo
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── CONTENIDO DINÁMICO DE TELEMETRÍA ─────────────────────
    render_dashboard_content()

    # ── FOOTER ────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-top:36px;padding:14px 0;border-top:1px solid #dde3ec;
                display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;
                font-size:0.84rem;color:#94a3b8;">
        <span>🌿 <strong style="color:#64748b;">San Ecoland Smart City</strong> · Valija IoT ESP32 v2.0</span>
        <span>Recepción HTTP POST vía FastAPI / Uvicorn</span>
        <span>Modo Producción · Railway Ready</span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
