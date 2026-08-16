import streamlit as st
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium
import pandas as pd
import plotly.graph_objects as go
import json
import os

st.set_page_config(
    page_title="Expedição Patagônia · Elétrico vs Combustão",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SISTEMA DE IDIOMAS (PT / ES / EN)
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

TRANSLATIONS = {
    "pt": {
        "page_title": "Expedição Patagônia · Elétrico vs Combustão",
        "hero_tag": "PESQUISA DE CAMPO CIENTÍFICA & AUTOMOTIVA · 2024–2026",
        "hero_title": "Expedição Patagônia:\nElétrico vs Combustão",
        "hero_subtitle": "Simulação imersiva de uma jornada épica de São Paulo (Mooca) ao Fim do Mundo (Ushuaia e Puerto Williams). Mais de 5.000 km cruzando 4 países, avaliando autonomia, infraestrutura, custos e viabilidade técnica ponto a ponto.",
        "badge1": "🔋 Tesla Model 3 Long Range", "badge2": "⛽ Hyundai Tucson 2.0", "badge3": "🇧🇷 🇺🇾 🇦🇷 🇨🇱 4 Países",
        "badge4": "~5.000 KM", "badge5": "13 Pontos Mapeados",
        "nav_title": "Navegação da Expedição",
        "nav_home": "🌟 Visão Geral & Painel",
        "nav_map": "🗺️ Mapa Interativo & Rota",
        "nav_stops": "📍 Diário de Bordo & Paradas",
        "nav_specs": "🔬 Ficha Técnica & Custos",
        "nav_tech": "⚙️ Metodologia & Dados",
        "m1": "Distância Total", "m2": "Custo Estimado (Tesla)", "m3": "Custo Estimado (Tucson)", "m4": "Economia do Elétrico",
        "tab1": "🗺️ Mapa Geoespacial Interativo", "tab2": "📍 Diário Detalhado dos 13 Pontos",
        "tab3": "🔬 Comparativo Técnico & Financeiro", "tab4": "🌐 Contexto Geopolítico & Antártico",
        "map_label": "TRACKING DA EXPEDIÇÃO", "map_title": "Trajeto Continental e Rotas do Fim do Mundo",
        "map_hint": "💡 <strong>Dica de Navegação:</strong> Clique nos marcadores do mapa para inspecionar as condições de cada parada, tipo de infraestrutura e relevo.",
        "details_label": "ESTAÇÕES DA ROTA", "details_title": "Raio-X dos Pontos de Parada",
        "specs_label": "ANÁLISE COMPARATIVA", "specs_title": "Custos, Emissões e Desafios Logísticos",
        "why_go_title": "Por que esta expedição importa?",
        "why_go_text": "A transição energética para a mobilidade elétrica enfrenta seu teste definitivo nas rodovias remotas da América do Sul. Enquanto a Ruta 3 oferece combustíveis fósseis tradicionais a cada cidade, a malha de carregadores rápidos CCS2 exige planejamento milimétrico, transformando a viagem em um fascinante estudo de caso sobre autonomia, resiliência de baterias e infraestrutura transnacional.",
        "route_overview_title": "Itinerário Completo da Rota",
        "route_overview_text": "Início: São Paulo (Mooca), BR → Curitiba → Florianópolis → Porto Alegre → Chuí (Fronteira Brasil-Uruguai) → Punta del Este → Buenos Aires → Bahía Blanca → Puerto Madryn → Comodoro Rivadavia → Río Gallegos → Fim 1: Ushuaia (Argentina) → Fim 2: Puerto Williams (Chile, Isla Navarino).",
        "tech_label": "TECNOLOGIAS & PILHA DE DADOS",
        "footer_title": "🚗 Amauri Almeida · Pesquisador & Autor",
        "footer_desc": "Tecnólogo em Gestão Ambiental (FATEC Jundiaí) · Pós-Graduando em IA, Machine Learning & Data Science e Big Data<br>Análise e Desenvolvimento de Sistemas (FACINT Maringá)",
        "footer_links": "📍 Brasil · Uruguai · Argentina · Chile",
    },
    "es": {
        "page_title": "Expedición Patagonia · Eléctrico vs Combustión",
        "hero_tag": "INVESTIGACIÓN DE CAMPO CIENTÍFICA & AUTOMOTOR · 2024–2026",
        "hero_title": "Expedición Patagonia:\nEléctrico vs Combustión",
        "hero_subtitle": "Simulación inmersiva de un viaje épico desde São Paulo (Mooca) hasta el Fin del Mundo (Ushuaia y Puerto Williams). Más de 5.000 km cruzando 4 países, evaluando autonomía, infraestructura y viabilidad técnica punto a punto.",
        "badge1": "🔋 Tesla Model 3 Long Range", "badge2": "⛽ Hyundai Tucson 2.0", "badge3": "🇧🇷 🇺🇾 🇦🇷 🇨🇱 4 Países",
        "badge4": "~5.000 KM", "badge5": "13 Puntos Mapeados",
        "nav_title": "Navegación de la Expedición",
        "nav_home": "🌟 Visión General & Panel",
        "nav_map": "🗺️ Mapa Interactivo & Ruta",
        "nav_stops": "📍 Diario de Ruta & Paradas",
        "nav_specs": "🔬 Ficha Técnica & Costos",
        "nav_tech": "⚙️ Metodología & Datos",
        "m1": "Distancia Total", "m2": "Costo Estimado (Tesla)", "m3": "Costo Estimado (Tucson)", "m4": "Ahorro del Eléctrico",
        "tab1": "🗺️ Mapa Geoespacial Interactivo", "tab2": "📍 Diario Detallado de los 13 Puntos",
        "tab3": "🔬 Comparativa Técnica & Financiera", "tab4": "🌐 Contexto Geopolítico & Antártico",
        "map_label": "TRACKING DE LA EXPEDICIÓN", "map_title": "Trayecto Continental y Rutas al Fin del Mundo",
        "map_hint": "💡 <strong>Consejo:</strong> Haga clic en los marcadores del mapa para inspeccionar el estado de cada parada, infraestructura y clima.",
        "details_label": "ESTACIONES DE LA RUTA", "details_title": "Rayos X de los Puntos de Parada",
        "specs_label": "ANÁLISIS COMPARATIVO", "specs_title": "Costos, Emisiones y Desafíos Logísticos",
        "why_go_title": "¿Por qué importa esta expedición?",
        "why_go_text": "La transición energética hacia la movilidad eléctrica enfrenta su prueba definitiva en las rutas remotas de Sudamérica. Mientras que la Ruta 3 ofrece combustibles fósiles tradicionales, la red de cargadores rápidos exige una planificación milimétrica, convirtiendo el viaje en un fascinante estudio de caso sobre autonomía y resiliência.",
        "route_overview_title": "Itinerario Completo de la Ruta",
        "route_overview_text": "Inicio: São Paulo (Mooca), BR → Curitiba → Florianópolis → Porto Alegre → Chuí (Frontera Brasil-Uruguay) → Punta del Este → Buenos Aires → Bahía Blanca → Puerto Madryn → Comodoro Rivadavia → Río Gallegos → Fin 1: Ushuaia (Argentina) → Fin 2: Puerto Williams (Chile, Isla Navarino).",
        "tech_label": "TECNOLOGÍAS & STACK DE DATOS",
        "footer_title": "🚗 Amauri Almeida · Investigador & Autor",
        "footer_desc": "Tecnólogo en Gestión Ambiental (FATEC Jundiaí) · Posgrado en IA, Machine Learning & Data Science y Big Data<br>Análisis y Desarrollo de Sistemas (FACINT Maringá)",
        "footer_links": "📍 Brasil · Uruguay · Argentina · Chile",
    },
    "en": {
        "page_title": "Patagonia Expedition · Electric vs Combustion",
        "hero_tag": "SCIENTIFIC FIELD RESEARCH & AUTOMOTIVE · 2024–2026",
        "hero_title": "Patagonia Expedition:\nElectric vs Combustion",
        "hero_subtitle": "Immersive simulation of an epic journey from São Paulo (Mooca) to the End of the World (Ushuaia & Puerto Williams). Over 5,000 km crossing 4 countries, evaluating range, infrastructure, costs, and technical viability point by point.",
        "badge1": "🔋 Tesla Model 3 Long Range", "badge2": "⛽ Hyundai Tucson 2.0", "badge3": "🇧🇷 🇺🇾 🇦🇷 🇨🇱 4 Countries",
        "badge4": "~5,000 KM", "badge5": "13 Mapped Points",
        "nav_title": "Expedition Navigation",
        "nav_home": "🌟 Overview & Dashboard",
        "nav_map": "🗺️ Interactive Map & Route",
        "nav_stops": "📍 Expedition Log & Stops",
        "nav_specs": "🔬 Tech Specs & Costs",
        "nav_tech": "⚙️ Methodology & Data",
        "m1": "Total Distance", "m2": "Estimated Cost (Tesla)", "m3": "Estimated Cost (Tucson)", "m4": "EV Savings",
        "tab1": "🗺️ Interactive Geospatial Map", "tab2": "📍 Detailed 13-Point Route Log",
        "tab3": "🔬 Technical & Financial Comparison", "tab4": "🌐 Geopolitical & Antarctic Context",
        "map_label": "EXPEDITION TRACKING", "map_title": "Continental Route and End of the World Paths",
        "map_hint": "💡 <strong>Tip:</strong> Click any map marker to inspect stop conditions, infrastructure, and climate.",
        "details_label": "ROUTE STATIONS", "details_title": "X-Ray of Stop Points",
        "specs_label": "COMPARATIVE ANALYSIS", "specs_title": "Costs, Emissions, and Logistical Challenges",
        "why_go_title": "Why does this expedition matter?",
        "why_go_text": "The energy transition toward electric mobility faces its ultimate test on South America's remote highways. While Ruta 3 offers traditional fossil fuels, the fast-charger network requires meticulous planning, turning the trip into a fascinating case study on battery range and infrastructure resilience.",
        "route_overview_title": "Complete Route Itinerary",
        "route_overview_text": "Start: São Paulo (Mooca), BR → Curitiba → Florianópolis → Porto Alegre → Chuí (Brazil-Uruguay Border) → Punta del Este → Buenos Aires → Bahía Blanca → Puerto Madryn → Comodoro Rivadavia → Río Gallegos → End 1: Ushuaia (Argentina) → End 2: Puerto Williams (Chile, Navarino Island).",
        "tech_label": "TECHNOLOGIES & DATA STACK",
        "footer_title": "🚗 Amauri Almeida · Researcher & Author",
        "footer_desc": "Environmental Management Technologist (FATEC Jundiaí) · Post-Grad in AI, Machine Learning & Data Science and Big Data<br>Systems Analysis and Development (FACINT Maringá)",
        "footer_links": "📍 Brazil · Uruguay · Argentina · Chile",
    }
}

# ============================================================
# ESTILOS CSS CUSTOMIZADOS (DESIGN IMERSIVO "WOW")
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono&display=swap');

:root {
    --primary: #1b3b6f;
    --primary-light: #218380;
    --accent: #ffb703;
    --ice: #e0fbfc;
    --dark: #0b132b;
    --card-bg: #ffffff;
    --text-main: #1d3557;
    --text-muted: #64748b;
    --danger: #e63946;
    --success: #2a9d8f;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-main);
}

.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #edf2f7 100%);
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b132b 0%, #1b3b6f 100%);
    color: white;
}
[data-testid="stSidebar"] .stRadio label {
    color: #e2e8f0 !important;
    font-weight: 500;
}

