"""
╔══════════════════════════════════════════════════════════════╗
║          SAN ECOLAND — Smart City Telemetry Dashboard        ║
║          IoT Network: 10 Smart Bus Stops + 5 Hydration Sta.  ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import random
import math

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
    /* ── Escala base de fuentes ── */
    html { font-size: 16px !important; }

    /* ── Variables de color ── */
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

    /* ── Fondo principal y prevención de scroll horizontal ── */
    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    .stApp { background-color: var(--bg) !important; color: var(--text) !important; }

    /* ── Tipografía base de encabezado ── */
    .main-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        color: var(--navy);
        line-height: 1.2;
    }
    .main-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        color: #94a3b8;
    }
    .main-desc {
        margin: 6px 0 0;
        color: var(--muted);
        font-size: 0.95rem;
    }
    .station-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0d1f52;
        margin-top: 4px;
    }

    /* ── Contenido de la sidebar ── */
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

    /* ── Botones de colapso y apertura del sidebar ── */
    div[data-testid="stSidebarCollapseButton"] button {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }
    div[data-testid="stSidebarCollapseButton"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    button[data-testid="stExpandSidebarButton"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        z-index: 9999999 !important;
        background: #0d1f52 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.3) !important;
        cursor: pointer !important;
        width: 38px !important;
        height: 38px !important;
        align-items: center !important;
        justify-content: center !important;
    }
    button[data-testid="stExpandSidebarButton"] svg,
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* ═════════════════════════════════════════════════════════════ */
    /* DESKTOP (>= 992px) — Sidebar navy fijo a la izquierda       */
    /* ═════════════════════════════════════════════════════════════ */
    @media (min-width: 992px) {
        section[data-testid="stSidebar"],
        [data-testid="stSidebar"] {
            min-width: 280px !important;
            width: 280px !important;
            max-width: 280px !important;
            background: var(--sidebar-bg) !important;
            transform: none !important;
            margin-left: 0 !important;
            left: 0 !important;
            top: 0 !important;
            position: relative !important;
            display: block !important;
            visibility: visible !important;
        }

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

        /* En desktop el sidebar siempre está visible, no se necesita botón de toggle */
        button[data-testid="stExpandSidebarButton"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    }

    /* ═════════════════════════════════════════════════════════════ */
    /* MOBILE & TABLET (< 992px) — Drawer flotante, 100% de ancho,  */
    /* columnas en vertical, tipografía adaptativa y cero squishing */
    /* ═════════════════════════════════════════════════════════════ */
    @media (max-width: 991px) {
        /* Sidebar como drawer flotante sobre la pantalla */
        section[data-testid="stSidebar"],
        [data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100vh !important;
            width: 85vw !important;
            max-width: 320px !important;
            min-width: 260px !important;
            z-index: 999999 !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.45) !important;
            background: var(--sidebar-bg) !important;
            transition: transform 0.25s ease-in-out !important;
        }

        /* Estado colapsado en móvil */
        section[data-testid="stSidebar"][aria-expanded="false"],
        [data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-105%) !important;
            display: none !important;
        }

        /* Estado expandido en móvil */
        section[data-testid="stSidebar"][aria-expanded="true"],
        [data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            display: block !important;
        }

        /* Contenedor principal ocupa el 100% sin dejar margen */
        .main, [data-testid="stMain"] {
            width: 100% !important;
            margin-left: 0 !important;
        }

        .main .block-container,
        [data-testid="stMainBlockContainer"],
        .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding-left: 12px !important;
            padding-right: 12px !important;
            padding-top: 54px !important; /* Espacio para el botón de menú */
            padding-bottom: 24px !important;
        }

        /* Apilar columnas en vertical en móvil para no apretar tarjetas */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 12px !important;
        }
        [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 4px !important;
        }

        /* Escala tipográfica adaptativa */
        .main-title {
            font-size: 1.45rem !important;
        }
        .main-subtitle {
            font-size: 0.88rem !important;
            display: block !important;
            margin-top: 2px !important;
        }
        .main-desc {
            font-size: 0.82rem !important;
        }
        .station-title {
            font-size: 1.35rem !important;
        }
        .metric-value {
            font-size: 1.65rem !important;
        }
        .metric-box {
            padding: 14px 16px !important;
        }
        .card {
            padding: 14px 16px !important;
        }
    }

    /* Texto sidebar */
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

    /* Botones de alerta en sidebar */
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

    /* ── Tarjetas métricas y contenedores nativos HTML ── */
    .metric-box {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: var(--shadow);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: var(--navy);
        line-height: 1.15;
    }
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;
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
        padding: 18px 20px;
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

    /* ── Toggles y radios ── */
    .stToggle label { color: var(--text) !important; font-weight: 600; font-size: 0.95rem !important; }
    .stRadio  label { color: var(--muted) !important; font-size: 0.88rem !important; }
    .stRadio > div > label { color: var(--text) !important; }
    .stMarkdown p  { font-size: 1rem; }
    .stCaptionContainer p { color: var(--muted) !important; font-size: 0.88rem !important; }

    /* ── Limpieza de decoraciones ── */
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
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPERS — etiquetas mensuales (últimos 12 meses)
# ─────────────────────────────────────────────────────────────
def month_label(months_back: int) -> str:
    now = datetime.now()
    m = now.month - months_back
    y = now.year
    while m <= 0:
        m += 12
        y -= 1
    return datetime(y, m, 1).strftime("%b %Y")

MONTH_LABELS = [month_label(i) for i in range(11, -1, -1)]


# ─────────────────────────────────────────────────────────────
# MOCK DATA — generación realista y determinística
# ─────────────────────────────────────────────────────────────
@st.cache_data
def generate_mock_data() -> dict:
    rng = np.random.default_rng(seed=42)

    bus_stops = [f"Smart Bus Stop #{i:02d}" for i in range(1, 11)]
    hydration  = [f"Hydration Station #{i:02d}" for i in range(1, 6)]

    stations = {}
    for i, name in enumerate(bus_stops + hydration):
        is_hydration = "Hydration" in name

        # 12 meses de kWh realistas
        base = rng.uniform(280, 520)
        monthly = rng.normal(loc=base / 12 * 30, scale=base * 0.07, size=12)
        monthly = np.clip(monthly, 60, None).round(1)
        total_kwh  = float(round(monthly[-1], 1))
        solar_pct  = rng.uniform(0.30, 0.78)
        solar_kwh  = round(total_kwh * solar_pct, 1)
        grid_kwh   = round(total_kwh * (1 - solar_pct), 1)

        # Exactamente 3 estaciones con problemas para la demo
        wifi_ok    = (i != 2)               # Smart Bus Stop #03 → WiFi offline
        chiller_ok = (i != 5)               # Smart Bus Stop #06 → Chiller fault
        heater_ok  = (i != 12)              # Hydration Station #03 → Heater fault
        led_ok     = (i != 5)               # Smart Bus Stop #06 → LED fault
        led_mode   = "FALLA" if not led_ok else ("ECO" if i in [1, 7, 9] else "NORMAL")

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
# NATIVE HTML METRIC CARD RENDERER (Zero dynamic JS chunks)
# ─────────────────────────────────────────────────────────────
def render_metric_card(label: str, value: str, delta: str = None, delta_type: str = "positive") -> str:
    delta_html = ""
    if delta:
        if delta_type == "positive":
            d_color = "#059669"
        elif delta_type == "negative":
            d_color = "#b91c1c"
        else:
            d_color = "#64748b"
        delta_html = f'<div class="metric-delta" style="color:{d_color};">{delta}</div>'
    
    return f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{delta_html}</div>'


# ─────────────────────────────────────────────────────────────
# NATIVE SVG BAR CHART (12 Meses — ultra-rápido, sin dependencias)
# ─────────────────────────────────────────────────────────────
def render_svg_bar_chart(monthly_kwh: list, month_labels: list) -> str:
    max_val = max(monthly_kwh) * 1.15
    avg_val = float(np.mean(monthly_kwh))
    w = 640
    h = 240
    chart_h = 165
    chart_y = 20
    bar_w = 28
    gap = (w - (bar_w * 12)) / 13
    
    avg_y = chart_y + chart_h - (avg_val / max_val * chart_h)
    
    svg = [
        f'<div class="card" style="padding:16px 20px;">',
        f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto;max-height:240px;display:block;">',
    ]
    
    # Líneas de cuadrícula
    for step in [0.25, 0.5, 0.75, 1.0]:
        gy = chart_y + chart_h - (step * chart_h)
        svg.append(f'<line x1="0" y1="{gy:.1f}" x2="{w}" y2="{gy:.1f}" stroke="#f1f5f9" stroke-width="1.2"/>')
        
    # Línea de promedio
    svg.append(f'<line x1="0" y1="{avg_y:.1f}" x2="{w}" y2="{avg_y:.1f}" stroke="#f59e0b" stroke-width="1.6" stroke-dasharray="5,4"/>')
    svg.append(f'<text x="{w-5}" y="{avg_y-5:.1f}" fill="#b45309" font-size="11" font-weight="700" text-anchor="end" font-family="system-ui, sans-serif">Prom. {avg_val:.0f} kWh</text>')
    
    # Barras de los 12 meses
    for idx, (val, label) in enumerate(zip(monthly_kwh, month_labels)):
        bx = gap + idx * (bar_w + gap)
        bh = (val / max_val) * chart_h
        by = chart_y + chart_h - bh
        color = "#0d1f52" if idx == 11 else ("#1ab8cc" if val >= avg_val else "#cbd5e1")
        svg.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{bh:.1f}" rx="4" fill="{color}">')
        svg.append(f'<title>{label}: {val:.1f} kWh</title>')
        svg.append('</rect>')
        # Etiqueta de mes
        svg.append(f'<text x="{bx + bar_w/2:.1f}" y="{chart_y + chart_h + 24}" fill="#64748b" font-size="10" font-weight="600" font-family="system-ui, sans-serif" text-anchor="middle" transform="rotate(-30, {bx + bar_w/2:.1f}, {chart_y + chart_h + 24})">{label}</text>')
        
    svg.append('</svg></div>')
    return "".join(svg)


# ─────────────────────────────────────────────────────────────
# NATIVE SVG DONUT CHART (Solar vs Grid — exacto y responsivo)
# ─────────────────────────────────────────────────────────────
def render_svg_donut(solar_kwh: float, grid_kwh: float) -> str:
    total = solar_kwh + grid_kwh
    solar_pct = (solar_kwh / total) if total > 0 else 0.5
    
    r = 62
    circ = 2 * math.pi * r
    solar_dash = circ * solar_pct
    
    lines = [
        '<div class="card" style="padding:16px 20px; display:flex; flex-direction:column; align-items:center; justify-content:center;">',
        '<svg viewBox="0 0 200 200" style="width:100%; max-width:210px; height:auto; display:block;">',
        f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="#0d1f52" stroke-width="26" stroke-dasharray="{circ:.1f}" stroke-dashoffset="0" transform="rotate(-90 100 100)"/>',
        f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="#1ab8cc" stroke-width="26" stroke-dasharray="{solar_dash:.1f} {circ:.1f}" stroke-dashoffset="0" transform="rotate(-90 100 100)"/>',
        f'<text x="100" y="96" text-anchor="middle" font-size="24" font-weight="800" fill="#0d1f52" font-family="system-ui, sans-serif">{total:.0f}</text>',
        '<text x="100" y="116" text-anchor="middle" font-size="11" font-weight="700" fill="#64748b" font-family="system-ui, sans-serif">kWh total</text>',
        '</svg>',
        '<div style="display:flex; gap:20px; justify-content:center; margin-top:8px;">',
        f'<div style="text-align:center;"><div style="font-size:1.15rem; font-weight:800; color:#1ab8cc;">{solar_kwh:.1f} kWh</div><div style="font-size:0.75rem; color:#94a3b8; font-weight:700;">SOLAR ({solar_pct*100:.1f}%)</div></div>',
        '<div style="color:#dde3ec; font-size:1.4rem; line-height:1;">|</div>',
        f'<div style="text-align:center;"><div style="font-size:1.15rem; font-weight:800; color:#0d1f52;">{grid_kwh:.1f} kWh</div><div style="font-size:0.75rem; color:#94a3b8; font-weight:700;">GRID ({(1-solar_pct)*100:.1f}%)</div></div>',
        '</div></div>'
    ]
    return "".join(lines)


# ─────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────
def main():
    stations     = generate_mock_data()
    station_list = list(stations.keys())

    # 3 estaciones con problemas para la demo
    failing = {
        nm: d for nm, d in stations.items()
        if not d["wifi_online"] or not d["chiller_online"]
        or not d["heater_online"] or not d["led_online"]
    }

    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:18px 0 22px;'>
            <div style='font-size:2.4rem;'>🌿</div>
            <div style='font-size:1.3rem; font-weight:800; color:#1ab8cc; letter-spacing:0.05em;'>SAN ECOLAND</div>
            <div style='font-size:0.8rem; color:#8b9ec8; letter-spacing:0.1em; text-transform:uppercase; margin-top:4px;'>Smart City · IoT Dashboard</div>
        </div>
        <div style='border-top:1px solid rgba(255,255,255,0.1); margin:0 0 18px;'></div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.8rem;font-weight:800;letter-spacing:0.14em;text-transform:uppercase;color:#8b9ec8;margin-bottom:10px;">📡 Seleccionar Nodo</div>', unsafe_allow_html=True)

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

        # Panel de Alertas Activas
        n_alerts = len(failing)
        alert_title_color = "#fca5a5" if n_alerts > 0 else "#6ee7b7"
        alert_title_ico   = "🚨" if n_alerts > 0 else "✅"

        st.markdown(
            f'<div style="font-size:0.8rem;font-weight:800;letter-spacing:0.12em;'
            f'text-transform:uppercase;color:{alert_title_color};margin-bottom:12px;">'
            f'{alert_title_ico} Alertas Activas ({n_alerts})</div>',
            unsafe_allow_html=True,
        )

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

            if st.button(f"→ Ir a {short}", key=f"nav_{fname}"):
                st.session_state["navigate_to"] = fname
                st.rerun()

        st.markdown(f"""
        <div style='border-top:1px solid rgba(255,255,255,0.1);margin-top:22px;padding-top:14px;
                    font-size:0.78rem;color:#4a5f8a;text-align:center;'>
            Refresh: {datetime.now().strftime("%H:%M:%S")}<br>15 nodos activos
        </div>
        """, unsafe_allow_html=True)

    # ── HEADER PRINCIPAL ─────────────────────────────────────
    st.markdown("""
    <div style='padding:4px 0 16px;'>
        <h1 class='main-title'>
            🌿 San Ecoland
            <span class='main-subtitle'> / Smart City Telemetry</span>
        </h1>
        <p class='main-desc'>
            Monitoreo en tiempo real · Red IoT: 10 Smart Bus Stops + 5 Hydration Stations
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── SECCIÓN 1: MÉTRICAS GLOBALES (Native HTML, Zero Chunks) ─
    total_kwh   = sum(s["total_kwh"]   for s in stations.values())
    total_co2   = sum(s["co2_reduced"] for s in stations.values())
    total_solar = sum(s["solar_kwh"]   for s in stations.values())
    alert_count = len(failing)

    st.markdown('<p class="sec-label">🌐 Métricas Globales de Red — Noviembre 2026</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_metric_card("⚡ Energía Producida", f"{total_kwh:,.1f} kWh", "▲ +8.3% vs mes anterior", "positive"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_metric_card("🌱 CO₂ Reducido", f"{total_co2:,.1f} kg", f"≈ {total_co2/1000:.2f} toneladas", "neutral"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_metric_card("☀️ Contribución Solar", f"{(total_solar/total_kwh)*100:.1f}%", f"{total_solar:,.1f} kWh solar", "positive"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_metric_card("🔴 Alertas Activas", f"{alert_count} nodos", f"{15 - alert_count}/15 operativos", "negative"), unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECCIONES 2 + 3: TELEMETRÍA DE ESTACIÓN ───────────────
    data         = stations[selected_station]
    is_hydration = data["type"] == "hydration"
    type_label   = "💧 Hydration Station" if is_hydration else "🚏 Smart Bus Stop"
    accent_color = "#1ab8cc" if is_hydration else "#0d1f52"

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {accent_color}; margin-bottom:16px; padding:18px 24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <div style="font-size:0.82rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;">{type_label}</div>
                <div class="station-title">{selected_station}</div>
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
        st.markdown(render_svg_bar_chart(data["monthly_kwh"], MONTH_LABELS), unsafe_allow_html=True)
        
        # Mini cards de resumen mensual
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(render_metric_card("Mes Actual", f"{data['total_kwh']:.1f} kWh"), unsafe_allow_html=True)
        with m2:
            st.markdown(render_metric_card("CO₂ Offset", f"{data['co2_reduced']:.1f} kg"), unsafe_allow_html=True)
        with m3:
            st.markdown(render_metric_card("Mejor Mes", f"{max(data['monthly_kwh']):.1f} kWh"), unsafe_allow_html=True)

    with col_right:
        st.markdown('<p class="sec-label">⚡ Balance de Fuentes de Energía</p>', unsafe_allow_html=True)
        st.markdown(render_svg_donut(data["solar_kwh"], data["grid_kwh"]), unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECCIÓN 4: SALUD DEL SISTEMA ──────────────────────────
    st.markdown('<p class="sec-label">🩺 Estado del Sistema & Alertas Críticas</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)

    # WiFi
    with h1:
        wok = data["wifi_online"]
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

    all_ok = wok and cok and hok and lok
    if all_ok:
        st.success("✅ Todos los sistemas están **operativos**. Sin alertas activas para esta estación.", icon="✅")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECCIÓN 5: CONTROL REMOTO DE ACTUADORES ───────────────
    st.markdown('<p class="sec-label">🎛️ Control Remoto de Actuadores</p>', unsafe_allow_html=True)
    init_session(data, selected_station)

    a1, a2, a3, a4 = st.columns(4)

    # Agua Fría (Chiller)
    with a1:
        with st.container(border=True):
            st.markdown("### 🧊 Agua Fría (Chiller)")
            st.caption("Activar / desactivar el sistema de agua fría.")
            ch_on = st.toggle("Chiller activo", key=f"{selected_station}_chiller")
            if not ch_on:
                st.radio("Modo al desactivar", ["Idle (standby)", "Apagado total"], key=f"{selected_station}_chiller_mode", horizontal=True)
                mode_txt = st.session_state[f"{selected_station}_chiller_mode"].split()[0]
                st.warning(f"⚠️ Chiller **desactivado** — Modo: {mode_txt}", icon="⚠️")
            else:
                st.info("🧊 Chiller activo · agua fría disponible.", icon="🧊")

    # Agua Caliente (Heater)
    with a2:
        with st.container(border=True):
            st.markdown("### 🔥 Agua Caliente (Heater)")
            st.caption("Activar / desactivar el sistema de agua caliente.")
            he_on = st.toggle("Heater activo", key=f"{selected_station}_heater")
            if not he_on:
                st.radio("Modo al desactivar", ["Idle (standby)", "Apagado total"], key=f"{selected_station}_heater_mode", horizontal=True)
                mode_txt = st.session_state[f"{selected_station}_heater_mode"].split()[0]
                st.warning(f"⚠️ Heater **desactivado** — Modo: {mode_txt}", icon="⚠️")
            else:
                st.info("🔥 Heater activo · agua caliente disponible.", icon="🔥")

    # WiFi
    with a3:
        with st.container(border=True):
            st.markdown("### 📶 Red WiFi")
            st.caption("Activar / desactivar el módulo WiFi de esta estación.")
            wi_on = st.toggle("WiFi activo", key=f"{selected_station}_wifi_act")
            if not wi_on:
                st.warning("⚠️ WiFi **desactivado** manualmente. Sin telemetría remota.", icon="⚠️")
            else:
                st.info("📶 WiFi activo · conectividad normal.", icon="📶")

    # Pantalla Digital
    with a4:
        with st.container(border=True):
            st.markdown("### 📺 Pantalla Digital")
            st.caption("Activar la pantalla o elegir modo al apagarla.")
            sc_on = st.toggle("Pantalla activa", key=f"{selected_station}_screen")
            if not sc_on:
                st.radio("Modo al apagar", ["Idle (logo fijo)", "Black (sin señal)"], key=f"{selected_station}_screen_mode", horizontal=True)
                mode_txt = st.session_state[f"{selected_station}_screen_mode"].split()[0]
                st.warning(f"⚠️ Pantalla **apagada** — Modo: {mode_txt}", icon="⚠️")
            else:
                st.info("📺 Pantalla activa · contenido programado.", icon="📺")

    # ── FOOTER ────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-top:36px;padding:14px 0;border-top:1px solid #dde3ec;
                display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;
                font-size:0.84rem;color:#94a3b8;">
        <span>🌿 <strong style="color:#64748b;">San Ecoland Smart City</strong> · IoT Telemetry Platform v2.0</span>
        <span>Actualizado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ART</span>
        <span>Modo Demo · Alta Disponibilidad</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
