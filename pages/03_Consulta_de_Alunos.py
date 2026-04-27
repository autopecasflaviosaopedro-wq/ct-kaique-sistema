
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consultar e Editar", layout="wide")

st.title("🔍 Consulta e Edição de Alunos")

def carregar_dados():
    try:
        conn = sqlite3.connect('gestao_academia.db')
        df = pd.read_sql_query("SELECT * FROM alunos", conn)
        conn.close()
        return df
    except:
        return None

def atualizar_aluno(id_aluno, nome, cpf, rg, tel, nasc, pagto):
    conn = sqlite3.connect('gestao_academia.db')
    c = conn.cursor()
    c.execute("""
        UPDATE alunos 
        SET nome=?, cpf=?, rg=?, tel=?, nasc=?, pagto=? 
        WHERE id=?
    """, (nome, cpf, rg, tel, nasc, pagto, id_aluno))
    conn.commit()
    conn.close()

df_alunos = carregar_dados()

if df_alunos is not None and not df_alunos.empty:
    busca = st.text_input("Pesquisar por nome:").upper()
    df_filtrado = df_alunos[df_alunos['nome'].str.contains(busca, na=False)] if busca else df_alunos
    
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

    st.write("---")
    st.subheader("⚙️ Ações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        id_selecionado = st.number_input("Digite o ID do aluno para Editar ou Excluir:", min_value=0, step=1)
    
    if id_selecionado > 0:
        # Puxa os dados atuais do aluno selecionado
        aluno_data = df_alunos[df_alunos['id'] == id_selecionado]
        
        if not aluno_data.empty:
            with st.expander(f"📝 Editar dados de: {aluno_data['nome'].values[0]}"):
                with st.form("form_edicao"):
                    novo_nome = st.text_input("Nome:", value=aluno_data['nome'].values[0]).upper()
                    novo_cpf = st.text_input("CPF:", value=aluno_data['cpf'].values[0])
                    novo_tel = st.text_input("Telefone:", value=aluno_data['tel'].values[0])
                    novo_rg = st.text_input("RG:", value=aluno_data['rg'].values[0])
                    novo_nasc = st.text_input("Nascimento:", value=aluno_data['nasc'].values[0])
                    novo_pagto = st.text_input("Dia Pagto:", value=aluno_data['pagto'].values[0])
                    
                    if st.form_submit_button("💾 Salvar Alterações"):
                        atualizar_aluno(id_selecionado, novo_nome, novo_cpf, novo_rg, novo_tel, novo_nasc, novo_pagto)
                        st.success("Dados atualizados!")
                        st.rerun()
            
            if st.button("❌ EXCLUIR ALUNO DEFINITIVAMENTE"):
                conn = sqlite3.connect('gestao_academia.db')
                conn.cursor().execute(f"DELETE FROM alunos WHERE id = {id_selecionado}")
                conn.commit()
                conn.close()
                st.warning("Aluno removido!")
                st.rerun()
else:
    st.info("Nenhum aluno cadastrado.")

if st.button("⬅️ Voltar"):
    st.switch_page("app.py")
