import csv
import json
import os
import sys

NOME_ARQUIVO = "estoque_vinhos.json"

estoque_padrao = [
    {"nome": "Quereu Rose 2024", "tipo": "Rose", "pallet": "Pallet 1", "caixa": "12 garrafas", "volume": "750ml"},
    {"nome": "Quereu Carmenere", "tipo": "Tinto", "pallet": "Pallet 2", "caixa": "6 garrafas", "volume": "750ml"},
    {"nome": "Quereu Chardonnay", "tipo": "Branco", "pallet": "Pallet 2", "caixa": "12 garrafas", "volume": "375ml"},
]


def carregar_dados():
    if os.path.exists(NOME_ARQUIVO):
        try:
            with open(NOME_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return estoque_padrao
    return estoque_padrao


def salvar_dados(estoque):
    try:
        with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(estoque, f, ensure_ascii=False, indent=4)
        print("💾 Alterações salvas no dispositivo!")
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")


def selecionar_caixa():
    print("\n📦 Qual a quantidade de garrafas por caixa?")
    print("1. Caixa c/ 12")
    print("2. Caixa c/ 6")
    print("3. Caixa c/ 3")
    print("4. Unidade (1 garrafa)")
    op = input("Opção (1-4): ").strip()

    mapeamento = {"1": "12 garrafas", "2": "6 garrafas", "3": "3 garrafas", "4": "1 garrafa"}
    return mapeamento.get(op, "12 garrafas")


def selecionar_volume():
    print("\n🧪 Qual o volume/tamanho da garrafa?")
    print("1. 750 ml (Padrão)")
    print("2. 375 ml (Meia garrafa)")
    print("3. 1500 ml / 1.5L (Magnum)")
    print("4. Outro valor")
    op = input("Opção (1-4): ").strip()

    if op == "1":
        return "750ml"
    elif op == "2":
        return "375ml"
    elif op == "3":
        return "1500ml (Magnum)"
    elif op == "4":
        custom = input("Digite o volume (ex: 187ml, 3000ml): ").strip()
        return custom if custom else "750ml"
    return "750ml"


def buscar_vinho(estoque_vinhos):
    print("\n--- 🔍 BUSCAR VINHO ---")
    print("1. Buscar por Nome")
    print("2. Buscar por Tipo")
    print("0. Voltar")

    sub_op = input("Escolha uma opção: ").strip()
    if sub_op == "0":
        return

    resultados = []
    if sub_op == "1":
        termo = input("\nDigite o nome do vinho: ").strip().lower()
        resultados = [v for v in estoque_vinhos if termo in v["nome"].lower()]
    elif sub_op == "2":
        termo = input("\nDigite o tipo (Tinto, Branco, Rosé...): ").strip().lower()
        resultados = [v for v in estoque_vinhos if termo in v["tipo"].lower()]
    else:
        print("\n❌ Opção inválida!")
        return

    if not resultados:
        print("\n⚠️ Nenhum vinho encontrado.")
        return

    print(f"\nEncontrado(s) {len(resultados)} resultado(s):")
    for idx, vinho in enumerate(resultados, 1):
        print(f"{idx}. {vinho['nome']} ({vinho['tipo']}) ➔ 📍 {vinho['pallet']}")

    escolha = input("\nDigite o número para ver detalhes (0 para voltar): ").strip()
    if escolha.isdigit():
        idx = int(escolha) - 1
        if 0 <= idx < len(resultados):
            v = resultados[idx]
            print(f"\n🍷 Nome: {v['nome']}")
            print(f"🍇 Tipo: {v['tipo']}")
            print(f"📍 Localização: {v['pallet']}")
            print(f"📦 Caixa: {v.get('caixa', 'N/I')}")
            print(f"🧪 Volume: {v.get('volume', 'N/I')}")


def cadastrar_vinho(estoque_vinhos):
    print("\n--- ➕ CADASTRAR VINHO ---")

    nome = input("Nome do vinho: ").strip()
    tipo = input("Tipo (Tinto, Branco, Rosé, Espumante...): ").strip()
    pallet = input("Localização (Ex: Pallet 1, Corredor B...): ").strip()

    if not (nome and tipo and pallet):
        print("\n❌ Nome, Tipo e Localização são obrigatórios!")
        return

    caixa = selecionar_caixa()
    volume = selecionar_volume()

    print("\n-----------------------------")
    print(f"🍷 Nome: {nome}")
    print(f"🍇 Tipo: {tipo}")
    print(f"📍 Localização: {pallet}")
    print(f"📦 Caixa: {caixa}")
    print(f"🧪 Volume: {volume}")
    print("-----------------------------")
    confirmar = input("Os dados estão corretos? (S/N): ").strip().upper()

    if confirmar == "S":
        novo_vinho = {
            "nome": nome,
            "tipo": tipo,
            "pallet": pallet,
            "caixa": caixa,
            "volume": volume
        }
        estoque_vinhos.append(novo_vinho)
        print(f"\n✅ '{nome}' cadastrado com sucesso!")
        salvar_dados(estoque_vinhos)
    else:
        print("\n❌ Cadastro cancelado!")


def editar_vinho(estoque_vinhos):
    print("\n--- ✏️ EDITAR VINHO ---")
    if not estoque_vinhos:
        print("Nenhum vinho cadastrado.")
        return

    for i, v in enumerate(estoque_vinhos, 1):
        print(f"{i}. {v['nome']} ➔ 📍 {v['pallet']}")

    escolha = input("\nDigite o número do vinho que deseja editar (0 para cancelar): ").strip()
    if escolha.isdigit():
        idx = int(escolha) - 1
        if 0 <= idx < len(estoque_vinhos):
            v = estoque_vinhos[idx]
            print(f"\nEditando '{v['nome']}'. Deixe em branco se NÃO quiser alterar o campo.")

            novo_nome = input(f"Novo Nome [{v['nome']}]: ").strip()
            novo_tipo = input(f"Novo Tipo [{v['tipo']}]: ").strip()
            novo_pallet = input(f"Nova Localização [{v['pallet']}]: ").strip()

            if novo_nome:
                v['nome'] = novo_nome
            if novo_tipo:
                v['tipo'] = novo_tipo
            if novo_pallet:
                v['pallet'] = novo_pallet

            mudar_caixa = input(f"Deseja alterar a caixa? Atual: {v.get('caixa', 'N/I')} (S/N): ").strip().upper()
            if mudar_caixa == "S":
                v['caixa'] = selecionar_caixa()

            mudar_vol = input(f"Deseja alterar o volume? Atual: {v.get('volume', 'N/I')} (S/N): ").strip().upper()
            if mudar_vol == "S":
                v['volume'] = selecionar_volume()

            print(f"\n✅ '{v['nome']}' atualizado com sucesso!")
            salvar_dados(estoque_vinhos)


def ver_todos_vinhos(estoque_vinhos):
    print("\n--- 🍷 TODOS OS VINHOS ---")
    if not estoque_vinhos:
        print("Nenhum vinho cadastrado.")
        return

    print("Como deseja visualizar?")
    print("1. Ordem padrão")
    print("2. Ordem Alfabética (Nome)")
    print("3. Agrupado por Localização (Pallet)")
    
    op = input("Opção (1-3): ").strip()

    lista_exibicao = list(estoque_vinhos)
    if op == "2":
        lista_exibicao.sort(key=lambda x: x["nome"].lower())
    elif op == "3":
        lista_exibicao.sort(key=lambda x: x["pallet"].lower())

    print("\n" + "=" * 50)
    for i, v in enumerate(lista_exibicao, 1):
        caixa_info = v.get('caixa', 'N/I')
        vol_info = v.get('volume', 'N/I')
        print(f"{i}. {v['nome']} ({v['tipo']})")
        print(f"   📍 {v['pallet']} | 📦 {caixa_info} | 🧪 {vol_info}")
        print("-" * 50)


def excluir_vinho(estoque_vinhos):
    print("\n--- 🗑️ EXCLUIR VINHO ---")
    if not estoque_vinhos:
        print("Nenhum vinho cadastrado.")
        return

    print("1. Excluir pelo NÚMERO da lista")
    print("2. Excluir pelo NOME")
    print("0. Cancelar")
    modo = input("Opção: ").strip()

    if modo == "1":
        for i, v in enumerate(estoque_vinhos, 1):
            print(f"{i}. {v['nome']} ({v['tipo']})")
        escolha = input("\nNúmero do vinho a excluir (0 para cancelar): ").strip()
        if escolha.isdigit():
            idx = int(escolha) - 1
            if 0 <= idx < len(estoque_vinhos):
                removido = estoque_vinhos.pop(idx)
                print(f"\n✅ '{removido['nome']}' excluído!")
                salvar_dados(estoque_vinhos)

    elif modo == "2":
        termo = input("\nDigite o nome a buscar: ").strip().lower()
        encontrados = [v for v in estoque_vinhos if termo in v["nome"].lower()]
        if not encontrados:
            print("\n⚠️ Nenhum vinho encontrado.")
            return

        for i, v in enumerate(encontrados, 1):
            print(f"{i}. {v['nome']} - {v['pallet']}")
        escolha = input("\nEscolha o número para excluir (0 para cancelar): ").strip()
        if escolha.isdigit():
            idx = int(escolha) - 1
            if 0 <= idx < len(encontrados):
                alvo = encontrados[idx]
                estoque_vinhos.remove(alvo)
                print(f"\n✅ '{alvo['nome']}' excluído!")
                salvar_dados(estoque_vinhos)


# FUNÇÃO DE EXPORTAR ATUALIZADA (SALVA EM DOWNLOADS)
def exportar_excel(estoque_vinhos):
    print("\n--- 📤 EXPORTAR PARA EXCEL/CSV ---")
    if not estoque_vinhos:
        print("Nenhum vinho para exportar.")
        return

    # Salva na pasta 'Download' do celular
    caminho_arquivo = "/sdcard/Download/estoque_vinhos.csv"

    try:
        with open(caminho_arquivo, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Nome do Vinho", "Tipo", "Localização (Pallet)", "Caixa", "Volume"])
            
            for v in estoque_vinhos:
                writer.writerow([
                    v.get("nome", ""),
                    v.get("tipo", ""),
                    v.get("pallet", ""),
                    v.get("caixa", "N/I"),
                    v.get("volume", "N/I")
                ])
        print("📊 Planilha gerada com sucesso!")
        print(f"📁 Arquivo salvo em: {caminho_arquivo}")
        print("💡 Abra a pasta 'Downloads' do celular para ver a planilha!")
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")


def menu_principal():
    estoque_vinhos = carregar_dados()

    while True:
        print("\n===================================")
        print("🍷 CONTROLE DE ESTOQUE DE VINHOS")
        print("1. Buscar vinho")
        print("2. Cadastrar novo vinho")
        print("3. Ver todos os vinhos (com Filtros)")
        print("4. Editar vinho existente")
        print("5. Excluir vinho")
        print("6. Exportar tabela para Excel (CSV)")
        print("7. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            buscar_vinho(estoque_vinhos)
        elif opcao == "2":
            cadastrar_vinho(estoque_vinhos)
        elif opcao == "3":
            ver_todos_vinhos(estoque_vinhos)
        elif opcao == "4":
            editar_vinho(estoque_vinhos)
        elif opcao == "5":
            excluir_vinho(estoque_vinhos)
        elif opcao == "6":
            exportar_excel(estoque_vinhos)
        elif opcao == "7":
            print("\nSaindo... Bom trabalho!")
            sys.exit()
        else:
            print("\n❌ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
