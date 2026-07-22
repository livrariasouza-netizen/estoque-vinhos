import streamlit as st
import json
import os

# Configuração da página
st.set_page_config(page_title="Gestão de Estoque de Vinhos", page_icon="🍷", layout="centered")

ARQUIVO_BANCO = "estoque_vinhos.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if "estoque" not in st.session_state:
    st.session_state.estoque = carregar_dados()

st.title("🍷 Controle de Estoque de Vinhos")

menu = st.sidebar.radio("Navegação", ["📋 Ver Todos os Vinhos", "➕ Cadastrar Vinho", "🔍 Buscar/Atualizar", "❌ Remover Vinho"])

if menu == "📋 Ver Todos os Vinhos":
    st.header("📋 Todos os Vinhos no Estoque")
    if not st.session_state.estoque:
        st.warning("Nenhum vinho cadastrado no momento.")
    else:
        st.table(st.session_state.estoque)

elif menu == "➕ Cadastrar Vinho":
    st.header("➕ Cadastrar Novo Vinho")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome do Vinho")
        tipo = st.selectbox("Tipo", ["Tinto", "Branco", "Rosé", "Espumante", "Sobremesa"])
        safra = st.number_input("Safra (Ano)", min_value=1900, max_value=2030, value=2020)
        quantidade = st.number_input("Quantidade em Estoque", min_value=1, value=1)
        preco = st.number_input("Preço Estimado (R$)", min_value=0.0, value=50.0, step=5.0)
        
        submitted = st.form_submit_button("Salvar Vinho")
        if submitted:
            if nome.strip() == "":
                st.error("O nome do vinho é obrigatório!")
            else:
                novo_vinho = {
                    "Nome": nome,
                    "Tipo": tipo,
                    "Safra": int(safra),
                    "Quantidade": int(quantidade),
                    "Preço": float(preco)
                }
                st.session_state.estoque.append(novo_vinho)
                salvar_dados(st.session_state.estoque)
                st.success(f"Vinho '{nome}' cadastrado com sucesso!")

elif menu == "🔍 Buscar/Atualizar":
    st.header("🔍 Buscar e Atualizar Estoque")
    busca = st.text_input("Digite o nome do vinho para buscar:")
    if busca:
        resultados = [v for v in st.session_state.estoque if busca.lower() in v["Nome"].lower()]
        if resultados:
            for vinho in resultados:
                st.write(f"**Vinho:** {vinho['Nome']} | **Tipo:** {vinho['Tipo']} | **Safra:** {vinho['Safra']}")
                nova_qtd = st.number_input(f"Nova quantidade para {vinho['Nome']}:", min_value=0, value=vinho['Quantidade'], key=vinho['Nome'])
                if st.button(f"Atualizar Qtd de {vinho['Nome']}"):
                    vinho['Quantidade'] = int(nova_qtd)
                    salvar_dados(st.session_state.estoque)
                    st.success("Quantidade atualizada!")
        else:
            st.warning("Nenhum vinho encontrado com esse nome.")

elif menu == "❌ Remover Vinho":
    st.header("❌ Remover Vinho do Estoque")
    if not st.session_state.estoque:
        st.warning("Nenhum vinho para remover.")
    else:
        nomes_vinhos = [v["Nome"] for v in st.session_state.estoque]
        vinho_para_remover = st.selectbox("Selecione o vinho a remover:", nomes_vinhos)
        if st.button("Deletar Vinho"):
            st.session_state.estoque = [v for v in st.session_state.estoque if v["Nome"] != vinho_para_remover]
            salvar_dados(st.session_state.estoque)
            st.success(f"'{vinho_para_remover}' foi removido com sucesso!")
            st.rerun()
