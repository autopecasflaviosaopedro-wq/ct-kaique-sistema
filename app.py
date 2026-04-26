import streamlit as st

# Configuração da página - Forçando o menu lateral a abrir (expanded)
st.set_page_config(
    page_title="Sistema CT Kaique", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilização para deixar os botões grandes e bonitos
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 100px;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .st-emotion-cache-1kyxreq {
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Painel de Controle - CT Kaique")
st.write("---")

st.subheader("Escolha uma opção para navegar:")

# Criando colunas para os botões ficarem lado a lado no PC e empilhados no Celular
col1, col2 = st.columns(2)

with col1:
    if st.button("📂 IR PARA: CADASTRO DE ALUNOS", type="primary"):
        st.switch_page("pages/01_Cadastro_de_Alunos.py")

with col2:
    if st.button("📅 IR PARA: GRADE DE HORÁRIOS"):
        # Verifica se o arquivo da grade já existe antes de tentar mudar
        try:
            st.switch_page("pages/02_Grade_de_Horários.py")
        except:
            st.error("O arquivo da Grade ainda não foi criado na pasta 'pages'!")

st.write("---")
st.info("💡 Dica: Se preferir, use o menu lateral à esquerda para navegar.")

# Pequeno resumo ou aviso
st.markdown("""
**Instruções de uso:**
1. Clique no botão acima para a área desejada.
2. No **Cadastro**, você pode adicionar novos alunos e ver a lista.
3. Na **Grade**, você define os horários e valores das aulas.
""")