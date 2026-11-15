"""
╔══════════════════════════════════════════════════════════════╗
║          SAN ECOLAND — Smart City Telemetry Dashboard        ║
║          IoT Network: 10 Smart Bus Stops + 5 Hydration Sta.  ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  — primera llamada obligatoria
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="San Ecoland · Smart City Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL STYLING  — paleta Xendar: blanco/gris claro + navy + teal
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Escala base: sube el rem de ~14px a 16px para todo el app ── */
    html { font-size: 16px !important; }

    /* ── Paleta base ── */
    :root {
        --bg:          #f0f4f9;
        --bg-card:     #ffffff;
        --sidebar-bg:  #0d1f52;
        --navy:        #0d1f52;
        --teal:        #1ab8cc;
        --teal-light:  #e6f8fb;
        --success:     #059669;
        --success-bg:  #d1fae5;
        --warn:        #b45309;
        --warn-bg:     #fef3c7;
        --danger:      #b91c1c;
        --danger-bg:   #fee2e2;
        --eco-bg:      #dbeafe;
        --eco-fg:      #1e40af;
        --text:        #1e293b;
        --muted:       #64748b;
        --border:      #dde3ec;
        --shadow:      0 1px 6px rgba(13,31,82,0.08);
    }

    /* ── Fondo principal ── */
    .stApp { background-color: var(--bg) !important; color: var(--text) !important; }

    /* ── Ajuste a toda la pantalla (ancho completo sin márgenes excesivos) ── */
    .main .block-container,
    [data-testid="stMainBlockContainer"],
    .block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* ── Sidebar navy — ancho 20% de pantalla, anclada en x=0 (nunca desplazada fuera de pantalla) ── */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        min-width: 20vw !important;
        width:     20vw !important;
        max-width: 20vw !important;
        background: var(--sidebar-bg) !important;
        transform: none !important;
        margin-left: 0 !important;
        left: 0 !important;
        top: 0 !important;
        position: relative !important;
        display: block !important;
        visibility: visible !important;
    }
    div[data-testid="stSidebarContent"] {
        width: 100% !important;
        min-width: 100% !important;
        overflow-x: hidden !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }
    div[data-testid="stSidebarUserContent"] {
        width: 100% !important;
        padding: 0 !important;
    }

    /* Botón para expandir o colapsar sidebar siempre visible */
    button[data-testid="stExpandSidebarButton"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        z-index: 9999999 !important;
        background: #0d1f52 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        cursor: pointer !important;
    }
    button[data-testid="stExpandSidebarButton"] svg,
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* Texto sidebar: todo en blanco con buena visibilidad */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #c8d4f0 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #ffffff !important; }

    /* Selectbox sidebar */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.12) !important;
        border-color: rgba(255,255,255,0.2) !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stSelectbox svg { fill: #c8d4f0 !important; }

    /* Botones de alerta en sidebar — alta visibilidad y contraste */
    [data-testid="stSidebar"] .stButton > button {
        background: #ef4444 !important;
        border: 1px solid #dc2626 !important;
        color: #ffffff !important;
        font-size: 0.84rem !important;
        font-weight: 700 !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        width: 100% !important;
        margin-top: 2px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.25) !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #dc2626 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stButton > button p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* ── Tarjetas métricas ── */
    div[data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: var(--shadow);
    }
    div[data-testid="metric-container"] label {
        color: var(--muted) !important;
        font-size: 0.84rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-size: 2.1rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: var(--muted) !important;
        font-size: 0.88rem !important;
    }

    /* ── Encabezados de sección ── */
    .sec-label {
        font-size: 0.84rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 0 0 12px 2px;
    }

    /* ── Tarjeta genérica ── */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: var(--shadow);
        height: 100%;
    }

    /* ── Badges de estado ── */
    .badge-ok   { background:var(--success-bg); color:#065f46; padding:5px 14px; border-radius:20px;
                  font-size:0.84rem; font-weight:700; display:inline-block; }
    .badge-fail { background:var(--danger-bg);  color:#991b1b; padding:5px 14px; border-radius:20px;
                  font-size:0.84rem; font-weight:700; display:inline-block; }
    .badge-eco  { background:var(--eco-bg);     color:var(--eco-fg); padding:5px 14px; border-radius:20px;
                  font-size:0.84rem; font-weight:700; display:inline-block; }
    .badge-warn { background:var(--warn-bg);    color:#92400e; padding:5px 14px; border-radius:20px;
                  font-size:0.84rem; font-weight:700; display:inline-block; }

    /* ── Fila de alerta en sidebar ── */
    .alert-row {
        background: rgba(239, 68, 68, 0.18) !important;
        border: 1px solid rgba(239, 68, 68, 0.45) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 6px;
    }
    .alert-row .ar-name  { color: #ffffff !important; font-weight: 800; font-size: 0.95rem; margin-bottom: 2px; }
    .alert-row .ar-issue { color: #fca5a5 !important; font-size: 0.84rem; font-weight: 600; }

    /* ── Separador ── */
    .divider { border-top: 1px solid var(--border); margin: 22px 0; }

    /* ── Toggles y radios: texto legible y más grande ── */
    .stToggle label { color: var(--text) !important; font-weight: 600; font-size: 0.95rem !important; }
    .stRadio  label { color: var(--muted) !important; font-size: 0.88rem !important; }
    .stRadio > div > label { color: var(--text) !important; }
    /* Texto de st.markdown en actuadores */
    .stMarkdown p  { font-size: 1rem; }

    /* ── Caption / texto de ayuda ── */
    .stCaptionContainer p { color: var(--muted) !important; font-size: 0.88rem !important; }

    /* ── Ocultar chrome de Streamlit sin bloquear el botón de expandir la barra lateral ── */
    #MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        display: none !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
        pointer-events: none !important;
    }
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] [data-testid="stToolbar"] {
        pointer-events: auto !important;
    }

    /* ── Plotly fondo transparente ── */
    .js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPERS — etiquetas mensuales (últimos 12 meses)
# ─────────────────────────────────────────────────────────────
def month_label(months_back: int) -> str:
    """Devuelve el label 'Nov 2026' para N meses atrás."""
    now = datetime.now()
    m = now.month - months_back
    y = now.year
    while m <= 0:
        m += 12
        y -= 1
    return datetime(y, m, 1).strftime("%b %Y")

MONTH_LABELS = [month_label(i) for i in range(11, -1, -1)]


# ─────────────────────────────────────────────────────────────
# MOCK DATA — generación realista, seed fija para demos
# ─────────────────────────────────────────────────────────────
@st.cache_data
def generate_mock_data() -> dict:
    rng = np.random.default_rng(seed=42)

    bus_stops = [f"Smart Bus Stop #{i:02d}" for i in range(1, 11)]
    hydration  = [f"Hydration Station #{i:02d}" for i in range(1, 6)]

    stations = {}
    for i, name in enumerate(bus_stops + hydration):
        is_hydration = "Hydration" in name

        # kWh mensuales — 12 meses con tendencia ligeramente creciente
        base = rng.uniform(280, 520)
        monthly = rng.normal(loc=base / 12 * 30, scale=base * 0.07, size=12)
        monthly = np.clip(monthly, 60, None).round(1)
        # Mes actual = último elemento
        total_kwh  = float(round(monthly[-1], 1))
        solar_pct  = rng.uniform(0.30, 0.78)
        solar_kwh  = round(total_kwh * solar_pct, 1)
        grid_kwh   = round(total_kwh * (1 - solar_pct), 1)

        # Estado de salud — exactamente 3 estaciones con problemas para la demo (BS#03, BS#06, HS#03)
        wifi_ok    = (i != 2)               # Smart Bus Stop #03 → WiFi offline
        chiller_ok = (i != 5)               # Smart Bus Stop #06 → Chiller fault
        heater_ok  = (i != 12)              # Hydration Station #03 → Heater fault
        led_ok     = (i != 5)               # Smart Bus Stop #06 → LED fault
        led_mode   = "FALLA" if not led_ok else ("ECO" if i in [1, 7, 9] else "NORMAL")

        # Estado inicial de actuadores
        valve_on   = i not in [1, 9]
        screen_on  = i not in [4, 8]

        stations[name] = {
            "type":           "hydration" if is_hydration else "bus_stop",
            "total_kwh":      total_kwh,
            "solar_kwh":      solar_kwh,
            "grid_kwh":       grid_kwh,
            "monthly_kwh":    monthly.tolist(),
            "co2_reduced":    round(total_kwh * 0.35, 2),
            "wifi_online":    wifi_ok,
            "chiller_online": chiller_ok,
            "heater_online":  heater_ok,
            "led_online":     led_ok,
            "led_mode":       led_mode,
            "valve_on":       valve_on,
            "screen_on":      screen_on,
            "last_seen":      (datetime.now() - timedelta(minutes=int(rng.integers(1, 30)))).strftime("%H:%M:%S"),
        }
    return stations


# ─────────────────────────────────────────────────────────────
# SESSION STATE — inicializa actuadores por estación
# ─────────────────────────────────────────────────────────────
def init_session(d: dict, n: str):
    """Preserva el estado de cada toggle entre re-renders."""
    defaults = {
        f"{n}_valve":          d["valve_on"],
        f"{n}_screen":         d["screen_on"],
        f"{n}_screen_mode":    "Idle (logo fijo)",
        f"{n}_chiller":        True,
        f"{n}_chiller_mode":   "Idle (standby)",
        f"{n}_heater":         True,
        f"{n}_heater_mode":    "Idle (standby)",
        f"{n}_wifi_act":       True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# BADGE HELPERS
# ─────────────────────────────────────────────────────────────
def badge(ok: bool, ok_txt="ONLINE", fail_txt="OFFLINE", warn_mode: str = None) -> str:
    if not ok:
        return f'<span class="badge-fail">✖ {fail_txt}</span>'
    if warn_mode == "ECO":
        return f'<span class="badge-eco">◆ ECO</span>'
    return f'<span class="badge-ok">● {ok_txt}</span>'


# ─────────────────────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────────────────────
def monthly_bar_chart(monthly_kwh: list) -> go.Figure:
    """Barras de los 12 meses — teal si ≥ promedio, gris claro si abajo, navy para el mes actual."""
    avg = float(np.mean(monthly_kwh))
    colors = []
    for idx, v in enumerate(monthly_kwh):
        if idx == 11:
            colors.append("#0d1f52")
        elif v >= avg:
            colors.append("#1ab8cc")
        else:
            colors.append("#cbd5e1")

    fig = go.Figure(go.Bar(
        x=MONTH_LABELS,
        y=monthly_kwh,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)"), cornerradius=4),
        hovertemplate="<b>%{x}</b><br><b>%{y:.1f} kWh</b><extra></extra>",
    ))
    fig.add_hline(
        y=avg, line_dash="dash", line_color="#f59e0b", line_width=1.5,
        annotation_text=f"Prom. {avg:.0f} kWh",
        annotation_font=dict(color="#b45309", size=11),
        annotation_position="top right",
    )
    fig.update_layout(
        xaxis=dict(
            tickangle=-30,
            tickfont=dict(color="#64748b", size=10),
            showgrid=False,
            linecolor="#dde3ec",
        ),
        yaxis=dict(
            tickfont=dict(color="#64748b", size=10),
            gridcolor="#f1f5f9",
            linecolor="#dde3ec",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=12, b=50, l=0, r=0),
        height=240,
        bargap=0.28,
    )
    return fig


def donut_chart(solar_kwh: float, grid_kwh: float) -> go.Figure:
    """Donut Solar vs Grid — colores de alta visibilidad sobre fondo blanco."""
    fig = go.Figure(go.Pie(
        labels=["Solar", "Grid (EDEN)"],
        values=[solar_kwh, grid_kwh],
        hole=0.60,
        marker=dict(
            colors=["#1ab8cc", "#0d1f52"],
            line=dict(color="#f0f4f9", width=3),
        ),
        textinfo="label+percent",
        textfont=dict(color="#1e293b", size=12, family="Arial"),
        hovertemplate="<b>%{label}</b><br>%{value:.1f} kWh — %{percent}<extra></extra>",
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=240,
        annotations=[dict(
            text=f"<b>{solar_kwh + grid_kwh:.0f}</b><br>kWh",
            x=0.5, y=0.5,
            font=dict(size=17, color="#0d1f52", family="Arial"),
            showarrow=False,
        )],
    )
    return fig


# ─────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────
def main():
    stations     = generate_mock_data()
    station_list = list(stations.keys())

    # Estaciones con al menos un sistema en fallo
    failing = {
        nm: d for nm, d in stations.items()
        if not d["wifi_online"] or not d["chiller_online"]
        or not d["heater_online"] or not d["led_online"]
    }

    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        # Branding
        st.markdown("""
        <div style='text-align:center; padding:18px 0 22px;'>
            <div style='font-size:2.4rem;'>🌿</div>
            <div style='font-size:1.3rem; font-weight:800; color:#1ab8cc; letter-spacing:0.05em;'>SAN ECOLAND</div>
            <div style='font-size:0.8rem; color:#8b9ec8; letter-spacing:0.1em; text-transform:uppercase; margin-top:4px;'>Smart City · IoT Dashboard</div>
        </div>
        <div style='border-top:1px solid rgba(255,255,255,0.1); margin:0 0 18px;'></div>
        """, unsafe_allow_html=True)

        # Selector de estación — navigate_to permite saltar desde las alertas
        st.markdown('<div style="font-size:0.8rem;font-weight:800;letter-spacing:0.14em;text-transform:uppercase;color:#8b9ec8;margin-bottom:10px;">📡 Seleccionar Nodo</div>', unsafe_allow_html=True)

        # Pre-seleccionar si se navegó desde una alerta
        if "navigate_to" in st.session_state:
            st.session_state["_station_sel"] = st.session_state.pop("navigate_to")

        if "_station_sel" not in st.session_state or st.session_state["_station_sel"] not in station_list:
            st.session_state["_station_sel"] = station_list[0]

        selected_station = st.selectbox(
            "Nodo",
            station_list,
            label_visibility="collapsed",
            key="_station_sel",
        )

        st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.1);margin:14px 0;"></div>', unsafe_allow_html=True)

        # ── Panel de Alertas Activas ──
        n_alerts = len(failing)
        if n_alerts == 0:
            alert_title_color = "#6ee7b7"
            alert_title_ico   = "✅"
        else:
            alert_title_color = "#fca5a5"
            alert_title_ico   = "🚨"

        st.markdown(
            f'<div style="font-size:0.8rem;font-weight:800;letter-spacing:0.12em;'
            f'text-transform:uppercase;color:{alert_title_color};margin-bottom:12px;">'
            f'{alert_title_ico} Alertas Activas ({n_alerts})</div>',
            unsafe_allow_html=True,
        )

        if n_alerts == 0:
            st.markdown(
                '<div style="font-size:0.9rem;color:#6ee7b7;padding:10px 12px;'
                'background:rgba(16,185,129,0.12);border-radius:6px;">Red sin alertas</div>',
                unsafe_allow_html=True,
            )
        else:
            # Mostrar las 3 alertas activas
            for fname, fdata in list(failing.items())[:3]:
                issues = []
                if not fdata["wifi_online"]:    issues.append("WiFi")
                if not fdata["chiller_online"]: issues.append("Chiller")
                if not fdata["heater_online"]:  issues.append("Heater")
                if not fdata["led_online"]:     issues.append("LED")
                short = fname.replace("Smart Bus Stop", "BS").replace("Hydration Station", "HS")

                st.markdown(f"""
                <div class="alert-row">
                    <div class="ar-name">{short}</div>
                    <div class="ar-issue">⚠ {" · ".join(issues)}</div>
                </div>
                """, unsafe_allow_html=True)

                # Botón de navegación directa
                if st.button(f"→ Ir a {short}", key=f"nav_{fname}"):
                    st.session_state["navigate_to"] = fname
                    st.rerun()

        # Footer
        st.markdown(f"""
        <div style='border-top:1px solid rgba(255,255,255,0.1);margin-top:22px;padding-top:14px;
                    font-size:0.78rem;color:#4a5f8a;text-align:center;'>
            Refresh: {datetime.now().strftime("%H:%M:%S")}<br>15 nodos activos
        </div>
        """, unsafe_allow_html=True)

    # ── HEADER PRINCIPAL ─────────────────────────────────────
    st.markdown("""
    <div style='padding:4px 0 22px;'>
        <h1 style='font-size:2rem;font-weight:800;margin:0;color:#0d1f52;'>
            🌿 San Ecoland
            <span style='font-size:1.1rem;font-weight:400;color:#94a3b8;'> / Smart City Telemetry</span>
        </h1>
        <p style='margin:6px 0 0;color:#64748b;font-size:0.95rem;'>
            Monitoreo en tiempo real · Red IoT: 10 Smart Bus Stops + 5 Hydration Stations
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── SECCIÓN 1: MÉTRICAS GLOBALES ──────────────────────────
    total_kwh   = sum(s["total_kwh"]   for s in stations.values())
    total_co2   = sum(s["co2_reduced"] for s in stations.values())
    total_solar = sum(s["solar_kwh"]   for s in stations.values())
    alert_count = len(failing)

    st.markdown('<p class="sec-label">🌐 Métricas Globales de Red — Noviembre 2026</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("⚡ Energía Producida",    f"{total_kwh:,.1f} kWh",   "▲ +8.3% vs mes anterior")
    with c2:
        st.metric("🌱 CO₂ Reducido",         f"{total_co2:,.1f} kg",    f"≈ {total_co2/1000:.2f} toneladas")
    with c3:
        st.metric("☀️ Contribución Solar",   f"{(total_solar/total_kwh)*100:.1f}%", f"{total_solar:,.1f} kWh solar")
    with c4:
        st.metric("🔴 Alertas Activas",      f"{alert_count} nodos",    f"{15 - alert_count}/15 operativos", delta_color="inverse")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECCIONES 2 + 3: TELEMETRÍA DE ESTACIÓN ───────────────
    data         = stations[selected_station]
    is_hydration = data["type"] == "hydration"
    type_label   = "💧 Hydration Station" if is_hydration else "🚏 Smart Bus Stop"
    accent_color = "#1ab8cc" if is_hydration else "#0d1f52"

    # Tarjeta de cabecera de estación
    st.markdown(f"""
    <div class="card" style="border-left:4px solid {accent_color}; margin-bottom:16px; padding:18px 24px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:0.82rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;">{type_label}</div>
                <div style="font-size:1.75rem;font-weight:800;color:#0d1f52;margin-top:4px;">{selected_station}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.8rem;color:#94a3b8;font-weight:600;">ÚLTIMO HEARTBEAT</div>
                <div style="font-size:1.3rem;color:#1ab8cc;font-weight:700;">{data['last_seen']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<p class="sec-label">📅 Producción Mensual (Últimos 12 Meses)</p>', unsafe_allow_html=True)
        st.plotly_chart(
            monthly_bar_chart(data["monthly_kwh"]),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        # Métricas resumidas debajo del gráfico
        m1, m2, m3 = st.columns(3)
        m1.metric("Mes Actual",   f"{data['total_kwh']:.1f} kWh")
        m2.metric("CO₂ Offset",   f"{data['co2_reduced']:.1f} kg")
        m3.metric("Mejor Mes",    f"{max(data['monthly_kwh']):.1f} kWh")

    with col_right:
        st.markdown('<p class="sec-label">⚡ Balance de Fuentes de Energía</p>', unsafe_allow_html=True)
        st.plotly_chart(
            donut_chart(data["solar_kwh"], data["grid_kwh"]),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown(f"""
        <div style="display:flex;gap:20px;justify-content:center;margin-top:-8px;">
            <div style="text-align:center;">
                <div style="font-size:1.25rem;font-weight:700;color:#1ab8cc;">{data['solar_kwh']:.1f} kWh</div>
                <div style="font-size:0.82rem;color:#94a3b8;font-weight:600;">SOLAR</div>
            </div>
            <div style="color:#dde3ec;font-size:1.4rem;line-height:1;">|</div>
            <div style="text-align:center;">
                <div style="font-size:1.25rem;font-weight:700;color:#0d1f52;">{data['grid_kwh']:.1f} kWh</div>
                <div style="font-size:0.82rem;color:#94a3b8;font-weight:600;">GRID (EDEN)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECCIÓN 4: SALUD DEL SISTEMA ──────────────────────────
    st.markdown('<p class="sec-label">🩺 Estado del Sistema & Alertas Críticas</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)

    # WiFi
    with h1:
        wok = data["wifi_online"]
        chiller_temp_str = f"{random.uniform(4.5, 7.5):.1f} °C"
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.88rem;color:#64748b;font-weight:700;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.06em;">📶 Red WiFi</div>
            <div style="margin-bottom:12px;">{badge(wok)}</div>
            <div style="font-size:0.9rem;color:#475569;">
                {"Señal fuerte · Latencia: 12 ms" if wok else "Sin señal detectada"}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not wok:
            st.error("🚨 **WiFi OFFLINE** — Conectividad remota perdida. Revisión manual requerida.", icon="🔴")

    # Chiller
    with h2:
        cok = data["chiller_online"]
        ct  = f"{random.uniform(4.5,7.5):.1f} °C" if cok else "—"
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.88rem;color:#64748b;font-weight:700;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.06em;">🧊 Agua Fría (Chiller)</div>
            <div style="margin-bottom:12px;">{badge(cok, fail_txt="FALLA")}</div>
            <div style="font-size:0.9rem;color:#475569;">
                {"Temp: " + ct + " · Flujo: Normal" if cok else "Falla del chiller detectada"}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not cok:
            st.error("🚨 **CHILLER OFFLINE** — Agua fría suspendida. Ticket #CHI-004 generado.", icon="🔴")

    # Heater
    with h3:
        hok = data["heater_online"]
        ht  = f"{random.uniform(58,72):.1f} °C" if hok else "—"
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.88rem;color:#64748b;font-weight:700;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.06em;">🔥 Agua Caliente (Heater)</div>
            <div style="margin-bottom:12px;">{badge(hok, fail_txt="FALLA")}</div>
            <div style="font-size:0.9rem;color:#475569;">
                {"Temp: " + ht + " · Presión: OK" if hok else "Falla del heater detectada"}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not hok:
            st.error("🚨 **HEATER OFFLINE** — Agua caliente suspendida. Ticket #HTR-007 generado.", icon="🔴")

    # LED Lighting
    with h4:
        lok      = data["led_online"]
        led_mode = data["led_mode"]
        if not lok:
            led_badge = badge(False, fail_txt="FALLA")
        elif led_mode == "ECO":
            led_badge = badge(True, warn_mode="ECO")
        else:
            led_badge = badge(True, ok_txt="NORMAL")

        led_detail = ""
        if lok:
            led_detail = "Consumo estándar · 100%" if led_mode == "NORMAL" else "Modo eco · Consumo −40%"
        else:
            led_detail = "Módulo LED con falla"

        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.88rem;color:#64748b;font-weight:700;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.06em;">💡 Iluminación LED</div>
            <div style="margin-bottom:12px;">{led_badge}</div>
            <div style="font-size:0.9rem;color:#475569;">{led_detail}</div>
        </div>
        """, unsafe_allow_html=True)
        if not lok:
            st.error("🚨 **LED OFFLINE** — Iluminación sin funcionar. Ticket #LED-003 generado.", icon="🔴")

    # Banner de todo OK
    all_ok = wok and cok and hok and lok
    if all_ok:
        st.success("✅ Todos los sistemas están **operativos**. Sin alertas activas para esta estación.", icon="✅")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECCIÓN 5: CONTROL REMOTO DE ACTUADORES ───────────────
    st.markdown('<p class="sec-label">🎛️ Control Remoto de Actuadores</p>', unsafe_allow_html=True)
    init_session(data, selected_station)

    a1, a2, a3, a4 = st.columns(4)

    # ── Agua Fría (Chiller) ──
    with a1:
        with st.container(border=True):
            st.markdown("### 🧊 Agua Fría (Chiller)")
            st.caption("Activar / desactivar el sistema de agua fría.")
            ch_on = st.toggle(
                "Chiller activo",
                key=f"{selected_station}_chiller",
            )
            if not ch_on:
                st.radio(
                    "Modo al desactivar",
                    ["Idle (standby)", "Apagado total"],
                    key=f"{selected_station}_chiller_mode",
                    horizontal=True,
                )
                mode_txt = st.session_state[f"{selected_station}_chiller_mode"].split()[0]
                st.warning(f"⚠️ Chiller **desactivado** — Modo: {mode_txt}", icon="⚠️")
            else:
                st.info("🧊 Chiller activo · agua fría disponible.", icon="🧊")

    # ── Agua Caliente (Heater) ──
    with a2:
        with st.container(border=True):
            st.markdown("### 🔥 Agua Caliente (Heater)")
            st.caption("Activar / desactivar el sistema de agua caliente.")
            he_on = st.toggle(
                "Heater activo",
                key=f"{selected_station}_heater",
            )
            if not he_on:
                st.radio(
                    "Modo al desactivar",
                    ["Idle (standby)", "Apagado total"],
                    key=f"{selected_station}_heater_mode",
                    horizontal=True,
                )
                mode_txt = st.session_state[f"{selected_station}_heater_mode"].split()[0]
                st.warning(f"⚠️ Heater **desactivado** — Modo: {mode_txt}", icon="⚠️")
            else:
                st.info("🔥 Heater activo · agua caliente disponible.", icon="🔥")

    # ── WiFi ──
    with a3:
        with st.container(border=True):
            st.markdown("### 📶 Red WiFi")
            st.caption("Activar / desactivar el módulo WiFi de esta estación.")
            wi_on = st.toggle(
                "WiFi activo",
                key=f"{selected_station}_wifi_act",
            )
            if not wi_on:
                st.warning("⚠️ WiFi **desactivado** manualmente. Sin telemetría remota.", icon="⚠️")
            else:
                st.info("📶 WiFi activo · conectividad normal.", icon="📶")

    # ── Pantalla Digital ──
    with a4:
        with st.container(border=True):
            st.markdown("### 📺 Pantalla Digital")
            st.caption("Activar la pantalla o elegir modo al apagarla.")
            sc_on = st.toggle(
                "Pantalla activa",
                key=f"{selected_station}_screen",
            )
            if not sc_on:
                st.radio(
                    "Modo al apagar",
                    ["Idle (logo fijo)", "Black (sin señal)"],
                    key=f"{selected_station}_screen_mode",
                    horizontal=True,
                )
                mode_txt = st.session_state[f"{selected_station}_screen_mode"].split()[0]
                st.warning(f"⚠️ Pantalla **apagada** — Modo: {mode_txt}", icon="⚠️")
            else:
                st.info("📺 Pantalla activa · contenido programado.", icon="📺")

    # ── FOOTER ────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-top:36px;padding:14px 0;border-top:1px solid #dde3ec;
                display:flex;justify-content:space-between;align-items:center;
                font-size:0.84rem;color:#94a3b8;">
        <span>🌿 <strong style="color:#64748b;">San Ecoland Smart City</strong> · IoT Telemetry Platform v2.0</span>
        <span>Actualizado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ART</span>
        <span>Streamlit + Plotly</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
