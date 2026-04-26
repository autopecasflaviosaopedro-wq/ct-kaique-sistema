import streamlit as st

# 1. Configuração da página - Força o menu lateral a abrir sozinho no celular
st.set_page_config(
    page_title="Sistema CT Kaique", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Estilização para botões grandes (Estilo App de Celular)
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 100px;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        border-radius: 15px;
        margin-bottom: 20px;
        white-space: normal;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Painel de Controle - CT Kaique")
st.write("---")

st.subheader("Escolha o que deseja gerenciar:")

# 3. Botões de Atalho no meio da tela
col1, col2 = st.columns(2)

with col1:
    # Botão azul chamativo para Alunos
    if st.button("👥 IR PARA:\nCADASTRO DE ALUNOS", type="primary"):
        try:
            st.switch_page("pages/01_Cadastro_de_Alunos.py")
        except:
            st.error("Erro: Verifique se a pasta 'pages' e o arquivo '01_Cadastro_de_Alunos.py' estão no GitHub!")

with col2:
    # Botão para Modalidades
    if st.button("🥋 IR PARA:\nCADASTRO MODALIDADES"):
        try:
            st.switch_page("pages/02_Cadastro_Modalidades.py")
        except:
            st.error("Erro: O arquivo '02_Cadastro_Modalidades.py' não foi encontrado na pasta 'pages'!")

st.write("---")

# 4. Instruções visuais
st.info("💡 **Dica para Celular:** Use o menu que desliza da esquerda para navegar mais rápido!")

st.markdown("""
### ℹ️ Resumo das Funções:
* **Cadastro de Alunos:** Matrículas, presenças e dados pessoais.
* **Cadastro Modalidades:** Gerenciar preços, modalidades (Jiu-Jitsu, Muay Thai) e horários.
""")

st.write("---")
st.caption("Sistema CT Kaique v2.0 - Unificado")