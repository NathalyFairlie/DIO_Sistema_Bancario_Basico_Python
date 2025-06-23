# Sistema Bancário Simples

# Menu de operações disponíveis
menu_operacoes = """
        ══════════════════════════════════════════════════════════
                           💳 MENU DA CONTA 💳                    
        ══════════════════════════════════════════════════════════
                                                                  
          [d] 💰 Realizar depósito                                
          [s] 💸 Realizar saque                                   
          [e] 📋 Consultar extrato                                                         
          [r] 👁️  Regras do Banco                              
          [x] 🚪 Logout (voltar ao menu principal)                
                                                                  
        ══════════════════════════════════════════════════════════
        
        ➤ Escolha uma operação: """

# Inicialização das variáveis
saldo = 0.0  # Saldo atual da conta
limite = 500.0  # Limite máximo para saques
extrato = ""  # Registro de movimentações
numero_saques = 0  # Contador de saques realizados
LIMITE_SAQUES = 3  # Limite máximo de saques permitidos

while True:
    opcao = input(menu_operacoes)

    # Operação de depósito
    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"           Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    # Operação de saque
    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        # Verificação das condições para saque
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        # Mensagens de erro para saques
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"           Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    # Operação de extrato
    elif opcao == "e":
        print("""
        ══════════════════════════════════════════════════════════
                           📋 EXTRATO DA CONTA 📋                    
        ══════════════════════════════════════════════════════════
        """)
        print("          Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\n           Saldo: R$ {saldo:.2f}")
        print("        ══════════════════════════════════════════════════════════")

    # Exibir regras do banco
    elif opcao == "r":
        print("""
        ══════════════════════════════════════════════════════════
                           👁️ REGRAS DO BANCO 👁️                    
        ══════════════════════════════════════════════════════════
              #1 O valor mínimo para depósito é R$ 1,00.
              #2 O limite para saques é R$ 500,00 por operação.
              #3 O número máximo de saques por dia é 3."
        ══════════════════════════════════════════════════════════""")


    # Sair do sistema
    elif opcao == "x":
        print("Saindo do sistema. Até logo!")
        break

    # Opção inválida
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")