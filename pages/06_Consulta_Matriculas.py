
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consulta de Matrículas", layout="wide")

# --- FUNÇÕES DE BANCO DE DADOS ---

def carregar_matriculas():
    try:
        conn = sqlite3.connect('gestao_academia.db')
        # Buscamos os dados da tabela de matrículas
        df = pd.read_sql_query("SELECT id, aluno, modalidade, data_matricula FROM matriculas", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame() # Retorna vazio se a tabela não existir ainda

def excluir_matricula(id_mat):
    try:
        conn = sqlite3.connect('gestao_academia.db')
        c = conn.cursor()
        c.execute("DELETE FROM matriculas WHERE id = ?", (id_mat,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao excluir: {e}")
        return False

# --- INTERFACE ---

st.title("📋 Relatório de Matrículas")
st.write("Visualize quais alunos estão em cada modalidade.")

# Estilo para botões mobile
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

df_mat = carregar_matriculas()

if not df_mat.empty:
    # Filtro rápido para facilitar no celular
    filtro_mod = st.selectbox("Filtrar por Modalidade:", ["TODAS"] + list(df_mat['modalidade'].unique()))
    
    df_exibir = df_mat if filtro_mod == "TODAS" else df_mat[df_mat['modalidade'] == filtro_mod]
    
    st.dataframe(df_exibir, use_container_width=True, hide_index=True)
    
    st.write("---")
    st.subheader("🗑️ Cancelar Matrícula")
    
    id_para_excluir = st.number_input("Digite o ID da matrícula para remover:", min_value=0, step=1)
    
    if id_para_excluir > 0:
        # Verifica se o ID existe no que foi carregado
        confirmar = st.button("❌ CONFIRMAR EXCLUSÃO DE MATRÍCULA")
        if confirmar:
            if excluir_matricula(id_para_excluir):
                st.warning(f"Matrícula {id_para_excluir} removida!")
                st.rerun()
else:
    st.info("Nenhuma matrícula encontrada no sistema.")

st.write("---")
if st.button("⬅️ Voltar"):
    st.switch_page("app.py")
