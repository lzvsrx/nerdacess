import streamlit as st
import pandas as pd
import os

# Função para carregar os dados de usuários
def carregar_usuarios(tipo):
    path = f"data/{tipo}.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

st.set_page_config(
    page_title="Login - NerdAcess",
    page_icon="🔒",
    layout="centered"
)

st.title("Área de Login 🔒")

# --- Formulário de Login ---
with st.form("login_form"):
    st.markdown("#### Acesse sua conta")
    
    email = st.text_input(
        "Email",
        placeholder="seuemail@exemplo.com",
        help="Digite o email cadastrado."
    )
    
    senha = st.text_input(
        "Senha",
        type="password",
        help="Digite sua senha."
    )
    
    submitted = st.form_submit_button("Entrar")

    if submitted:
        df_clientes = carregar_usuarios("clientes")
        df_lojistas = carregar_usuarios("lojistas")

        # Procura o usuário nos dois dataframes
        cliente = df_clientes[(df_clientes['email'] == email) & (df_clientes['senha'] == senha)]
        lojista = df_lojistas[(df_lojistas['email'] == email) & (df_lojistas['senha'] == senha)]

        if not cliente.empty:
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = 'cliente'
            st.session_state['user_info'] = cliente.iloc[0].to_dict()
            st.success("Login de cliente realizado com sucesso!")
            # Idealmente, redirecionar para a página de produtos
        elif not lojista.empty:
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = 'lojista'
            st.session_state['user_info'] = lojista.iloc[0].to_dict()
            st.success("Login de lojista realizado com sucesso!")
            # Idealmente, redirecionar para o painel do lojista
        else:
            st.error("Email ou senha incorretos.")

st.markdown("---")
st.info("Ainda não tem uma conta? Vá para a página de cadastro!")