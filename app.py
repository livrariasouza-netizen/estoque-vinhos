import streamlit as st
import json
import os

# Configuração da página
st.set_page_config(page_title="Localizador de Vinhos", page_icon="🍷", layout="centered")

# --- CONFIGURAÇÃO DE SEGURANÇA ---
SENHA_ACESSO = "1234"  # 👈 Mude a sua senha aqui!

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

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.title("🔒 Acesso Restrito - Localização de Vinhos")
    st.info("Este aplicativo contém dados de controle interno. Digite a senha para continuar.")
    
    senha_input = st.text_input("Digite a senha de acesso:", type="password")
    if st.button("Entrar no Sistema"):
        if senha_input == SENHA_ACESSO:
            st.session_state.autenticado = True
            st.success("Acesso liberado!")
            st.rerun()
        else:
            st.error("Senha incorreta! Acesso negado.")

# --- TELA PRINCIPAL (APÓS LOGIN) ---
else:
    st.sidebar.title("🍷 Gestão de Vinhos")
    if st.sidebar.button("🔒 Sair do Sistema"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🍷 Localização e Estoque de Vinhos")

    menu = st.sidebar.radio("Navegação", [
        "📍 Consultar Localização", 
        "➕ Cadastrar Novo Vinho", 
        "✏️ Editar / Mudar de Lugar", 
        "❌ Remover Vinho"
    ])

    if menu == "📍 Consultar Localização":
        st.header("📍 Onde estão os Vinhos?")
        
        busca = st.text_input("🔍 Buscar por Nome, Tipo ou Localização (ex: Prateleira 1, Adega):")
        
        if not st.session_state.estoque:
            st.warning("Nenhum vinho cadastrado no momento.")
        else:
            vinhos_exibicao = st.session_state.estoque
            if busca:
                vinhos_exibicao = [
                    v for v in st.session_state.estoque 
                    if busca.lower() in v.get("Nome", "").lower() 
                    or busca.lower() in v.get("Localizacao", "").lower()
                    or busca.lower() in v.get("Tipo", "").lower()
                ]
            
            if vinhos_exibicao:
                st.table(vinhos_exibicao)
            else:
                st.warning("Nenhum vinho encontrado com o termo buscado.")

    elif menu == "➕ Cadastrar Novo Vinho":
        st.header("➕ Cadastrar Vinho e Localização")
        with st.form("form_cadastro"):
            nome = st.text_input("Nome do Vinho")
            tipo = st.selectbox("Tipo", ["Tinto", "Branco", "Rosé", "Espumante", "Sobremesa", "Outro"])
            safra = st.number_input("Safra (Ano)", min_value=1900, max_value=2030, value=2020)
            localizacao = st.text_input("📍 Onde está guardado? (Ex: Adega A - Prateleira 2, Caixote 3)")
            quantidade = st.number_input("Quantidade de Garrafas", min_value=1, value=1)
            preco = st.number_input("Preço Estimado (R$)", min_value=0.0, value=50.0, step=5.0)
            
            submitted = st.form_submit_button("Salvar Registro")
            if submitted:
                if nome.strip() == "" or localizacao.strip() == "":
                    st.error("O Nome do vinho e a Localização são obrigatórios!")
                else:
                    novo_vinho = {
                        "Nome": nome,
                        "Tipo": tipo,
                        "Safra": int(safra),
                        "Localizacao": localizacao,
                        "Quantidade": int(quantidade),
                        "Preço": float(preco)
                    }
                    st.session_state.estoque.append(novo_vinho)
                    salvar_dados(st.session_state.estoque)
                    st.success(f"Vinho '{nome}' salvo na localização: '{localizacao}'!")

    elif menu == "✏️ Editar / Mudar de Lugar":
        st.header("✏️ Atualizar Quantidade ou Mudar de Lugar")
        if not st.session_state.estoque:
            st.warning("Nenhum vinho para editar.")
        else:
            nomes_vinhos = [v["Nome"] for v in st.session_state.estoque]
            vinho_sel = st.selectbox("Selecione o Vinho:", nomes_vinhos)
            
            # Encontra o vinho selecionado
            vinho_obj = next((v for v in st.session_state.estoque if v["Nome"] == vinho_sel), None)
            
            if vinho_obj:
                nova_loc = st.text_input("Nova Localização:", value=vinho_obj.get("Localizacao", ""))
                nova_qtd = st.number_input("Nova Quantidade:", min_value=0, value=vinho_obj.get("Quantidade", 1))
                
                if st.button("Salvar Alterações"):
                    vinho_obj["Localizacao"] = nova_loc
                    vinho_obj["Quantidade"] = int(nova_qtd)
                    salvar_dados(st.session_state.estoque)
                    st.success("Dados atualizados com sucesso!")
                    st.rerun()

    elif menu == "❌ Remover Vinho":
        st.header("❌ Remover Vinho do Sistema")
        if not st.session_state.estoque:
            st.warning("Nenhum vinho para remover.")
        else:
            nomes_vinhos = [v["Nome"] for v in st.session_state.estoque]
            vinho_para_remover = st.selectbox("Selecione o vinho a remover:", nomes_vinhos)
            if st.button("Deletar Registro"):
                st.session_state.estoque = [v for v in st.session_state.estoque if v["Nome"] != vinho_para_remover]
                salvar_dados(st.session_state.estoque)
                st.success(f"'{vinho_para_remover}' foi removido com sucesso!")
                st.rerun()
