import streamlit as st
import mercadopago
import uuid

st.set_page_config(
    page_title="Pagamento - NerdAcess",
    page_icon="💳",
    layout="centered"
)

st.title("Finalizar Pagamento 💳")

# Tenta carregar o Access Token do Mercado Pago dos secrets do Streamlit
try:
    sdk = mercadopago.SDK(st.secrets["MERCADOPAGO_ACCESS_TOKEN"])
except (KeyError, FileNotFoundError):
    st.error("A chave de acesso do Mercado Pago não foi configurada. O pagamento não pode ser processado.")
    st.stop()

# Verifica se o carrinho existe e não está vazio
if 'carrinho' in st.session_state and st.session_state.carrinho:
    
    items = []
    total_pedido = 0
    for item in st.session_state.carrinho:
        items.append({
            "title": item['nome_produto'],
            "quantity": item['quantidade'],
            "unit_price": item['preco']
        })
        total_pedido += item['preco'] * item['quantidade']

    st.subheader("Resumo do Pedido")
    for item in st.session_state.carrinho:
        st.write(f"- {item['nome_produto']} (x{item['quantidade']}): R$ {item['preco'] * item['quantidade']:.2f}")
    st.markdown("---")
    st.header(f"Total a pagar: R$ {total_pedido:.2f}")

    # Cria a preferência de pagamento
    preference_data = {
        "items": items,
        "external_reference": str(uuid.uuid4()), # ID único para o pedido
        "back_urls": {
            # Futuramente, criar páginas de sucesso, falha e pendente
            "success": "http://localhost:8501", 
            "failure": "http://localhost:8501",
            "pending": "http://localhost:8501"
        },
        "auto_return": "approved"
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        link_pagamento = preference["init_point"]
        
        st.markdown(f"[Pagar com Mercado Pago]({link_pagamento})", unsafe_allow_html=True)
        st.success("Clique no link acima para ser redirecionado para um ambiente de pagamento seguro.")

    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o link de pagamento: {e}")
        st.warning("Por favor, tente novamente mais tarde.")

else:
    st.warning("Seu carrinho está vazio. Adicione produtos antes de prosseguir para o pagamento.")
    st.page_link("app.py", label="Voltar para a loja", icon="🛍️")