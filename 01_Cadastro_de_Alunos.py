import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Cadastro de Alunos", layout="centered")

st.title("👥 Cadastro de Novos Alunos")

def salvar_aluno(nome, cpf, rg, tel, nasc, pagto):
    try:
        conn = sqlite3.connect('gestao_academia.db')
        c = conn.cursor()
        # CRIA A TABELA CASO ELA NÃO EXISTA (BLINDAGEM)
        c.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT, cpf TEXT, rg TEXT, tel TEXT, nasc TEXT, pagto TEXT
            )
        """)
        c.execute("""
            INSERT INTO alunos (nome, cpf, rg, tel, nasc, pagto) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, cpf, rg, tel, nasc, pagto))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return False

with st.form("form_cadastro", clear_on_submit=True):
    nome = st.text_input("NOME COMPLETO:").upper().strip()
    
    col1, col2 = st.columns(2)
    with col1:
        cpf = st.text_input("CPF (Apenas números):", max_chars=11)
        rg = st.text_input("RG:", max_chars=12)
        nasc = st.date_input("DATA DE NASCIMENTO:", min_value=date(1940, 1, 1))
        
    with col2:
        tel = st.text_input("TELEFONE (DDD + Número):", max_chars=11)
        pagto = st.number_input("DIA DE PAGAMENTO:", min_value=1, max_value=31, step=1)

    submit = st.form_submit_button("✅ SALVAR CADASTRO", use_container_width=True)

    if submit:
        if nome and cpf and tel:
            data_str = nasc.strftime("%d/%m/%Y")
            if salvar_aluno(nome, cpf, rg, tel, data_str, str(pagto)):
                st.success(f"Aluno {nome} cadastrado com sucesso!")
                st.balloons()
        else:
            st.warning("⚠️ Preencha Nome, CPF e Telefone.")

if st.button("⬅️ Voltar"):
    st.switch_page("app.py")