/* Hero Section */
.hero-wrap {
    background: linear-gradient(135deg, #0b132b 0%, #1b3b6f 50%, #218380 100%);
    border-radius: 24px;
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(11, 19, 43, 0.25);
}
.hero-wrap::after {
    content: "🏔️";
    font-size: 160px;
    position: absolute;
    right: 20px;
    bottom: -30px;
    opacity: 0.15;
}
.hero-tag {
    background: rgba(255, 183, 3, 0.2);
    color: #ffb703;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 6px 14px;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(255, 183, 3, 0.4);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 1rem;
    white-space: pre-line;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: rgba(255, 255, 255, 0.85);
    max-width: 720px;
    line-height: 1.6;
    margin-bottom: 1.8rem;
}
.hero-badges {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #ffffff;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 6px 14px;
    border-radius: 30px;
    backdrop-filter: blur(5px);
}
.badge-highlight {
    background: rgba(42, 157, 143, 0.3);
    border-color: #2a9d8f;
    color: #99f6e4;
}

/* Metric Cards */
.metric-box {
    background: var(--card-bg);
    border-radius: 18px;
    padding: 1.5rem;
    border-top: 4px solid var(--primary-light);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04);
    text-align: center;
    transition: transform 0.2s ease;
}
.metric-box:hover {
    transform: translateY(-4px);
}
.metric-box.danger { border-top-color: var(--danger); }
.metric-box.success { border-top-color: var(--success); }
.metric-val {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: var(--primary);
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.metric-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}

