import streamlit as st
import os

# Configuração da Página
st.set_page_config(
    page_title="Sistema CT Kaique", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("🚀 Painel de Controle - CT Kaique")
st.write("---")

st.subheader("Escolha o que deseja gerenciar:")

# Criando os botões grandes
col1, col2 = st.columns(2)

with col1:
    # Botão de Alunos - Forçando o caminho correto
    if st.button("👥 IR PARA:\nCADASTRO DE ALUNOS", type="primary", use_container_width=True):
        st.switch_page("pages/01_Cadastro_de_Alunos.py")

with col2:
    # Botão de Modalidades - Forçando o caminho correto
    if st.button("🥋 IR PARA:\nCADASTRO MODALIDADES", use_container_width=True):
        st.switch_page("pages/02_Cadastro_Modalidades.py")

st.write("---")
st.info("💡 Se os botões acima derem erro, recarregue a página ou use o menu lateral à esquerda.")

# Listagem de segurança (ajuda a saber se a pasta pages está visível)
if not os.path.exists("pages"):
    st.error("⚠️ Atenção: A pasta 'pages' não foi detectada no servidor. Verifique o GitHub.")
