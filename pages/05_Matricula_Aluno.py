
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Matrícula de Aluno", layout="centered")

# --- FUNÇÕES DE BANCO DE DADOS ---

def carregar_modalidades():
    conn = sqlite3.connect('gestao_academia.db')
    try:
        # Busca apenas o nome para preencher o seletor
        df = pd.read_sql_query("SELECT nome_modalidade FROM modalidades", conn)
        conn.close()
        return df['nome_modalidade'].tolist()
    except:
        conn.close()
        return []

def carregar_alunos():
    conn = sqlite3.connect('gestao_academia.db')
    try:
        df = pd.read_sql_query("SELECT nome FROM alunos", conn)
        conn.close()
        return df['nome'].tolist()
    except:
        conn.close()
        return []

def efetuar_matricula(nome_aluno, nome_mod):
    try:
        conn = sqlite3.connect('gestao_academia.db')
        c = conn.cursor()
        # Criar a tabela de matrículas se não existir
        c.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno TEXT,
                modalidade TEXT,
                data_matricula DATE DEFAULT CURRENT_DATE
            )
        """)
        # Verifica se o aluno já está matriculado nessa modalidade para não duplicar
        c.execute("SELECT * FROM matriculas WHERE aluno = ? AND modalidade = ?", (nome_aluno, nome_mod))
        if c.fetchone():
            conn.close()
            return "Erro: Este aluno já está matriculado nesta modalidade!"
        
        c.execute("INSERT INTO matriculas (aluno, modalidade) VALUES (?, ?)", (nome_aluno, nome_mod))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return f"Erro no banco: {e}"

# --- INTERFACE ---

st.title("📝 Matrícula de Alunos")

lista_alunos = carregar_alunos()
lista_mod = carregar_modalidades()

if not lista_alunos:
    st.warning("⚠️ Nenhum aluno cadastrado! Cadastre o aluno primeiro.")
elif not lista_mod:
    st.warning("⚠️ Nenhuma modalidade cadastrada! Cadastre as modalidades primeiro.")
else:
    with st.form("form_matricula", clear_on_submit=True):
        aluno_sel = st.selectbox("Selecione o Aluno:", lista_alunos)
        mod_sel = st.selectbox("Selecione a Modalidade:", lista_mod)
        
        st.write("---")
        submit = st.form_submit_button("✅ CONFIRMAR MATRÍCULA")
        
        if submit:
            resultado = efetuar_matricula(aluno_sel, mod_sel)
            
            if resultado is True:
                st.success(f"Matrícula de **{aluno_sel}** em **{mod_sel}** realizada!")
                st.balloons()
            else:
                st.error(resultado)

st.write("---")
if st.button("⬅️ Voltar"):
    st.switch_page("app.py")