/* Section Titles */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--primary-light);
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 0.4rem;
    font-weight: 700;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 1.5rem;
    line-height: 1.2;
}

/* Info Cards */
.info-card {
    background: var(--card-bg);
    border-radius: 18px;
    padding: 1.8rem;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
    border-left: 5px solid var(--primary-light);
    margin-bottom: 1.2rem;
}
.alert-box {
    background: #e0fbfc;
    border-left: 5px solid var(--primary-light);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1.2rem 0;
    font-size: 0.92rem;
    color: #0b132b;
}

/* Footer */
.footer-wrap {
    background: linear-gradient(135deg, #0b132b 0%, #1b3b6f 100%);
    border-radius: 20px;
    padding: 2.5rem;
    color: rgba(255, 255, 255, 0.85);
    text-align: center;
    margin-top: 4rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.footer-title {
    font-family: 'Playfair Display', serif;
    color: #ffb703;
    font-size: 1.4rem;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR DE NAVEGAÇÃO E IDIOMA
# ============================================================
with st.sidebar:
    st.markdown("### 🌐 Idioma / Language")
    selected_lang = st.selectbox(
        "Selecione o idioma:",
        options=["pt", "es", "en"],
        format_func=lambda x: {"pt": "🇧🇷 Português", "es": "🇪🇸 Español", "en": "🇺🇸 English"}[x],
        index=["pt", "es", "en"].index(st.session_state.lang)
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    T = TRANSLATIONS[st.session_state.lang]

    st.markdown("---")
    st.markdown(f"### {T['nav_title']}")
    nav_choice = st.radio(
        "Navegação",
        options=[T["nav_home"], T["nav_map"], T["nav_stops"], T["nav_specs"], T["nav_tech"]],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🚗 Veículos em Comparação")
    st.info("🔋 **Tesla Model 3 Long Range (2024)**\n\n⛽ **Hyundai Tucson 2.0 (2024)**")
    st.markdown("---")
    st.markdown("### 🇦🇺 Rota Transnacional")
    st.markdown("🇧🇷 **Brasil** ➔ 🇺🇾 **Uruguai** ➔ 🇦🇷 **Argentina** ➔ 🇨🇱 **Chile**")

# ============================================================
# CARREGAMENTO DOS DADOS ENRIQUECIDOS DA ROTA
# ============================================================
@st.cache_data
def load_route_data():
    path = "route_data_enhanced.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

route_data = load_route_data()

# ============================================================
# CORPO PRINCIPAL
# ============================================================

# Hero Banner
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-tag">{T['hero_tag']}</div>
    <div class="hero-title">{T['hero_title']}</div>
    <div class="hero-subtitle">{T['hero_subtitle']}</div>
    <div class="hero-badges">
        <span class="badge badge-highlight">{T['badge1']}</span>
        <span class="badge badge-highlight">{T['badge2']}</span>
        <span class="badge">{T['badge3']}</span>
        <span class="badge">{T['badge4']}</span>
        <span class="badge">{T['badge5']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SEÇÃO 1: VISÃO GERAL & PAINEL (HOME) ─────────────────────
if nav_choice == T["nav_home"]:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-box"><div class="metric-val">~5.100 km</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box success"><div class="metric-val">$460</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box danger"><div class="metric-val">$1.250</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-box"><div class="metric-val">2.7×</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.markdown(f'<div class="section-label">CONTEXTO DA PESQUISA</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{T["why_go_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card">
            <p style="line-height: 1.7; font-size: 0.98rem; color: #1d3557;">
            {T['why_go_text']}
            </p>
            <br>
            <p style="line-height: 1.7; font-size: 0.95rem; color: #64748b;">
            A expedição simula rigorosamente o consumo de energia elétrica versus combustíveis fósseis, contemplando variações de relevo na Cordillera dos Andes, ventos patagônicos laterais, densidade de eletropostos na malha UTE uruguaia e postos YPF argentinos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown(f'<div class="section-label">ROTA MUNDIAL DO FIM DO MUNDO</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">De São Paulo à Isla Navarino</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #218380;">
            <strong>{T['route_overview_title']}</strong><br><br>
            <p style="font-size: 0.9rem; color: #334155; line-height: 1.6;">
            {T['route_overview_text']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">DESTAQUES DA EXPEDIÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Galeria de Paradas Estratégicas</div>', unsafe_allow_html=True)

    # Exibir cards interativos para algumas paradas-chave
    cols = st.columns(3)
    key_stops = [route_data[0], route_data[6], route_data[11], route_data[12]] if len(route_data) >= 13 else route_data[:3]
    
    for i, stop in enumerate(key_stops[:3]):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05); height: 100%; border-top: 4px solid #1b3b6f;">
                <div style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #218380; font-weight: 700; margin-bottom: 0.5rem;">PARADA #{stop['id']} · {stop['country']}</div>
                <div style="font-family: 'Playfair Display'; font-size: 1.3rem; font-weight: 700; color: #1b3b6f; margin-bottom: 0.5rem;">{stop['name']}</div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 1rem;">📏 {stop['distance_from_start']} desde São Paulo</div>
                <p style="font-size: 0.88rem; color: #334155; line-height: 1.5;">{stop['highlights']}</p>
            </div>
            """, unsafe_allow_html=True)

# ── SEÇÃO 2: MAPA INTERATIVO & ROTA ─────────────────────────
elif nav_choice == T["nav_map"]:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="alert-box">{T["map_hint"]}</div>', unsafe_allow_html=True)

    if route_data:
        m = folium.Map(location=[-40, -62], zoom_start=4, tiles='CartoDB positron')

        points = [[c['lat'], c['lon']] for c in route_data]

        # Linha base da rota
        folium.PolyLine(points, color="#1b3b6f", weight=3, opacity=0.4, tooltip="Trajeto Continental Principal").add_to(m)

        # Linha animada "AntPath" simulando o fluxo da expedição
        AntPath(
            points,
            color="#218380",
            weight=5,
            opacity=0.85,
            delay=900,
            dash_array=[15, 25],
            pulse_color="#ffffff",
            tooltip="Fluxo da Expedição · São Paulo ➔ Ushuaia ➔ Puerto Williams"
        ).add_to(m)

        # Marcadores para cada parada com ícones customizados
        for stop in route_data:
            icon_name = "info-sign"
            icon_color = "blue"
            prefix_val = "glyphicon"

            if stop['type'] == "Start":
                icon_name, icon_color = "play", "green"
            elif "End" in stop['type']:
                icon_name, icon_color = "flag", "red"
            elif "Tesla" in stop['type'] or "Grid" in stop['type']:
                icon_name, icon_color = "flash", "cadetblue"
            elif "Gas" in stop['type'] or "Fuel" in stop['type']:
                icon_name, icon_color = "gas-pump", "orange"
                prefix_val = "fa"
            elif stop['type'] == "Border":
                icon_name, icon_color = "random", "purple"
                prefix_val = "fa"

            popup_html = f"""
            <div style="font-family: 'Plus Jakarta Sans'; width: 220px; padding: 5px;">
                <h4 style="margin: 0 0 5px 0; color: #1b3b6f; font-family: 'Playfair Display';">{stop['name']}</h4>
                <p style="margin: 3px 0; font-size: 12px;"><b>País:</b> {stop['country']}</p>
                <p style="margin: 3px 0; font-size: 12px;"><b>Distância:</b> {stop['distance_from_start']}</p>
                <p style="margin: 3px 0; font-size: 12px;"><b>Infra:</b> {stop['charging_infra']}</p>
                <p style="margin: 3px 0; font-size: 12px; color: #218380;"><i>{stop['highlights']}</i></p>
            </div>
            """

            folium.Marker(
                [stop['lat'], stop['lon']],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"#{stop['id']} - {stop['name']}",
                icon=folium.Icon(color=icon_color, icon=icon_name, prefix=prefix_val)
            ).add_to(m)

        st_folium(m, width=1250, height=600)
    else:
        st.error("Erro ao carregar dados geográficos da rota.")

# ── SEÇÃO 3: DIÁRIO DE BORDO & PARADAS ──────────────────────
elif nav_choice == T["nav_stops"]:
    st.markdown(f'<div class="section-label">{T["details_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["details_title"]}</div>', unsafe_allow_html=True)

    selected_stop_name = st.selectbox(
        "Selecione uma parada da expedição para visualizar o dossiê completo:",
        options=[s['name'] for s in route_data]
    )

    stop_info = next((s for s in route_data if s['name'] == selected_stop_name), route_data[0])

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown(f"""
        <div class="info-card">
            <span style="background: #218380; color: white; padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.75rem;">PARADA #{stop_info['id']} · {stop_info['country']}</span>
            <h2 style="font-family: 'Playfair Display'; color: #1b3b6f; margin-top: 1rem; margin-bottom: 0.5rem;">{stop_info['name']}</h2>
            <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem;">Coordenadas: {stop_info['lat']}, {stop_info['lon']} | Elevação: {stop_info['elevation']}</p>
            
            <p><b>📏 Distância acumulada:</b> {stop_info['distance_from_start']}</p>
            <p><b>⚡ Infraestrutura Elétrica:</b> {stop_info['charging_infra']}</p>
            <p><b>⛽ Infraestrutura de Combustível:</b> {stop_info['gas_infra']}</p>
            <p><b>🌡️ Clima (Verão / Inverno):</b> {stop_info['climate_summer']} / {stop_info['climate_winter']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #ffb703;">
            <h3 style="font-family: 'Playfair Display'; color: #1b3b6f; margin-top: 0; margin-bottom: 1rem;">Destaques Científicos & Logísticos</h3>
            <p style="line-height: 1.7; font-size: 0.95rem; color: #1d3557; margin-bottom: 1.2rem;">
            {stop_info['highlights']}
            </p>
            <h4 style="font-family: 'Playfair Display'; color: #1b3b6f; margin-bottom: 0.5rem;">Orientações de Trânsito & Fronteira</h4>
            <p style="line-height: 1.6; font-size: 0.92rem; color: #64748b;">
            {stop_info['logistics']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Tabela Geral de Paradas da Expedição")
    df_stops = pd.DataFrame(route_data)
    st.dataframe(df_stops[['id', 'name', 'country', 'distance_from_start', 'elevation', 'type']], use_container_width=True)

# ── SEÇÃO 4: FICHA TÉCNICA & CUSTOS ─────────────────────────
elif nav_choice == T["nav_specs"]:
    st.markdown(f'<div class="section-label">{T["specs_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["specs_title"]}</div>', unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("""
        <div class="info-card" style="border-left-color: #2a9d8f;">
            <h3 style="font-family: 'Playfair Display'; color: #1b3b6f;">🔋 Tesla Model 3 Long Range (2024)</h3>
            <p><b>Autonomia Estimada:</b> ~550 km por carga completa</p>
            <p><b>Capacidade da Bateria:</b> 78.1 kWh (Lítio-íon)</p>
            <p><b>Tracionamento:</b> Dual Motor AWD (Integral)</p>
            <p><b>Infraestrutura de Apoio:</b> Supercharger Tesla, Redes UTE (Uruguai), Eletropostos YPF/Privados</p>
            <p><b>Custo Estimado da Viagem:</b> <b>~$460 USD</b> (Recargas em redes públicas e residenciais/hoteleiras)</p>
        </div>
        """, unsafe_allow_html=True)

    with col_v2:
        st.markdown("""
        <div class="info-card" style="border-left-color: #e63946;">
            <h3 style="font-family: 'Playfair Display'; color: #1b3b6f;">⛽ Hyundai Tucson 2.0 (2024)</h3>
            <p><b>Autonomia Estimada:</b> ~750 km com tanque cheio</p>
            <p><b>Capacidade do Tanque:</b> 54 Litros (Gasolina)</p>
            <p><b>Consumo Médio Rodoviário:</b> ~12.5 km/L</p>
            <p><b>Infraestrutura de Apoio:</b> Rede consolidada de postos (Ipiranga, Petrobras, Ancap, YPF, Copec)</p>
            <p><b>Custo Estimado da Viagem:</b> <b>~$1.250 USD</b> (Combustível fóssil ao longo dos 4 países)</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Gráfico Comparativo de Custos Estimados (USD)")

    fig = go.Figure(data=[
        go.Bar(name='Tesla Model 3 (Elétrico)', x=['São Paulo ➔ Ushuaia & Puerto Williams'], y=[460], marker_color='#2a9d8f'),
        go.Bar(name='Hyundai Tucson (Combustão)', x=['São Paulo ➔ Ushuaia & Puerto Williams'], y=[1250], marker_color='#e63946')
    ])
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Custo Total Estimado (USD)",
        font=dict(family='Plus Jakarta Sans', size=13),
        margin=dict(t=20, b=20),
        legend=dict(orientation="h", y=1.1, x=0.2)
    )
    st.plotly_chart(fig, use_container_width=True)

# ── SEÇÃO 5: METODOLOGIA & CONTEXTO ─────────────────────────
elif nav_choice == T["nav_tech"]:
    st.markdown(f'<div class="section-label">{T["tech_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Metodologia Científica e Stack Tecnológica</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3 style="font-family: 'Playfair Display'; color: #1b3b6f;">📋 Nota Metodológica Oficial</h3>
        <p style="line-height: 1.7; color: #334155;">
        Esta simulação é o resultado de pesquisa independente de campo aplicada ao setor automotivo e energético (2024–2026), unindo geoprocessamento, análise de eficiência energética e logística transnacional. Os custos apresentados são estimativas baseadas em fichas técnicas oficiais dos veículos, preços médios de eletricidade e combustíveis fósseis nos quatro países cruzados (Brasil, Uruguai, Argentina e Chile), e distâncias geodésicas reais mapeadas ponto a ponto.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        <div class="info-card" style="border-left-color: #1b3b6f;">
            <h4 style="font-family: 'Playfair Display'; color: #1b3b6f;">🛠️ Stack Tecnológica</h4>
            <ul>
                <li><b>Python 3.11 & Streamlit:</b> Arquitetura do painel e reatividade.</li>
                <li><b>Folium & Streamlit-Folium:</b> Mapeamento geoespacial e rotas vetoriais.</li>
                <li><b>Plotly:</b> Visualização interativa de dados financeiros e energéticos.</li>
                <li><b>Pandas & JSON:</b> Estruturação e manipulação do diário de bordo.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown("""
        <div class="info-card" style="border-left-color: #ffb703;">
            <h4 style="font-family: 'Playfair Display'; color: #1b3b6f;">🌐 Contexto Geopolítico</h4>
            <p style="font-size: 0.9rem; color: #334155; line-height: 1.6;">
            A rota explora o debate sul-americano sobre qual cidade representa o verdadeiro fim do mundo continental: <b>Ushuaia</b> (Argentina, na Terra do Fogo) ou <b>Puerto Williams</b> (Chile, na Ilha Navarino, a cidade mais austral do planeta).
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# RODAPÉ INSTITUCIONAL
# ============================================================
st.markdown(f"""
<div class="footer-wrap">
    <div class="footer-title">{T['footer_title']}</div>
    <p style="margin: 0.5rem 0; font-size: 0.92rem; line-height: 1.6;">{T['footer_desc']}</p>
    <p style="margin: 1.2rem 0 0.5rem; font-size: 0.88rem; opacity: 0.8;">
    {T['footer_links']} &nbsp;|&nbsp; 
    🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color: #ffb703; text-decoration: none;">Portfólio Ambiental</a> &nbsp;|&nbsp; 
    🐙 <a href="https://github.com/amaurialmeida/road-to-patagonia" style="color: #ffb703; text-decoration: none;">Repositório GitHub</a>
    </p>
    <p style="font-size: 0.78rem; opacity: 0.5; margin-top: 1rem;">© 2024–2026 · Expedição Patagônia · Pesquisa de Campo Transnacional</p>
</div>
""", unsafe_allow_html=True)
