import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Carrinho de Compras - NerdAcess",
    page_icon="🛒",
    layout="wide"
)

st.title("Meu Carrinho de Compras 🛒")

# Inicializa o carrinho na session_state se não existir
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# Função para remover item do carrinho
def remover_item(produto_id):
    st.session_state.carrinho = [item for item in st.session_state.carrinho if item['id_produto'] != produto_id]

if not st.session_state.carrinho:
    st.info("Seu carrinho está vazio.")
    st.page_link("app.py", label="Continuar comprando", icon="🛍️")
else:
    total_carrinho = 0
    
    for item in st.session_state.carrinho:
        total_item = item['preco'] * item['quantidade']
        total_carrinho += total_item
        
        col1, col2, col3, col4, col5 = st.columns([2, 4, 2, 2, 1])
        
        with col1:
            st.image(item['imagem'], width=100)
        with col2:
            st.subheader(item['nome_produto'])
            st.caption(f"Marca: {item['marca']}")
        with col3:
            st.write(f"Preço: R$ {item['preco']:.2f}")
            # A quantidade será 1 por enquanto. Pode ser expandido no futuro.
            st.write(f"Quantidade: {item['quantidade']}")
        with col4:
            st.write(f"Subtotal: R$ {total_item:.2f}")
        with col5:
            if st.button("Remover", key=f"remover_{item['id_produto']}"):
                remover_item(item['id_produto'])
                st.rerun()

    st.markdown("---")
    st.header(f"Total do Pedido: R$ {total_carrinho:.2f}")
    
    st.page_link("pages/6_Pagamento.py", label="Finalizar Compra", icon="💳")