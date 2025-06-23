
import textwrap

def menu():
    #Exibe o menu principal e retorna a opção do usuário.
    
    menu_texto = """
        ══════════════════════════════════════════════════════════
                           💳 MENU PRINCIPAL 💳                    
        ══════════════════════════════════════════════════════════
                                                                  
          [d]  💰 Realizar depósito                                
          [s]  💸 Realizar saque                                   
          [e]  📋 Consultar extrato                                
          [nu] 👤 Criar novo usuário
          [nc] 🏦 Criar nova conta
          [lc] 🧾 Listar contas existentes
          [r]  👁️  Regras do Banco                              
          [x]  🚪 Sair do sistema               
                                                                  
        ══════════════════════════════════════════════════════════
    """
    return input(textwrap.dedent(menu_texto) + "\n        ➤ Escolha uma operação: ")

def depositar(saldo, valor, extrato, /):
    #Realiza um depósito e adiciona a transação à lista de extrato.

    if valor > 0:
        saldo += valor
        extrato.append(("Depósito", valor))  # Adiciona à lista
        print("\n✅ Depósito realizado com sucesso!")
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    #Realiza um saque, valida as regras e adiciona a transação à lista de extrato.

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n❌ Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\n❌ Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("\n❌ Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato.append(("Saque", -valor))  # Adiciona à lista (com valor negativo para clareza)
        numero_saques += 1
        print("\n✅ Saque realizado com sucesso!")
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

# ======== FUNÇÃO DE EXTRATO ATUALIZADA ========
def exibir_extrato(saldo, /, *, extrato):
    #Constrói o extrato como uma string única e a imprime com textwrap.dedent.

    # 1. Começamos a construir a string com o cabeçalho.
    #    A indentação aqui é proposital, pois dedent() a removerá.
    extrato_formatado = """
        ══════════════════════════════════════════════════════════
                           📋 EXTRATO DA CONTA 📋                    
        ══════════════════════════════════════════════════════════
    """

    # 2. Adicionamos o conteúdo do extrato à string.
    if not extrato:
        extrato_formatado += "\n          Não foram realizadas movimentações.\n"
    else:
        for tipo, valor in extrato:
            # Formata o valor e a linha, como antes
            valor_str = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            linha = f"{tipo:<25} {valor_str:>20}"
            # Adiciona a linha formatada e com margem à string principal
            extrato_formatado += f"\n          {linha}"

    # 3. Adicionamos o rodapé com o saldo à string. o X funciona como armazenamento temp do valor
    saldo_str = f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    linha_saldo = f"{'SALDO ATUAL':<25} {saldo_str:>20}"
    
    extrato_formatado += f"""

          --------------------------------------------------
          {linha_saldo}

        ══════════════════════════════════════════════════════════
    """

    # 4. Imprimimos a string completa de uma só vez, usando dedent.
    print(textwrap.dedent(extrato_formatado))
# =================================================================

def exibir_regras():
    #Exibe as regras do banco.

    regras_texto = """
        ══════════════════════════════════════════════════════════
                        👁️ REGRAS DO BANCO 👁️                    
        ══════════════════════════════════════════════════════════
              #1 O valor mínimo para depósito é R$ 1,00.
              #2 O limite para saques é R$ 500,00 por operação.
              #3 O número máximo de saques por dia é 3.
        ══════════════════════════════════════════════════════════"""
    print(textwrap.dedent(regras_texto))
# =================================================================


def criar_usuario(usuarios):
    #Cria um novo usuário (cliente) no sistema.

    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n❌ Operação falhou! Já existe usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n✅ Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    #Filtra e retorna um usuário pelo CPF, se existir.

    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    #Cria uma nova conta vinculada a um usuário.

    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n✅ Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n❌ Operação falhou! Usuário não encontrado.")
    return None

# ======== FUNÇÃO DE LISTAR CONTAS ATUALIZADA ========
def listar_contas(contas):
    #Constrói a lista de contas como uma string única e a imprime com textwrap.dedent.
    
    # 1. Inicia a string com o cabeçalho
    contas_formatado = """
        ══════════════════════════════════════════════════════════
                         🧾 CONTAS CADASTRADAS 🧾                   
        ══════════════════════════════════════════════════════════
    """

    # 2. Adiciona o conteúdo
    if not contas:
        contas_formatado += "\n          Nenhuma conta cadastrada no sistema.\n"
    else:
        for i, conta in enumerate(contas):
            # Adiciona o texto de cada conta à string principal
            contas_formatado += f"""
          Agência: {conta['agencia']}
          C/C:     {conta['numero_conta']}
          Titular: {conta['usuario']['nome']}"""
            
            # Adiciona um separador se não for a última conta
            if i < len(contas) - 1:
                contas_formatado += "\n          --------------------------------------"

    # 3. Adiciona o rodapé
    contas_formatado += """

        ══════════════════════════════════════════════════════════
    """

    # 4. Imprime tudo de uma vez
    print(textwrap.dedent(contas_formatado))
# ====================================================================

def main():
    #Função principal que executa o sistema bancário.

    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    numero_saques = 0
    
    # A variável 'extrato' agora é uma LISTA para permitir a formatação
    extrato = []
    
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == "r":
            exibir_regras()

        elif opcao == "x":
            print("\n👋 Saindo do sistema. Até logo!")
            break

        else:
            print("\n❌ Operação inválida, por favor selecione novamente a operação desejada.")

# Inicia o programa
main()
