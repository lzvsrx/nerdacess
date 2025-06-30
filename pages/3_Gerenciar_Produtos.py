import streamlit as st
import pandas as pd
import os
from PIL import Image

# Função para carregar ou criar o dataframe de produtos
def carregar_produtos():
    path = "data/produtos.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=["id_produto", "id_lojista", "nome_produto", "marca", "preco", "descricao", "imagem"])
        df.to_csv(path, index=False)
        return df

st.set_page_config(
    page_title="Gerenciar Produtos - NerdAcess",
    page_icon="📦",
    layout="wide"
)

st.title("Gerenciamento de Produtos 📦")

# Verifica se o usuário é um lojista logado
if 'logged_in' in st.session_state and st.session_state['logged_in'] and st.session_state['user_type'] == 'lojista':
    
    st.success(f"Bem-vindo, {st.session_state['user_info']['nome_loja']}!")
    st.markdown("---")

    # --- Formulário para adicionar novo produto ---
    with st.expander("Adicionar Novo Produto", expanded=True):
        with st.form("novo_produto_form", clear_on_submit=True):
            st.markdown("#### Detalhes do Produto")
            
            nome_produto = st.text_input("Nome do Produto")
            marca = st.text_input("Marca")
            preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
            descricao = st.text_area("Descrição do Produto")
            imagem_produto = st.file_uploader("Imagem do Produto", type=['png', 'jpg', 'jpeg'])
            
            submit_produto = st.form_submit_button("Cadastrar Produto")

            if submit_produto:
                if nome_produto and marca and preco > 0 and descricao and imagem_produto:
                    # Salvar a imagem
                    img = Image.open(imagem_produto)
                    # Garante que o diretório de imagens de produtos exista
                    os.makedirs("assets/produtos", exist_ok=True) 
                    caminho_imagem = os.path.join("assets/produtos", imagem_produto.name)
                    img.save(caminho_imagem)

                    # Adicionar produto ao CSV
                    df_produtos = carregar_produtos()
                    novo_id_produto = len(df_produtos) + 1
                    id_lojista = st.session_state['user_info']['id_lojista']
                    
                    novo_produto = pd.DataFrame({
                        'id_produto': [novo_id_produto],
                        'id_lojista': [id_lojista],
                        'nome_produto': [nome_produto],
                        'marca': [marca],
                        'preco': [preco],
                        'descricao': [descricao],
                        'imagem': [caminho_imagem]
                    })

                    df_produtos = pd.concat([df_produtos, novo_produto], ignore_index=True)
                    df_produtos.to_csv("data/produtos.csv", index=False)
                    st.success("Produto cadastrado com sucesso!")
                else:
                    st.error("Por favor, preencha todos os campos para cadastrar o produto.")

    st.markdown("---")
    # --- Listagem dos produtos do lojista ---
    st.header("Seus Produtos Cadastrados")
    
    df_produtos_lojista = carregar_produtos()
    id_lojista_logado = st.session_state['user_info']['id_lojista']
    produtos_do_lojista = df_produtos_lojista[df_produtos_lojista['id_lojista'] == id_lojista_logado]

    if produtos_do_lojista.empty:
        st.info("Você ainda não cadastrou nenhum produto.")
    else:
        st.dataframe(produtos_do_lojista)

else:
    st.error("Acesso negado. Por favor, faça o login como lojista para acessar esta página.")
    st.info("Vá para a página de Login para entrar na sua conta.")