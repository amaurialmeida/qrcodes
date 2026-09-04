import streamlit as st
import pandas as pd
import urllib.parse
import io
import qrcode
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Acervo & Catálogo de Colecionáveis ⚽📚🪙",
    layout="wide",
    page_icon="⚽"
)

# --- NÚMERO DO WHATSAPP DO AMAURI ---
WHATSAPP_NUMERO = "5511942762908"

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
st.markdown("""
    <style>
    .price-tag {
        font-size: 1.4rem;
        font-weight: bold;
        color: #2e7d32;
    }
    .old-price {
        text-decoration: line-through;
        color: #757575;
        font-size: 0.9rem;
        margin-left: 8px;
    }
    .badge-barateou {
        background-color: #ffeb3b;
        color: #000;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 5px;
    }
    .badge-vendido {
        background-color: #d32f2f;
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
    }
    .badge-livro {
        background-color: #0288d1;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 5px;
    }
    .shirt-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 5px;
    }
    .shirt-sub {
        color: #616161;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# --- FUNÇÃO GERADORA DE QR CODE ---
def gerar_qr_code(url: str):
    """Gera uma imagem PIL de QR Code a partir de uma URL fornecida."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


# --- BASE DE DADOS COMPLETA DO ACERVO ---
@st.cache_data
def carregar_dados():
    RAW_BASE = "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/verso"
    
    data = [
        # --- CAMISAS E VESTUÁRIO ---
        {
            "id": 1,
            "titulo": "Camisa Operário Mato Grosso do Sul / MS Home #9, Champs",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "Mato Grosso do Sul - Operário MS",
            "marca": "Champs",
            "tamanho": "G",
            "preco_original": 160.0,
            "preco_atual": 60.0,
            "tag": "barateou",
            "vendido": False,
            "link_br": "https://www.sofutebolbrasil.com/produto/569/camisa-oficial-operario-ms",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/operario-frente.jpeg",
                f"{RAW_BASE}/operario-verso.jpeg"
            ]
        },
        {
            "id": 2,
            "titulo": "Camisa Juventus da Mooca Azul Aniversário 459 Anos #9, Superbolla",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "São Paulo - Mooca",
            "marca": "Superbolla",
            "tamanho": "G",
            "preco_original": 270.0,
            "preco_atual": 120.0,
            "tag": "barateou",
            "vendido": False,
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-da-mooca-especial-2015-azul/up/MLBU1726959953?pdp_filters=item_id%3AMLB3312171725#origin=share&sid=share&wid=MLB3312171725&action=copy",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/juve-azul-frente.jpeg",
                f"{RAW_BASE}/juve-azul-verso.jpeg"
            ]
        },
        {
            "id": 3,
            "titulo": "Camisa Juventus 2007/2008, Nike, New Holland Fiat Group, Scudetto",
            "categoria": "Camisa de Futebol",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "Nike",
            "tamanho": "M",
            "preco_original": 220.0,
            "preco_atual": 150.0,
            "tag": "barateou",
            "vendido": False,
            "link_br": "https://www.instagram.com/p/DPh6VfWjJOq/?img_index=1",
            "link_int": "https://www.enjoei.com.br/p/camisa-juventus-italia-nike-2007-futebol-esportiva-colecionador-original-da-epoca-89041407?srsltid=AfmBOoq2PXrUMeAKmRZAicuJSuu5Suo7r9skWAAhPDVa2pV1KiKiehkn&vid=17d08c25-0b1d-4732-a7bf-093bad985a05",
            "fotos": [
                f"{RAW_BASE}/juve-frente.jpeg",
                f"{RAW_BASE}/juve-verso.jpeg"
            ]
        },
        {
            "id": 4,
            "titulo": "Camisa Juventus 2015/2016 Rosa Jeep, Adidas Climacool",
            "categoria": "Camisa de Futebol",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "Adidas",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 350.0,
            "tag": "barateou",
            "vendido": True,
            "link_br": "https://www.mercadolivre.com.br/camisa-juventus-201516/up/MLBU3253537035#polycard_client=search-web-mobile&be_origin=backend&overlay_label=not_apply&search_layout=stack&position=2&type=product&tracking_id=7b617228-c264-44e0-8502-4d3938d259a5&wid=MLB4104645169&sid=search",
            "link_int": "https://www.ebay.com/itm/389084099014",
            "fotos": [
                f"{RAW_BASE}/juve-rosa-frente.jpeg",
                f"{RAW_BASE}/juve-rosa-verso.jpeg",
                f"{RAW_BASE}/juve-rosa-detalhes.jpeg"
            ]
        },
        {
            "id": 5,
            "titulo": "Jaqueta Juventus 2009/2010 Treino, Nike",
            "categoria": "Camisa de Futebol",
            "pais": "Itália",
            "time_regiao": "Turim - Juventus",
            "marca": "Nike",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 299.0,
            "tag": "raridade",
            "vendido": True,
            "link_br": None,
            "link_int": "https://www.ebay.com/itm/168192283231",
            "fotos": [
                f"{RAW_BASE}/blusajuve-frente.jpeg",
                f"{RAW_BASE}/blusajuve-verso.jpeg",
                f"{RAW_BASE}/blusajuve-detalhes.jpeg"
            ]
        },
        {
            "id": 6,
            "titulo": "Camisa São Paulo, Reebok 2007, Adriano Imperador #10, LG Fast, Patch Campeão",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "Reebok",
            "tamanho": "G",
            "preco_original": 250.0,
            "preco_atual": 199.0,
            "tag": "barateou",
            "vendido": False,
            "link_br": "https://memoriasdoesporteoficial.com.br/produto/camisa-sao-paulo-reebok-2007-tricolor/",
            "link_int": "https://www.ebay.com/itm/175121591014",
            "fotos": [
                f"{RAW_BASE}/spfc2-frente.jpeg",
                f"{RAW_BASE}/spfc2-verso.jpeg",
                f"{RAW_BASE}/spfc2-detalhes.jpeg"
            ]
        },
        {
            "id": 7,
            "titulo": "Camisa São Paulo, Adidas 1997, Denilson #11, Data Control",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "Adidas",
            "tamanho": "G",
            "preco_original": 500.0,
            "preco_atual": 450.0,
            "tag": "barateou",
            "vendido": True,
            "link_br": "https://pe.olx.com.br/grande-recife/esportes-e-lazer/roupas-esportivas/camisa-sao-paulo-adidas-1997-datacontrol-1508643853?utm_medium=shared_link&utm_source=direct",
            "link_int": None,
            "fotos": [
                "https://raw.githubusercontent.com/amaurialmeida/tshirts/main/assets/frente/frente%201.jpeg",
                f"{RAW_BASE}/detalhes/verso1.jpeg",
                f"{RAW_BASE}/detalhe1.jpeg"
            ]
        },
        {
            "id": 8,
            "titulo": "Blusa Agasalho São Paulo, Del-Lini Tricot 1993, Relíquia Histórica",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "Del-Lini Tricot",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 600.0,
            "tag": "relíquia",
            "vendido": False,
            "link_br": None,
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/blusasp-frente.jpeg",
                f"{RAW_BASE}/blusasp-verso.jpeg"
            ]
        },
        {
            "id": 9,
            "titulo": "Camisa Liverpool 2006/2007 Home, Adidas, Carlsberg, Item de Colecionador",
            "categoria": "Camisa de Futebol",
            "pais": "Inglaterra",
            "time_regiao": "Liverpool",
            "marca": "Adidas",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 350.0,
            "tag": "raridade",
            "vendido": True,
            "link_br": "https://www.mercadolivre.com.br/camisa-liverpool-2005-2006-adidas-teamgeist-original-epoca/up/MLBU3358810718",
            "link_int": "https://www.ebay.com/itm/197498583510",
            "fotos": [
                f"{RAW_BASE}/liverpool-frente.jpeg",
                f"{RAW_BASE}/liverpool-verso.jpeg",
                f"{RAW_BASE}/liverpool-detalhes21.jpeg"
            ]
        },
        {
            "id": 10,
            "titulo": "Camisa Sampdoria ERG Itália Azul, Asics",
            "categoria": "Camisa de Futebol",
            "pais": "Itália",
            "time_regiao": "Sampdoria",
            "marca": "Asics",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 320.0,
            "tag": "raridade",
            "vendido": True,
            "link_br": None,
            "link_int": "https://www.ebay.com/itm/267415041067",
            "fotos": [
                f"{RAW_BASE}/samp-frente.jpeg",
                f"{RAW_BASE}/samp-verso.jpeg",
                f"{RAW_BASE}/samp-detalhes.jpeg"
            ]
        },
        {
            "id": 11,
            "titulo": "Camisa Panathinaikos 2010/2011 Home Cosmote, Adidas",
            "categoria": "Camisa de Futebol",
            "pais": "Grécia",
            "time_regiao": "Atenas",
            "marca": "Adidas",
            "tamanho": "M",
            "preco_original": 280.0,
            "preco_atual": 260.0,
            "tag": "importada",
            "vendido": False,
            "link_br": "https://www.enjoei.com.br/p/camisa-panathinaikos-2010-11-home-original-143625516",
            "link_int": "https://www.ebay.com/itm/389490870451",
            "fotos": [
                f"{RAW_BASE}/panathinaikos-frente.jpeg",
                f"{RAW_BASE}/panathinaikos-verso.jpeg",
                f"{RAW_BASE}/panathinaikos-detalhes.jpeg",
                f"{RAW_BASE}/panathinaikos-detalhes2.jpeg"
            ]
        },
        {
            "id": 12,
            "titulo": "Camisa Kaiserslautern Mobil Gel Alemanha, Nike",
            "categoria": "Camisa de Futebol",
            "pais": "Alemanha",
            "time_regiao": "Kaiserslautern",
            "marca": "Nike",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 260.0,
            "tag": "raridade",
            "vendido": False,
            "link_br": None,
            "link_int": "https://www.ebay.it/itm/286873950722",
            "fotos": [
                f"{RAW_BASE}/kaiser-frente.jpeg",
                f"{RAW_BASE}/kaiser-verso.jpeg",
                f"{RAW_BASE}/kaiser-detalhes.jpeg"
            ]
        },
        {
            "id": 13,
            "titulo": "Camisa Itália Copa do Mundo FIFA 2014 Home #21, Pirlo, Puma",
            "categoria": "Camisa de Futebol",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "Puma",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 300.0,
            "tag": "barateou",
            "vendido": False,
            "link_br": "https://www.futclassics.com.br/product-page/italia-2014-home-m-5-6",
            "link_int": "https://www.ebay.com/itm/128011480704",
            "fotos": [
                f"{RAW_BASE}/italia-frente.jpeg",
                f"{RAW_BASE}/italia-verso.jpeg"
            ]
        },
        {
            "id": 14,
            "titulo": "Camisa Itália Campione Del Mondo Comemorativa, Puma",
            "categoria": "Camisa de Futebol",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "Puma",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 240.0,
            "tag": "especial",
            "vendido": False,
            "link_br": None,
            "link_int": "https://www.ebay.com/itm/226370114363",
            "fotos": [
                f"{RAW_BASE}/italiacampione-frente.jpeg",
                f"{RAW_BASE}/italiacampione-verso.jpeg",
                f"{RAW_BASE}/italiacampione-detalhes.jpeg"
            ]
        },
        {
            "id": 15,
            "titulo": "Camisa Seleção Inglaterra 2007 Home, Umbro",
            "categoria": "Camisa de Futebol",
            "pais": "Inglaterra",
            "time_regiao": "Seleção Inglesa",
            "marca": "Umbro",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 280.0,
            "tag": "barateou",
            "vendido": False,
            "link_br": "https://www.futclassics.com.br/product-page/inglaterra-2007-home-11",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/inglaterra-frente.jpeg",
                f"{RAW_BASE}/inglaterra-detalhes.jpeg"
            ]
        },
        {
            "id": 16,
            "titulo": "Camisa Ibiza Eivissa 2009 Camisa 1 Vermelha, Champs",
            "categoria": "Camisa de Futebol",
            "pais": "Espanha",
            "time_regiao": "Ibiza",
            "marca": "Champs",
            "tamanho": "M",
            "preco_original": 180.0,
            "preco_atual": 150.0,
            "tag": "importada",
            "vendido": True,
            "link_br": "https://brechodofutebol.com/products/ibiza-eivissa-2009-segunda-camisa-tam-p?srsltid=AfmBOooaZ5LOym7C_3sq2WOdXIBHKsP21kuJ4_aKrlHqjoTehlDttDkw",
            "link_int": None,
            "fotos": [
                f"{RAW_BASE}/ibiza-frente.jpeg",
                f"{RAW_BASE}/ibiza-verso.jpeg",
                f"{RAW_BASE}/ibiza-detalhes1.jpeg",
                f"{RAW_BASE}/ibiza-detalhes21.jpeg"
            ]
        },
        {
            "id": 17,
            "titulo": "Camisa Seleção Itália Rugby 2007 - 2009, Kappa",
            "categoria": "Camisa de Futebol",
            "pais": "Itália",
            "time_regiao": "Seleção Italiana",
            "marca": "Kappa",
            "tamanho": "G",
            "preco_original": 0.0,
            "preco_atual": 150.0,
            "tag": "especial",
            "vendido": False,
            "link_br": "https://www.enjoei.com.br/p/camisa-selecao-italia-rugby-111153794",
            "link_int": "https://www.ebay.co.uk/itm/282395881167",
            "fotos": [
                f"{RAW_BASE}/italiarugby-frente.jpeg",
                f"{RAW_BASE}/italiarugby-verso.jpeg"
            ]
        },
        {
            "id": 18,
            "titulo": "Camisa Polo Seleção Brasileira 1962, Guaraná Antarctica",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "Seleção Brasileira",
            "marca": "Guaraná Antarctica",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 50.0,
            "tag": "retrô",
            "vendido": False,
            "link_br": "https://www.enjoei.com.br/p/camisa-polo-brasil-62-colecao-guarana-antarctica-tamanho-m-135941790?srsltid=AfmBOorjWPUoE-yVo4-31kkxgQZyCcfCP5cmhF05A9IGxsCp-Q6kCblW&vid=64f8d94e-6832-4c1a-9f71-1ef6dfffe246",
            "link_int": None,
            "fotos": ["https://via.placeholder.com/400x500?text=Brasil+1962"]
        },
        {
            "id": 19,
            "titulo": "Regata Atlético Mineiro, ABC Torcida Organizada",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "Minas Gerais - Galo",
            "marca": "ABC - Torcida Organizada",
            "tamanho": "M",
            "preco_original": 0.0,
            "preco_atual": 30.0,
            "tag": "especial",
            "vendido": False,
            "link_br": None,
            "link_int": None,
            "fotos": ["https://via.placeholder.com/400x500?text=Atletico+Mineiro"]
        },
        {
            "id": 20,
            "titulo": "Camisa São Paulo F.C. Algodão Morumbi, Reebok",
            "categoria": "Camisa de Futebol",
            "pais": "Brasil",
            "time_regiao": "São Paulo",
            "marca": "Reebok",
            "tamanho": "P",
            "preco_original": 0.0,
            "preco_atual": 40.0,
            "tag": "especial",
            "vendido": False,
            "link_br": None,
            "link_int": None,
            "fotos": ["https://via.placeholder.com/400x500?text=SPFC+Morumbi"]
        },
        {
            "id": 21,
            "titulo": "Camisa Packers Green Bay Futebol Americano, Jawill Davis #11",
            "categoria": "Camisa de Futebol",
            "pais": "EUA",
            "time_regiao": "NFL - Green Bay Packers",
            "marca": "A4",
            "tamanho": "P",
            "preco_original": 0.0,
            "preco_atual": 40.0,
            "tag": "importada",
            "vendido": False,
            "link_br": None,
            "link_int": None,
            "fotos": ["https://via.placeholder.com/400x500?text=Green+Bay+Packers"]
        },

        # --- MOEDAS E NUMISMÁTICA ---
        {
            "id": 22,
            "titulo": "Lote 23 Moedas 1 Real: Canoagem (2), Rugby (1), Golfe (1), Voleibol (1), Futebol (2), Natação (2), Judô (2), Vela (1), Salto com Vara (3), Mascote Tom (3), Paratriatlo (1), Atletismo Paralímpico (3), Banco Central 40 Anos (1)",
            "categoria": "Moedas / Numismática",
            "pais": "Brasil",
            "time_regiao": "Numismática / Coleção Olimpíadas e BC",
            "marca": "Banco Central / Casa da Moeda",
            "tamanho": "23 Peças",
            "preco_original": 206.0,
            "preco_atual": 180.0,
            "tag": "colecionador",
            "vendido": False,
            "link_br": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-futebol___642139-SIT.html",
            "link_int": "https://qrcodes-rguxkngmtumghgrvux5mzj.streamlit.app/",
            "fotos": ["https://via.placeholder.com/400x500?text=Lote+Moedas+1+Real"]
        },

        # --- LIVROS E PUBLICAÇÕES DE FUTEBOL ---
        {
            "id": 23,
            "titulo": "O Grande Livro dos Mundiais de Copa (Edição Única, 2006, Completo e na Caixa)",
            "categoria": "Livros / Publicações",
            "pais": "Internacional / Brasil",
            "time_regiao": "Copas do Mundo",
            "marca": "Editora Folio / Keir Radnedge",
            "tamanho": "Edição Única (2006)",
            "preco_original": 0.0,
            "preco_atual": 120.0,
            "tag": "livro",
            "vendido": False,
            "link_br": "https://shopee.com.br/O-Grande-Livro-dos-Mundiais-de-Copa-(Edi%C3%A7%C3%A3o-%C3%9Anica-2006-Completo-e-na-Caixa)-i.732870411.22494759672",
            "link_int": "https://higinocultural.com.br/produto/o-grande-livro-dos-mundiais-keir-radnedge-com-mark-bushell/",
            "fotos": ["https://via.placeholder.com/400x500?text=Grande+Livro+Mundiais"]
        },
        {
            "id": 24,
            "titulo": "Livro TODAS AS COPAS DE 1930 A 2002",
            "categoria": "Livros / Publicações",
            "pais": "Brasil",
            "time_regiao": "Copas do Mundo",
            "marca": "Jornal o LANCE! / Marcos Augusto Gonçalves",
            "tamanho": "Edição Única (2002)",
            "preco_original": 0.0,
            "preco_atual": 40.0,
            "tag": "livro",
            "vendido": False,
            "link_br": "https://shopee.com.br/TODAS-AS-COPAS-DE-1930-A-2002-i.398672555.11829321560",
            "link_int": "https://www.estantevirtual.com.br/livro/todas-as-copas-de-1930-a-2002-RH2-6673-000",
            "fotos": ["https://via.placeholder.com/400x500?text=Todas+as+Copas+1930-2002"]
        },
        {
            "id": 25,
            "titulo": "Livro Recordes do futebol mundial 2010",
            "categoria": "Livros / Publicações",
            "pais": "Brasil",
            "time_regiao": "Estatísticas / Futebol Mundial",
            "marca": "Ciranda Cultural / Keir Radnedge",
            "tamanho": "Edição 2010",
            "preco_original": 0.0,
            "preco_atual": 25.0,
            "tag": "livro",
            "vendido": False,
            "link_br": "https://shopee.com.br/product/381527624/18699858047?gads_t_sig=gqRjZGVrxHCFomtpsTE0MjUxOnRzc19zZGtfa2V5omt20QACpGFsZ2_SAAAAZKNkZWvAomN0xEAAAAAMCDZ1QISG3Y9eQ8yPVgAOiad7g2PqyaqkWO_9nGG8rv2GeSvTKVy0YH9Uq_tAMSkaB8ROm0FmD1_y4Fc6qmNpcGhlcnRleHTEcgAAAAwLbuIEzpgHxE82qu1p7MYIezDhOYSbZG8BqZcAcXlsNDlczv1nTnPeZbulESCCvK7l9MANdX3VIU0kZVZQcWLDg3m6T3-VhJzoZLUsPCIw80c7AZnG1M6sCo3EeXJ0KFu03I3m7sMRzRVac_kcAg",
            "link_int": "https://www.estantevirtual.com.br/livro/livro-recordes-do-futebol-mundial-2010-JP6-3795-000?campaign=ev",
            "fotos": ["https://via.placeholder.com/400x500?text=Recordes+Futebol+2010"]
        },
        {
            "id": 26,
            "titulo": "Kit Atualização Copa do Mundo 2014 Panini",
            "categoria": "Livros / Publicações",
            "pais": "Brasil",
            "time_regiao": "Copa do Mundo 2014",
            "marca": "Panini",
            "tamanho": "Edição 2014",
            "preco_original": 0.0,
            "preco_atual": 0.0,
            "tag": "livro",
            "vendido": False,
            "link_br": "https://sp.olx.com.br/sao-paulo-e-regiao/antiguidades/kit-atualizacao-copa-2014-panini-1528325551",
            "link_int": None,
            "fotos": ["https://via.placeholder.com/400x500?text=Kit+Panini+Copa+2014"]
        }
    ]
    return pd.DataFrame(data)


