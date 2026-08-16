import streamlit as st
import urllib.parse

st.set_page_config(page_title="Gerador de Etiquetas", page_icon="🏷️", layout="wide")

# Lista de camisas cadastradas
catalog = [
    {"id": 1, "titulo": "Operário MS Home #9", "marca": "Champs", "tamanho": "M", "preco": "R$ 60,00", "link_br": "https://www.sofutebolbrasil.com/produto/569/camisa-oficial-operario-ms", "link_int": None},
    {"id": 2, "titulo": "Juventus Mooca Azul 459 Anos", "marca": "Superbolla", "tamanho": "M", "preco": "R$ 120,00", "link_br": "https://www.mercadolivre.com.br/camisa-juventus-da-mooca-especial-2015-azul/up/MLBU1726959953", "link_int": None},
    {"id": 3, "titulo": "Juventus 2007/2008 Scudetto", "marca": "Nike", "tamanho": "M", "preco": "R$ 150,00", "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035", "link_int": None},
    {"id": 4, "titulo": "Juventus 2015/2016 Rosa", "marca": "Adidas", "tamanho": "G", "preco": "R$ 350,00", "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035", "link_int": "https://www.ebay.com/itm/389084099014"},
    {"id": 5, "titulo": "Jaqueta Juventus 2009/2010 Treino", "marca": "Nike", "tamanho": "G", "preco": "R$ 299,00", "link_br": None, "link_int": "https://www.ebay.com/itm/168192283231"},
    {"id": 6, "titulo": "São Paulo 2007 Adriano #10", "marca": "Reebok", "tamanho": "G", "preco": "R$ 199,00", "link_br": "https://memoriasdoesporteoficial.com.br/produto/camisa-sao-paulo-reebok-2007-tricolor/", "link_int": "https://www.ebay.com/itm/175121591014"},
    {"id": 7, "titulo": "São Paulo 1997 Denilson #11", "marca": "Adidas", "tamanho": "G", "preco": "R$ 450,00", "link_br": "https://pe.olx.com.br/grande-recife/esportes-e-lazer/roupas-esportivas/camisa-sao-paulo-adidas-1997-datacontrol-1508643853", "link_int": None},
    {"id": 8, "titulo": "Blusa Agasalho SPFC 1993", "marca": "Del-Lini Tricot", "tamanho": "G", "preco": "R$ 600,00", "link_br": None, "link_int": None},
    {"id": 9, "titulo": "Liverpool 2006/2007 Home", "marca": "Adidas", "tamanho": "G", "preco": "R$ 350,00", "link_br": "https://www.mercadolivre.com.br/camisa-liverpool-2005-2006-adidas-teamgeist-original-epoca/up/MLBU3358810718", "link_int": "https://www.ebay.com/itm/197498583510"},
    {"id": 10, "titulo": "Sampdoria 2004/2005 ERG Azul", "marca": "Kappa", "tamanho": "G", "preco": "R$ 320,00", "link_br": None, "link_int": "https://www.ebay.com/itm/267415041067"},
    {"id": 11, "titulo": "Panathinaikos 2010/2011 Home", "marca": "Adidas", "tamanho": "M", "preco": "R$ 260,00", "link_br": "https://www.enjoei.com.br/p/camisa-panathinaikos-2010-11-home-original-143625516", "link_int": "https://www.ebay.com/itm/389490870451"},
    {"id": 12, "titulo": "Kaiserslautern Mobil Gel", "marca": "Nike", "tamanho": "G", "preco": "R$ 260,00", "link_br": None, "link_int": "https://www.ebay.it/itm/286873950722"},
    {"id": 13, "titulo": "Itália Copa 2014 Pirlo #21", "marca": "Puma", "tamanho": "M", "preco": "R$ 300,00", "link_br": "https://www.futclassics.com.br/product-page/italia-2014-home-m-5-6", "link_int": "https://www.ebay.com/itm/128011480704"},
    {"id": 14, "titulo": "Itália Campione Del Mondo", "marca": "Puma", "tamanho": "G", "preco": "R$ 240,00", "link_br": None, "link_int": "https://www.ebay.com/itm/226370114363"},
    {"id": 15, "titulo": "Inglaterra 2007 Home", "marca": "Umbro", "tamanho": "M", "preco": "R$ 280,00", "link_br": "https://www.futclassics.com.br/product-page/inglaterra-2007-home-11", "link_int": None},
    {"id": 16, "titulo": "Ibiza Eivissa 2009 Vermelha", "marca": "Champs", "tamanho": "M", "preco": "R$ 150,00", "link_br": "https://brechodofutebol.com/products/ibiza-eivissa-2009-segunda-camisa-tam-p", "link_int": None}
]

