import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURAÇÃO DE CAMINHO ---
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(PASTA_ATUAL, 'gestao_academia.db')

st.set_page_config(page_title="SISTEMA CT KAIQUE", layout="wide")

# --- FUNÇÕES DE BANCO DE DADOS ---

def inicializar_banco():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    
    # 1. Cria a tabela se ela não existir
    cursor.execute('''CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT, cpf TEXT, rg TEXT, telefone TEXT, 
        data_nasc TEXT, status TEXT DEFAULT 'ATIVO',
        data_pagto TEXT, data_matricula TEXT)''')
    
    # 2. Adiciona colunas faltantes se o banco for antigo
    colunas_necessarias = [
        ('rg', 'TEXT'),
        ('data_nasc', 'TEXT'),
        ('data_matricula', 'TEXT')
    ]
    
    for nome_col, tipo_col in colunas_necessarias:
        try:
            cursor.execute(f"ALTER TABLE alunos ADD COLUMN {nome_col} {tipo_col}")
        except sqlite3.OperationalError:
            pass
            
    conn.commit()
    conn.close()

def executar_query(sql, params=()):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Inicializa o banco
inicializar_banco()

# --- INTERFACE ---

st.title("🏋️ GESTÃO CT KAIQUE - v1.0 (Mobile)")

tab_cadastro, tab_lista = st.tabs(["📝 Cadastro / Edição", "🔍 Lista de Alunos"])

with tab_cadastro:
    st.subheader("Dados do Aluno")
    
    query_ids = "SELECT id FROM alunos ORDER BY id DESC"
    ids_existentes = [str(row[0]) for row in executar_query(query_ids)]
    id_selecionado = st.selectbox("ID do Registro (Selecione para Editar):", ["NOVO"] + ids_existentes)

    dados = {"nome": "", "cpf": "", "rg": "", "tel": "", "nasc": "", "status": "ATIVO", "pagto": ""}
    
    if id_selecionado != "NOVO":
        res = executar_query("SELECT nome, cpf, rg, telefone, data_nasc, status, data_pagto FROM alunos WHERE id=?", (id_selecionado,))
        if res:
            r = res[0]
            dados = {"nome": r[0], "cpf": r[1], "rg": r[2], "tel": r[3], "nasc": r[4], "status": r[5], "pagto": r[6]}

    col1, col2 = st.columns(2)
    with col1:
        nome_input = st.text_input("NOME COMPLETO:", value=dados["nome"]).upper().strip()
        cpf_input = st.text_input("CPF:", value=dados["cpf"])
        rg_input = st.text_input("RG:", value=dados["rg"])
    with col2:
        tel_input = st.text_input("TELEFONE:", value=dados["tel"])
        nasc_input = st.text_input("DATA NASCIMENTO:", value=dados["nasc"])
        dia_pagto_input = st.text_input("DIA DE PAGAMENTO (01 a 31):", value=dados["pagto"])

    status_input = st.radio("STATUS:", ["ATIVO", "INATIVO"], index=0 if dados["status"] == "ATIVO" else 1)

    if st.button("💾 SALVAR / ATUALIZAR", use_container_width=True):
        if nome_input and dia_pagto_input:
            if id_selecionado == "NOVO":
                hoje = datetime.now().strftime("%d/%m/%Y")
                executar_query('''INSERT INTO alunos (nome, cpf, rg, telefone, data_nasc, status, data_pagto, data_matricula) 
                                  VALUES (?,?,?,?,?,?,?,?)''', 
                               (nome_input, cpf_input, rg_input, tel_input, nasc_input, status_input, dia_pagto_input, hoje))
                st.success(f"Aluno {nome_input} cadastrado!")
            else:
                executar_query('''UPDATE alunos SET nome=?, cpf=?, rg=?, telefone=?, data_nasc=?, status=?, data_pagto=? 
                                  WHERE id=?''', 
                               (nome_input, cpf_input, rg_input, tel_input, nasc_input, status_input, dia_pagto_input, id_selecionado))
                st.success(f"Cadastro de {nome_input} atualizado!")
            st.rerun()
        else:
            st.error("Nome e Dia de Pagamento são obrigatórios!")

with tab_lista:
    st.subheader("Pesquisar Cadastros")
    termo_busca = st.text_input("Digite o nome para filtrar:").upper()
    
    sql_busca = "SELECT id, nome, cpf, rg, telefone, data_nasc, status, data_pagto FROM alunos"
    if termo_busca:
        sql_busca += f" WHERE nome LIKE '%{termo_busca}%'"
    
    try:
        conn = sqlite3.connect(CAMINHO_BANCO)
        df = pd.read_sql_query(sql_busca, conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Erro ao carregar lista: {e}")

if st.sidebar.button("🔄 Limpar Tudo / Atualizar"):
    st.rerun()