df_acervo = carregar_dados()

# --- LISTA DE MOEDAS COM LINKS DA NUMISMÁTICA VIEIRA ---
MOEDAS_LINKS = [
    {
        "nome": "Moeda Futebol Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-futebol___642139-SIT.html"
    },
    {
        "nome": "Moeda Canoagem Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-paracanoagem___602017-SIT.html"
    },
    {
        "nome": "Moeda Golfe Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-golfe___566398-SIT.html"
    },
    {
        "nome": "Moeda Voleibol Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-voleibol___642141-SIT.html"
    },
    {
        "nome": "Moeda Natação Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-natacao___566396-SIT.html"
    },
    {
        "nome": "Moeda Judô Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-judo___642140-SIT.html"
    },
    {
        "nome": "Moeda Vela Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-vela___602019-SIT.html"
    },
    {
        "nome": "Moeda Atletismo Salto com Vara Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-atletismo___566394-SIT.html"
    },
    {
        "nome": "Moeda Mascote TOM Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-mascote-paralimpico-tom___711998-SIT.html"
    },
    {
        "nome": "Moeda Paratriatlo Olimpíada 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-olimpicos-rio-2016-paratriatlo___566399-SIT.html"
    },
    {
        "nome": "Moeda Atletismo Paraolímpico 2016",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/moeda-de-um-real-comemorativa-aos-jogos-ol%C3%ADmpicos-rio-2016-atletismo-paral%C3%ADmpico___642138-SIT.html"
    },
    {
        "nome": "Moeda Banco Central 40 Anos",
        "url": "https://www.numismaticavieira.com.br/Moedas-Nacionais/Republica/Aco/Real/catalogo-vieira-no-95-1-real-banco-central-bimetalica___432487-SIT.html"
    }
]

