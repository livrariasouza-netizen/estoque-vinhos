import json
import os
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Controle de Estoque de Vinhos",
    page_icon="🍷",
    layout="wide",
)

# --- CONFIGURAÇÃO DE SEGURANÇA ---
SENHA_ACESSO = "1234"
NOME_ARQUIVO = "estoque_vinhos.json"

estoque_padrao = [
    {
        "nome": "Quereu Rose 2024",
        "tipo": "Rosé",
        "pallet": "Pallet 1",
        "caixa": "12 garrafas",
        "volume": "750ml",
    },
    {
        "nome": "Quereu Carmenere",
        "tipo": "Tinto",
        "pallet": "Pallet 2",
        "caixa": "6 garrafas",
        "volume": "750ml",
    },
    {
        "nome": "Quereu Chardonnay",
        "tipo": "Branco",
        "pallet": "Pallet 2",
        "caixa": "12 garrafas",
        "volume": "375ml",
    },
]


def carregar_dados():
    if os.path.exists(NOME_ARQUIVO):
        try:
            with open(NOME_ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados if isinstance(dados, list) else estoque_padrao
        except Exception:
            return estoque_padrao
    return estoque_padrao


def salvar_dados(estoque):
    try:
        with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(estoque, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")


# Inicializa a sessão
if "estoque" not in st.session_state:
    st.session_state.estoque = carregar_dados()

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.title("🔒 Acesso Restrito - Controle de Estoque")
    st.info("Digite a senha para acessar o localizador de vinhos.")

    senha_input = st.text_input("Digite a senha de acesso:", type="password")
    if st.button("Entrar no Sistema"):
        if senha_input == SENHA_ACESSO:
            st.session_state.autenticado = True
            st.success("Acesso liberado!")
            st.rerun()
        else:
            st.error("Senha incorreta! Acesso negado.")

# --- TELA PRINCIPAL ---
else:
    if st.sidebar.button("🔒 Sair do Sistema"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🍷 CONTROLE DE ESTOQUE DE VINHOS")
    st.caption("Sistema de Gestão de Pallets e Embalagens")
    st.markdown("---")

    menu = st.sidebar.radio(
        "Menu Principal",
        [
            "1. Buscar vinho",
            "2. Cadastrar novo vinho",
            "3. Ver todos os vinhos",
            "4. Editar vinho existente",
            "5. Excluir vinho",
            "6. Exportar tabela para Excel (CSV)",
        ],
    )

    # 1. BUSCAR VINHO
    if menu == "1. Buscar vinho":
        st.header("🔍 BUSCAR VINHO")
        sub_op = st.radio("Como deseja buscar?", ["Por Nome", "Por Tipo"])
        termo = st.text_input("Digite o termo de busca:").strip().lower()

        if termo:
            resultados = []
            for v in st.session_state.estoque:
                nome_vinho = str(v.get("nome", "")).lower()
                tipo_vinho = str(v.get("tipo", "")).lower()

                if sub_op == "Por Nome" and termo in nome_vinho:
                    resultados.append(v)
                elif sub_op == "Por Tipo" and termo in tipo_vinho:
                    resultados.append(v)

            if not resultados:
                st.warning("⚠️ Nenhum vinho encontrado.")
            else:
                st.success(f"Encontrado(s) {len(resultados)} resultado(s):")
                for v in resultados:
                    with st.expander(
                        f"🍷 {v.get('nome', 'Sem nome')} ({v.get('tipo', 'S/T')}) ➔ 📍 {v.get('pallet', 'S/P')}"
                    ):
                        st.write(f"**Localização:** {v.get('pallet', 'N/I')}")
                        st.write(f"**Caixa:** {v.get('caixa', 'N/I')}")
                        st.write(f"**Volume:** {v.get('volume', 'N/I')}")

    # 2. CADASTRAR VINHO
    elif menu == "2. Cadastrar novo vinho":
        st.header("➕ CADASTRAR VINHO")

        with st.form("form_cadastrar"):
            nome = st.text_input("Nome do vinho:").strip()
            tipo = st.text_input(
                "Tipo (Tinto, Branco, Rosé, Espumante...):"
            ).strip()
            pallet = st.text_input(
                "Localização (Ex: Pallet 1, Corredor B...):"
            ).strip()

            caixa = st.selectbox(
                "📦 Quantidade de garrafas por caixa:",
                ["12 garrafas", "6 garrafas", "3 garrafas", "1 garrafa"],
            )

            vol_opcao = st.selectbox(
                "🧪 Volume / Tamanho da garrafa:",
                ["750ml", "375ml", "1500ml (Magnum)", "Outro valor"],
            )

            volume_custom = ""
            if vol_opcao == "Outro valor":
                volume_custom = st.text_input("Digite o volume customizado:")

            submit = st.form_submit_button("✅ Salvar Vinho")

            if submit:
                volume_final = (
                    volume_custom if vol_opcao == "Outro valor" else vol_opcao
                )

                if nome and tipo and pallet:
                    novo_vinho = {
                        "nome": nome,
                        "tipo": tipo,
                        "pallet": pallet,
                        "caixa": caixa,
                        "volume": volume_final if volume_final else "750ml",
                    }
                    st.session_state.estoque.append(novo_vinho)
                    salvar_dados(st.session_state.estoque)
                    st.success(f"✅ '{nome}' cadastrado com sucesso!")
                else:
                    st.error("❌ Nome, Tipo e Localização são obrigatórios!")

    # 3. VER TODOS OS VINHOS (CORRIGIDO)
    elif menu == "3. Ver todos os vinhos":
        st.header("🍷 TODOS OS VINHOS")

        if not st.session_state.estoque:
            st.warning("Nenhum vinho cadastrado.")
        else:
            ordem = st.radio(
                "Como deseja visualizar?",
                [
                    "Ordem padrão",
                    "Ordem Alfabética (Nome)",
                    "Agrupado por Localização (Pallet)",
                ],
            )

            lista_exibicao = [dict(v) for v in st.session_state.estoque]

            if ordem == "Ordem Alfabética (Nome)":
                lista_exibicao.sort(
                    key=lambda x: str(x.get("nome", "")).lower()
                )
            elif ordem == "Agrupado por Localização (Pallet)":
                lista_exibicao.sort(
                    key=lambda x: str(x.get("pallet", "")).lower()
                )

            df = pd.DataFrame(lista_exibicao)
            colunas_map = {
                "nome": "Nome do Vinho",
                "tipo": "Tipo",
                "pallet": "Localização (Pallet)",
                "caixa": "Caixa",
                "volume": "Volume",
            }
            df.rename(columns=colunas_map, inplace=True)
            st.dataframe(df, use_container_width=True)

    # 4. EDITAR VINHO (CORRIGIDO)
    elif menu == "4. Editar vinho existente":
        st.header("✏️ EDITAR VINHO")

        if not st.session_state.estoque:
            st.warning("Nenhum vinho cadastrado.")
        else:
            opcoes = [
                f"{i + 1}. {v.get('nome', 'Sem nome')} - 📍 {v.get('pallet', 'Sem local')}"
                for i, v in enumerate(st.session_state.estoque)
            ]
            idx_selecionado = st.selectbox(
                "Selecione o vinho que deseja editar:",
                range(len(opcoes)),
                format_func=lambda x: opcoes[x],
            )

            vinho = st.session_state.estoque[idx_selecionado]

            with st.form("form_editar"):
                novo_nome = st.text_input(
                    "Novo Nome:", str(vinho.get("nome", ""))
                )
                novo_tipo = st.text_input(
                    "Novo Tipo:", str(vinho.get("tipo", ""))
                )
                novo_pallet = st.text_input(
                    "Nova Localização:", str(vinho.get("pallet", ""))
                )

                opcoes_caixa = [
                    "12 garrafas",
                    "6 garrafas",
                    "3 garrafas",
                    "1 garrafa",
                ]
                caixa_atual = vinho.get("caixa", "12 garrafas")
                idx_caixa = (
                    opcoes_caixa.index(caixa_atual)
                    if caixa_atual in opcoes_caixa
                    else 0
                )
                nova_caixa = st.selectbox(
                    "Caixa:", opcoes_caixa, index=idx_caixa
                )

                novo_volume = st.text_input(
                    "Volume:", str(vinho.get("volume", "750ml"))
                )

                submit_edit = st.form_submit_button("💾 Salvar Alterações")

                if submit_edit:
                    st.session_state.estoque[idx_selecionado] = {
                        "nome": novo_nome,
                        "tipo": novo_tipo,
                        "pallet": novo_pallet,
                        "caixa": nova_caixa,
                        "volume": novo_volume,
                    }
                    salvar_dados(st.session_state.estoque)
                    st.success(f"✅ '{novo_nome}' atualizado com sucesso!")
                    st.rerun()

    # 5. EXCLUIR VINHO (CORRIGIDO)
    elif menu == "5. Excluir vinho":
        st.header("🗑️ EXCLUIR VINHO")

        if not st.session_state.estoque:
            st.warning("Nenhum vinho cadastrado.")
        else:
            opcoes_excluir = [
                f"{i + 1}. {v.get('nome', 'Sem nome')} ({v.get('tipo', 'S/T')}) - 📍 {v.get('pallet', 'Sem local')}"
                for i, v in enumerate(st.session_state.estoque)
            ]

            idx_excluir = st.selectbox(
                "Selecione o vinho a remover:",
                range(len(opcoes_excluir)),
                format_func=lambda x: opcoes_excluir[x],
            )

            vinho_alvo = st.session_state.estoque[idx_excluir]

            if st.button("❌ Confirmar Exclusão"):
                nome_removido = vinho_alvo.get("nome", "Vinho")
                st.session_state.estoque.pop(idx_excluir)
                salvar_dados(st.session_state.estoque)
                st.success(f"✅ '{nome_removido}' excluído com sucesso!")
                st.rerun()

    # 6. EXPORTAR PLANILHA
    elif menu == "6. Exportar tabela para Excel (CSV)":
        st.header("📤 EXPORTAR PARA EXCEL (CSV)")

        if st.session_state.estoque:
            df = pd.DataFrame(st.session_state.estoque)
            csv_data = df.to_csv(index=False, sep=";").encode("utf-8-sig")

            st.download_button(
                label="📥 Baixar Planilha em Excel / CSV",
                data=csv_data,
                file_name="estoque_vinhos.csv",
                mime="text/csv",
            )
            st.info(
                "💡 Ao clicar no botão, o arquivo será salvo no seu dispositivo!"
            )
        else:
            st.warning("Nenhum dado para exportar.")
