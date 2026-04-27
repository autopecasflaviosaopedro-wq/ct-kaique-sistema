
import streamlit as st
import sqlite3

st.set_page_config(page_title="Cadastro de Modalidades", layout="centered")

# Função para verificar se o horário já está ocupado
def verificar_conflito(horarios_novos):
    conn = sqlite3.connect('gestao_academia.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS modalidades (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_modalidade TEXT, preco REAL, grade TEXT)")
    
    c.execute("SELECT nome_modalidade, grade FROM modalidades")
    modalidades_existentes = c.fetchall()
    conn.close()

    for h_novo in horarios_novos:
        dia_novo = h_novo.split(":")[0].strip() # Pega o "Seg"
        hora_nova = h_novo.split(":")[1].strip() # Pega o "08:00"

        for nome_existente, grade_existente in modalidades_existentes:
            if grade_existente:
                horarios_db = grade_existente.split(" | ")
                for h_db in horarios_db:
                    if h_novo == h_db:
                        return f"O horário {dia_novo} às {hora_nova} já está ocupado pela modalidade: {nome_existente}"
    return None

def salvar_modalidade_db(nome, preco, grade_horarios):
    try:
        conn = sqlite3.connect('gestao_academia.db')
        c = conn.cursor()
        # O uso de IF NOT EXISTS previne erros, e o check de conflito previne duplicados
        c.execute("INSERT INTO modalidades (nome_modalidade, preco, grade) VALUES (?, ?, ?)", 
                  (nome, preco, grade_horarios))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro: {e}")
        return False

st.title("🥋 Cadastro de Modalidades")

nome_mod = st.text_input("NOME DA MODALIDADE:").upper().strip()
preco_mod = st.number_input("VALOR MENSALIDADE (R$):", min_value=0.0, format="%.2f")

st.write("---")
st.write("### 📅 Grade de Horários")

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
horarios_escolhidos = []

for dia in dias:
    col_dia, col_hora = st.columns([1, 1])
    with col_dia:
        checado = st.checkbox(dia, key=f"c_{dia}")
    with col_hora:
        hora = st.text_input(
            f"Hora {dia}", 
            placeholder="00:00", 
            label_visibility="collapsed", 
            disabled=not checado,
            key=f"i_{dia}"
        )
        if checado and hora:
            # Padroniza para "Seg: 08:00"
            horarios_escolhidos.append(f"{dia[:3]}: {hora.strip()}")

st.write("---")

# 3. Botão de Salvar com trava de segurança
if st.button("✅ SALVAR MODALIDADE", use_container_width=True):
    if not nome_mod or not horarios_escolhidos:
        st.warning("⚠️ Preencha o nome e selecione pelo menos um dia/horário!")
    else:
        # Primeiro: verifica se há conflito de horário
        conflito = verificar_conflito(horarios_escolhidos)
        
        if conflito:
            st.error(f"🚫 {conflito}")
        else:
            # Segundo: Salva se estiver tudo limpo
            grade_final = " | ".join(horarios_escolhidos)
            if salvar_modalidade_db(nome_mod, preco_mod, grade_final):
                st.success(f"Modalidade {nome_mod} salva com sucesso!")
                st.balloons()
                # O rerun limpa os campos e evita que o usuário clique 2x e duplique
                st.rerun()

if st.button("⬅️ Voltar"):
    st.switch_page("app.py")
