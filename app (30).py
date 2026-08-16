import streamlit as st
import urllib.parse

st.set_page_config(page_title="Gerador de Etiquetas", page_icon="🏷️", layout="wide")

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
    if not link:
        return None
    encoded = urllib.parse.quote(link)
    return f"https://quickchart.io/qr?text={encoded}&size=150"

st.title("🏷️ Gerador de Etiquetas para Embalagens")
st.write("Abaixo estão suas etiquetas formatadas com QR Code. Para imprimir ou salvar em PDF, utilize a função de impressão do seu navegador (Menu do navegador > Imprimir).")

st.divider()

# Exibe em grade de 2 colunas para caber bem na tela do celular/computador
cols = st.columns(2)

for idx, item in enumerate(catalog):
    # Alterna entre as colunas
    col = cols[idx % 2]
    
    with col:
        with st.container(border=True):
            st.subheader(f"#{item['id']} {item['titulo']}")
            st.caption(f"**Marca:** {item['marca']} | **Tamanho:** {item['tamanho']}")
            st.markdown(f"### **Preço:** :green[{item['preco']}]")
            
            c_br, c_int = st.columns(2)
            
            qr_br = get_qr_url(item['link_br'])
            qr_int = get_qr_url(item['link_int'])
            
            with c_br:
                if qr_br:
                    st.caption("🇧🇷 **BR**")
                    st.image(qr_br, width=110)
                else:
                    st.caption("🇧🇷 *Sem Link*")
                    
            with c_int:
                if qr_int:
                    st.caption("🌎 **INT**")
                    st.image(qr_int, width=110)
                else:
                    st.caption("🌎 *Sem Link*")
