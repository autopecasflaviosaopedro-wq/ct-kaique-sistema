import streamlit as st
import sqlite3
import pandas as pd

# Configuração para celular
st.set_page_config(page_title="Consultar Modalidades", layout="wide")

st.title("🔍 Consulta e Edição de Modalidades")

# --- FUNÇÕES DE BANCO DE DADOS ---

def carregar_modalidades():
    try:
        conn = sqlite3.connect('gestao_academia.db')
        df = pd.read_sql_query("SELECT id, nome_modalidade, preco, grade FROM modalidades", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar: {e}")
        return None

def verificar_conflito_edicao(id_atual, grade_nova):
    """Verifica se os novos horários conflitam com OUTRAS modalidades"""
    conn = sqlite3.connect('gestao_academia.db')
    c = conn.cursor()
    # Busca todas as modalidades, EXCETO a que estamos editando agora
    c.execute("SELECT nome_modalidade, grade FROM modalidades WHERE id != ?", (id_atual,))
    outras_modalidades = c.fetchall()
    conn.close()

    horarios_novos = [h.strip() for h in grade_nova.split("|")]

    for h_novo in horarios_novos:
        for nome_existente, grade_existente in outras_modalidades:
            if grade_existente:
                horarios_db = [h.strip() for h in grade_existente.split("|")]
                if h_novo in horarios_db:
                    return f"Conflito! O horário '{h_novo}' já está ocupado por: {nome_existente}"
    return None

def atualizar_modalidade(id_mod, nome, preco, grade):
    try:
        conn = sqlite3.connect('gestao_academia.db')
        c = conn.cursor()
        c.execute("""
            UPDATE modalidades 
            SET nome_modalidade=?, preco=?, grade=? 
            WHERE id=?
        """, (nome, preco, grade, id_mod))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False

# --- INTERFACE ---

# Estilo para botões no celular
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 50px; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

df_mod = carregar_modalidades()

if df_mod is not None and not df_mod.empty:
    st.write("### Grade Atual")
    st.dataframe(df_mod, use_container_width=True, hide_index=True)
    
    st.write("---")
    st.subheader("⚙️ Gerenciar Modalidade")
    
    id_selecionado = st.number_input("Digite o ID para Editar ou Excluir:", min_value=0, step=1)
    
    if id_selecionado > 0:
        dados = df_mod[df_mod['id'] == id_selecionado]
        
        if not dados.empty:
            col_edit, col_del = st.columns(2)
            
            with col_edit:
                with st.expander(f"📝 EDITAR: {dados['nome_modalidade'].values[0]}"):
                    with st.form("form_edita_mod"):
                        novo_nome = st.text_input("Nome:", value=dados['nome_modalidade'].values[0]).upper()
                        novo_preco = st.number_input("Preço (R$):", value=float(dados['preco'].values[0]), format="%.2f")
                        nova_grade = st.text_area("Grade (Ex: Seg: 08:00 | Qua: 08:00):", value=dados['grade'].values[0])
                        
                        if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                            # 1. Verifica conflito antes de atualizar
                            conflito = verificar_conflito_edicao(id_selecionado, nova_grade)
                            
                            if conflito:
                                st.error(f"🚫 {conflito}")
                            else:
                                if atualizar_modalidade(id_selecionado, novo_nome, novo_preco, nova_grade):
                                    st.success("Atualizado com sucesso!")
                                    st.rerun()
            
            with col_del:
                if st.button("❌ EXCLUIR", type="secondary"):
                    conn = sqlite3.connect('gestao_academia.db')
                    conn.cursor().execute("DELETE FROM modalidades WHERE id = ?", (id_selecionado,))
                    conn.commit()
                    conn.close()
                    st.warning("Modalidade removida!")
                    st.rerun()
        else:
            st.error("ID não encontrado.")

else:
    st.info("Nenhuma modalidade cadastrada.")

st.write("---")
if st.button("⬅️ Voltar ao Início"):
    st.switch_page("app.py")
