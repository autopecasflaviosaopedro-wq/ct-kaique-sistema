import streamlit as st

# Configuração da página para Mobile (Ícone e Título da aba)
st.set_page_config(
    page_title="CT Kaique - Gestão",
    page_icon="🥋",
    layout="centered"
)

# Estilo CSS para botões grandes, fáceis de tocar no celular
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 65px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        margin-bottom: 12px;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        transition: all 0.3s;
    }
    .stButton>button:active {
        background-color: #007bff;
        color: white;
    }
    .main-title {
        text-align: center;
        color: #1E1E1E;
        font-family: 'Arial', sans-serif;
    }
    .section-header {
        margin-top: 20px;
        padding: 5px;
        background-color: #f8f9fa;
        border-left: 5px solid #007bff;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🥋 CT Kaique - Sistema</h1>", unsafe_allow_html=True)
st.write("---")

# --- SEÇÃO DE ALUNOS ---
st.markdown("<div class='section-header'>👥 GESTÃO DE ALUNOS</div><br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ NOVO ALUNO"):
        st.switch_page("pages/01_Cadastro_de_Alunos.py")
with col2:
    if st.button("🔍 VER ALUNOS"):
        st.switch_page("pages/03_Consulta_de_Alunos.py")

# --- SEÇÃO DE MATRÍCULAS (O VÍNCULO) ---
st.markdown("<div class='section-header'>📝 MATRÍCULAS E TURMAS</div><br>", unsafe_allow_html=True)

if st.button("✅ REALIZAR MATRÍCULA"):
    st.switch_page("pages/05_Matricula_Aluno.py")

if st.button("📋 LISTA POR MODALIDADE"):
    st.switch_page("pages/06_Consulta_Matriculas.py")

# --- SEÇÃO DE MODALIDADES ---
st.markdown("<div class='section-header'>🥋 MODALIDADES E GRADE</div><br>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    if st.button("🆕 NOVA MODAL"):
        st.switch_page("pages/02_Cadastro_Modalidades.py")
with col4:
    if st.button("📊 VER GRADE"):
        st.switch_page("pages/04_Consulta_Modalidades.py")

st.write("---")
st.caption("CT Kaique Gestão v1.0 | Operando via SQLite Local")