# --- NAVEGAÇÃO POR ABAS ---
tab_acervo, tab_moedas, tab_sites = st.tabs([
    "📦 Acervo & Catálogo",
    "🪙 Coleção de Moedas (Links & Referências)",
    "🌐 QR Codes dos Meus Sites"
])

# ==========================================
# ABA 1: ACERVO & CATÁLOGO DE COLECIONÁVEIS
# ==========================================
with tab_acervo:
    # BARRA LATERAL (FILTROS)
    st.sidebar.title("⚽ Filtros do Acervo")

    categorias_disponiveis = ["Todas"] + list(df_acervo["categoria"].unique())
    categoria_sel = st.sidebar.selectbox("Filtrar por Categoria", categorias_disponiveis)

    paises_disponiveis = ["Todos"] + list(df_acervo["pais"].dropna().unique())
    pais_sel = st.sidebar.selectbox("Filtrar por País", paises_disponiveis)

    marcas_disponiveis = ["Todas"] + list(df_acervo["marca"].dropna().unique())
    marca_sel = st.sidebar.selectbox("Filtrar por Marca / Editora", marcas_disponiveis)

    status_sel = st.sidebar.radio("Status do Item", ["Todos", "Apenas Disponíveis", "Apenas Vendidos"])

    busca = st.sidebar.text_input("🔍 Buscar no Título ou Detalhes")

    # Aplicando Filtros
    df_filtrado = df_acervo.copy()

    if categoria_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria_sel]

    if pais_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["pais"] == pais_sel]

    if marca_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["marca"] == marca_sel]

    if status_sel == "Apenas Disponíveis":
        df_filtrado = df_filtrado[~df_filtrado["vendido"]]
    elif status_sel == "Apenas Vendidos":
        df_filtrado = df_filtrado[df_filtrado["vendido"]]

    if busca:
        df_filtrado = df_filtrado[
            df_filtrado["titulo"].str.contains(busca, case=False, na=False) |
            df_filtrado["time_regiao"].str.contains(busca, case=False, na=False)
        ]

    st.title("⚽ Acervo de Colecionáveis: Camisas, Livros & Moedas")
    st.write(f"Exibindo **{len(df_filtrado)}** item(ns) encontrado(s) de um total de {len(df_acervo)}.")
    st.markdown("---")

    # GRID DE PRODUTOS
    cols = st.columns(3)

    for idx, (_, item) in enumerate(df_filtrado.iterrows()):
        col = cols[idx % 3]
        
        with col:
            with st.container():
                foto_principal = item["fotos"][0] if item["fotos"] else "https://via.placeholder.com/400x500?text=Sem+Foto"
                st.image(foto_principal, use_container_width=True)
                
                # Badges
                if item["vendido"]:
                    st.markdown('<span class="badge-vendido"> VENDIDO</span>', unsafe_allow_html=True)
                elif item["tag"] == "barateou":
                    st.markdown('<span class="badge-barateou">⚡ BARATEOU</span>', unsafe_allow_html=True)
                elif item["tag"] == "livro":
                    st.markdown('<span class="badge-livro">📚 LIVRO / OBRAS</span>', unsafe_allow_html=True)
                    
                # Título e Especificações
                st.markdown(f'<div class="shirt-title">{item["titulo"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="shirt-sub"><b>Marca/Editora:</b> {item["marca"]} | <b>Tamanho/Edição:</b> {item["tamanho"]}</div>', unsafe_allow_html=True)
                
                # Preço
                if item["preco_atual"] > 0:
                    if item["preco_original"] > item["preco_atual"]:
                        st.markdown(
                            f'<span class="price-tag">R$ {item["preco_atual"]:.2f}</span>'
                            f'<span class="old-price">R$ {item["preco_original"]:.2f}</span>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(f'<span class="price-tag">R$ {item["preco_atual"]:.2f}</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="price-tag">Sob Consulta</span>', unsafe_allow_html=True)
                
                # Link WhatsApp
                msg_wsp = f"Olá Amauri, vi no app seu item: '{item['titulo']}' e tenho interesse!"
                wsp_url = f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(msg_wsp)}"
                
                if not item["vendido"]:
                    st.markdown(f"[💬 Tenho Interesse (WhatsApp)]({wsp_url})", unsafe_allow_html=True)
                
                # Expander de Links de Referência & QR Code
                with st.expander("🔗 Links de Referência & QR Code"):
                    link_ref = item["link_br"] or item["link_int"]
                    
                    if item["link_br"]:
                        st.write(f"🇧🇷 [Link Nacional / Shopee / OLX]({item['link_br']})")
                    if item["link_int"]:
                        st.write(f"🌐 [Link Internacional / Estante Virtual]({item['link_int']})")
                    if not item["link_br"] and not item["link_int"]:
                        st.write("Sem links de referência cadastrados.")
                    
                    if link_ref:
                        qr_img = gerar_qr_code(link_ref)
                        buf = io.BytesIO()
                        qr_img.save(buf, format="PNG")
                        st.image(buf.getvalue(), caption="Aponte a câmera para o Link de Referência", width=150)

                st.markdown("---")

