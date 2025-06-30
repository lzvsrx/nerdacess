import streamlit as st

st.set_page_config(
    page_title="NerdAcess - Sua Loja Nerd Acessível",
    page_icon="휠체어",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.meusite.com/help',
        'Report a bug': "https://www.meusite.com/bug",
        'About': "# Este é um e-commerce com foco em acessibilidade!"
    }
)

st.title("Bem-vindo à NerdAcess! 🚀")
st.markdown("---")

st.sidebar.title("Menu")
st.sidebar.info("Navegue pelas seções do nosso site.")
st.sidebar.markdown("---")
st.sidebar.success("🔒 Ambiente de Navegação Seguro")

st.header("Sobre Nós")
st.write(
    """
    A NerdAcess é mais do que uma loja, é uma comunidade! 
    Nossa missão é trazer o melhor do universo nerd para todos, com um foco especial em acessibilidade. 
    Queremos que todos, sem exceção, possam navegar, escolher e comprar seus itens favoritos de forma 
    simples, segura e divertida.
    """
)

import pandas as pd
import os

# Função para carregar produtos
def carregar_produtos():
    path = "data/produtos.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame(columns=["id_produto", "id_lojista", "nome_produto", "marca", "preco", "descricao", "imagem"])

st.header("Nossos Produtos")
st.write("Explore nosso catálogo e encontre produtos incríveis!")

df_produtos = carregar_produtos()

# --- Filtros ---
st.sidebar.header("Filtros")
filtro_nome = st.sidebar.text_input("Buscar por nome:")
marcas_disponiveis = ["Todas"] + sorted(df_produtos['marca'].unique().tolist())
filtro_marca = st.sidebar.selectbox("Filtrar por marca:", marcas_disponiveis)
preco_maximo = df_produtos['preco'].max() if not df_produtos.empty else 1000.0
filtro_preco = st.sidebar.slider("Preço máximo (R$):", 0.0, float(preco_maximo), float(preco_maximo))

# Aplicar filtros
produtos_filtrados = df_produtos

if filtro_nome:
    produtos_filtrados = produtos_filtrados[produtos_filtrados['nome_produto'].str.contains(filtro_nome, case=False, na=False)]
if filtro_marca != "Todas":
    produtos_filtrados = produtos_filtrados[produtos_filtrados['marca'] == filtro_marca]
if filtro_preco:
    produtos_filtrados = produtos_filtrados[produtos_filtrados['preco'] <= filtro_preco]


# --- Listagem de Produtos ---
if produtos_filtrados.empty:
    st.warning("Nenhum produto encontrado com os filtros selecionados.")
else:
    # Exibir produtos em colunas
    colunas = st.columns(3)
    for i, produto in produtos_filtrados.iterrows():
        coluna_atual = colunas[i % 3]
        with coluna_atual:
            if os.path.exists(produto['imagem']):
                st.image(produto['imagem'], caption=produto['nome_produto'], use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x200.png?text=Imagem+N/D", use_container_width=True)
            
            st.markdown(f"**{produto['nome_produto']}**")
            st.markdown(f"_{produto['marca']}_")
            st.markdown(f"**R$ {produto['preco']:.2f}**")
            st.page_link(
                "pages/4_Produto.py",
                label="Ver detalhes",
                icon="🛍️",
                query_params={"id": produto['id_produto']}
            )