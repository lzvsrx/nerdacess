import streamlit as st
import pandas as pd
import os

# Função para carregar ou criar o dataframe de clientes
def carregar_clientes():
    if os.path.exists("data/clientes.csv"):
        return pd.read_csv("data/clientes.csv")
    else:
        df = pd.DataFrame(columns=["id_cliente", "nome_completo", "email", "senha"])
        df.to_csv("data/clientes.csv", index=False)
        return df

# Função para carregar ou criar o dataframe de lojistas
def carregar_lojistas():
    if os.path.exists("data/lojistas.csv"):
        return pd.read_csv("data/lojistas.csv")
    else:
        df = pd.DataFrame(columns=["id_lojista", "nome_loja", "cnpj", "email", "senha"])
        df.to_csv("data/lojistas.csv", index=False)
        return df

st.set_page_config(
    page_title="Cadastro - NerdAcess",
    page_icon="📝",
    layout="centered"
)

st.title("Crie sua Conta 📝")

tipo_usuario = st.radio(
    "Você quer se cadastrar como:",
    ('Cliente', 'Lojista'),
    horizontal=True,
    help="Escolha o tipo de conta que deseja criar."
)

st.markdown("---")

if tipo_usuario == 'Cliente':
    with st.form("cadastro_cliente_form", clear_on_submit=True):
        st.markdown("#### Dados do Cliente")
        
        nome_cliente = st.text_input("Nome Completo")
        email_cliente = st.text_input("Email", placeholder="seuemail@exemplo.com")
        senha_cliente = st.text_input("Senha", type="password")
        confirma_senha_cliente = st.text_input("Confirme a Senha", type="password")
        
        submit_cliente = st.form_submit_button("Cadastrar como Cliente")

        if submit_cliente:
            if senha_cliente == confirma_senha_cliente and nome_cliente and email_cliente:
                df_clientes = carregar_clientes()
                if email_cliente in df_clientes['email'].values:
                    st.error("Este email já está cadastrado.")
                else:
                    novo_id = len(df_clientes) + 1
                    novo_cliente = pd.DataFrame({
                        'id_cliente': [novo_id],
                        'nome_completo': [nome_cliente],
                        'email': [email_cliente],
                        'senha': [senha_cliente] # Em um projeto real, a senha seria hasheada
                    })
                    df_clientes = pd.concat([df_clientes, novo_cliente], ignore_index=True)
                    df_clientes.to_csv("data/clientes.csv", index=False)
                    st.success("Cadastro de cliente realizado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos e verifique se as senhas coincidem.")

elif tipo_usuario == 'Lojista':
    with st.form("cadastro_lojista_form", clear_on_submit=True):
        st.markdown("#### Dados do Lojista")
        
        nome_loja = st.text_input("Nome da Loja")
        cnpj = st.text_input("CNPJ", help="Digite apenas os números.")
        email_lojista = st.text_input("Email da Loja", placeholder="contato@sualoja.com")
        senha_lojista = st.text_input("Senha", type="password")
        confirma_senha_lojista = st.text_input("Confirme a Senha", type="password")
        
        submit_lojista = st.form_submit_button("Cadastrar como Lojista")

        if submit_lojista:
            if senha_lojista == confirma_senha_lojista and nome_loja and cnpj and email_lojista:
                df_lojistas = carregar_lojistas()
                if email_lojista in df_lojistas['email'].values:
                    st.error("Este email de loja já está cadastrado.")
                elif cnpj in df_lojistas['cnpj'].values:
                    st.error("Este CNPJ já está cadastrado.")
                else:
                    novo_id = len(df_lojistas) + 1
                    novo_lojista = pd.DataFrame({
                        'id_lojista': [novo_id],
                        'nome_loja': [nome_loja],
                        'cnpj': [cnpj],
                        'email': [email_lojista],
                        'senha': [senha_lojista] # Hashear a senha
                    })
                    df_lojistas = pd.concat([df_lojistas, novo_lojista], ignore_index=True)
                    df_lojistas.to_csv("data/lojistas.csv", index=False)
                    st.success("Cadastro de lojista realizado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos e verifique se as senhas coincidem.")