# ==========================================
# ABA 2: COLEÇÃO DE MOEDAS (LINKS & QR CODES)
# ==========================================
with tab_moedas:
    st.title("🪙 Catálogo de Referência de Moedas Olímpicas & Comemorativas")
    st.write("Consulte os links oficiais no catálogo da Numismática Vieira e escaneie o QR Code individual de cada moeda.")
    st.markdown("---")

    grid_moedas = st.columns(3)
    
    for idx, moeda in enumerate(MOEDAS_LINKS):
        col = grid_moedas[idx % 3]
        with col:
            with st.container():
                st.subheader(f"🪙 {moeda['nome']}")
                st.markdown(f"[🔗 Ver no Catálogo Numismática Vieira]({moeda['url']})", unsafe_allow_html=True)
                
                qr_img = gerar_qr_code(moeda['url'])
                buf = io.BytesIO()
                qr_img.save(buf, format="PNG")
                st.image(buf.getvalue(), caption=f"QR Code: {moeda['nome']}", width=180)
                st.markdown("---")

# ==========================================
# ABA 3: QR CODES DOS MEUS SITES
# ==========================================
with tab_sites:
    st.title("🌐 QR Codes de Acesso aos Aplicativos")
    st.write("Aponte a câmera do celular para acessar diretamente as plataformas de vendas.")
    st.markdown("---")

    col_site1, col_site2 = st.columns(2)

    url_site1 = "https://qrcodes-rguxkngmtumghgrvux5mzj.streamlit.app/"
    url_site2 = "https://tshirts-football2026.streamlit.app/"

    with col_site1:
        st.subheader("📚 Site 1: Livros & Moedas")
        st.markdown(f"**Link Direto:** [{url_site1}]({url_site1})")
        qr_site1 = gerar_qr_code(url_site1)
        buf_site1 = io.BytesIO()
        qr_site1.save(buf_site1, format="PNG")
        st.image(buf_site1.getvalue(), caption="Acesse o Site 1 (Livros e Moedas)", width=260)

    with col_site2:
        st.subheader("⚽ Site 2: Camisas de Futebol")
        st.markdown(f"**Link Direto:** [{url_site2}]({url_site2})")
        qr_site2 = gerar_qr_code(url_site2)
        buf_site2 = io.BytesIO()
        qr_site2.save(buf_site2, format="PNG")
        st.image(buf_site2.getvalue(), caption="Acesse o Site 2 (Camisas de Futebol)", width=260)