def get_qr_url(link):
    """Gera a URL da imagem do QR Code usando QuickChart API"""
    if not link:
        return None
    encoded = urllib.parse.quote(link)
    return f"https://quickchart.io/qr?text={encoded}&size=150"

# CSS para controlar o layout na tela e na impressão
st.markdown("""
<style>
/* Estilos para a tela */
.label-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: flex-start;
}

.shirt-card {
    border: 2px dashed #333;
    border-radius: 8px;
    padding: 10px;
    width: 320px;
    background-color: #ffffff;
    color: #000000;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    page-break-inside: avoid;
}

.shirt-header {
    font-size: 14px;
    font-weight: bold;
    border-bottom: 1px solid #ccc;
    padding-bottom: 4px;
    margin-bottom: 6px;
    text-transform: uppercase;
}

.shirt-details {
    font-size: 12px;
    margin-bottom: 6px;
}

.price-tag {
    font-size: 16px;
    font-weight: bold;
    color: #2e7d32;
    margin-top: 4px;
}

.qr-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 6px;
    border-top: 1px solid #eee;
    padding-top: 6px;
}

.qr-box {
    text-align: center;
    font-size: 10px;
    font-weight: bold;
}

.qr-box img {
    width: 70px;
    height: 70px;
    display: block;
    margin: 0 auto;
}

/* Ocultar elementos do Streamlit ao imprimir */
@media print {
    header, footer, .stButton, .no-print, [data-testid="stSidebar"] {
        display: none !important;
    }
    body {
        background: white !important;
    }
    .main .block-container {
        padding: 0 !important;
    }
    .label-grid {
        gap: 8px;
    }
    .shirt-card {
        border: 1px dashed #000 !important;
        box-shadow: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("🏷️ Gerador de Etiquetas para Embalagens")
st.write("Clique no botão abaixo para abrir a janela de impressão. As etiquetas já estão formatadas com bordas pontilhadas para corte!")

# Botão de impressão (ativa o print do próprio navegador)
st.components.v1.html("""
    <button onclick="window.print()" style="
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        width: 100%;
    ">🖨️ Imprimir Todas as Etiquetas (PDF / Impressora)</button>
""", height=60)

st.markdown("---")

# Monta o HTML das etiquetas em grade
html_content = '<div class="label-grid">'

for item in catalog:
    qr_br = get_qr_url(item['link_br'])
    qr_int = get_qr_url(item['link_int'])
    
    qr_br_html = f'<div class="qr-box">🇧🇷 BR<img src="{qr_br}"/></div>' if qr_br else ''
    qr_int_html = f'<div class="qr-box">🌎 INT<img src="{qr_int}"/></div>' if qr_int else ''

    html_content += f"""
    <div class="shirt-card">
        <div class="shirt-header">#{item['id']} {item['titulo']}</div>
        <div class="shirt-details">
            <b>Marca:</b> {item['marca']} | <b>Tam:</b> {item['tamanho']}<br>
            <div class="price-tag">Preço: {item['preco']}</div>
        </div>
        <div class="qr-container">
            {qr_br_html}
            {qr_int_html}
        </div>
    </div>
    """

html_content += '</div>'

# Exibe na página
st.markdown(html_content, unsafe_allow_html=True)
