import streamlit as st
import pandas as pd
import os
from gtts import gTTS
import base64

# Função para carregar produtos
def carregar_produtos():
    path = "data/produtos.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# Função para gerar áudio e retorná-lo em base64
def gerar_audio_base64(texto):
    tts = gTTS(text=texto, lang='pt-br')
    audio_path = "assets/audio_descricao.mp3"
    tts.save(audio_path)
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    os.remove(audio_path) # Remove o arquivo após ler
    return base64.b64encode(audio_bytes).decode()

st.set_page_config(
    page_title="Detalhes do Produto - NerdAcess",
    page_icon="🛍️",
    layout="wide"
)

# Pega o ID do produto dos parâmetros da URL
query_params = st.query_params
produto_id = int(query_params.get("id", 0))

if produto_id > 0:
    df_produtos = carregar_produtos()
    produto = df_produtos[df_produtos['id_produto'] == produto_id]

    if not produto.empty:
        produto = produto.iloc[0]
        
        st.title(produto['nome_produto'])
        st.markdown(f"### Marca: {produto['marca']}")
        
        col1, col2 = st.columns([1, 2])

        with col1:
            if os.path.exists(produto['imagem']):
                st.image(produto['imagem'], use_column_width=True)
            else:
                st.image("https://via.placeholder.com/300x300.png?text=Imagem+N/D", use_column_width=True)

        with col2:
            st.header(f"R$ {produto['preco']:.2f}")
            st.subheader("Descrição")
            st.write(produto['descricao'])

            if st.button("Ouvir Descrição 🔊", key=f"ouvir_{produto_id}"):
                audio_base64 = gerar_audio_base64(produto['descricao'])
                audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
                st.markdown(audio_html, unsafe_allow_html=True)
            
            if st.button("Adicionar ao Carrinho", key=f"add_cart_{produto_id}"):
                # Inicializa o carrinho se não existir
                if 'carrinho' not in st.session_state:
                    st.session_state.carrinho = []
                
                # Verifica se o produto já está no carrinho
                item_existente = next((item for item in st.session_state.carrinho if item['id_produto'] == produto_id), None)
                
                if item_existente:
                    # Por enquanto, apenas informa que já está lá. Futuramente, pode incrementar a quantidade.
                    st.warning(f"{produto['nome_produto']} já está no seu carrinho.")
                else:
                    # Adiciona o item ao carrinho
                    novo_item = {
                        'id_produto': produto_id,
                        'nome_produto': produto['nome_produto'],
                        'marca': produto['marca'],
                        'preco': produto['preco'],
                        'imagem': produto['imagem'],
                        'quantidade': 1 # Começa com quantidade 1
                    }
                    st.session_state.carrinho.append(novo_item)
                    st.success(f"{produto['nome_produto']} adicionado ao carrinho!")

    else:
        st.error("Produto não encontrado.")
        st.page_link("app.py", label="Voltar para a Loja", icon="🏠")
else:
    st.warning("Nenhum produto selecionado.")
    st.page_link("app.py", label="Voltar para a Loja", icon="🏠")