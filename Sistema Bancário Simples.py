# Importa o módulo textwrap para ajudar na formatação de textos longos.
import textwrap
# Importa as classes ABC e abstractmethod para criar classes e métodos abstratos.
from abc import ABC, abstractmethod
# Importa a classe datetime para registrar a data e hora das transações.
from datetime import datetime

# =================================================================================
# CLASSES DE TRANSAÇÃO E HISTÓRICO
# =================================================================================

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__.capitalize(),
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

# =================================================================================
# CLASSES DE CLIENTE - Só existe o cliente PessoaFisica. 
# =================================================================================

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return f"Nome: {self.nome} | CPF: {self.cpf}"

# =================================================================================
# CLASSES DE CONTA - ContaJuridica armazena CNPJ e Razão Social diretamente.
# =================================================================================

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente # O cliente será sempre um objeto PessoaFisica
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero, **kwargs):
        return cls(cliente=cliente, numero=numero, **kwargs)

    @property
    def saldo(self): return self._saldo
    @property
    def numero(self): return self._numero
    @property
    def agencia(self): return self._agencia
    @property
    def cliente(self): return self._cliente
    @property
    def historico(self): return self._historico
    # Propriedades para acessar limites (serão definidos nas classes filhas)
    @property
    def limite_valor_saque(self): return self._limite_valor_saque
    @property
    def limite_qtde_saques(self): return self._limite_qtde_saques

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n❌ Operação falhou! Saldo insuficiente.")
        elif valor <= 0:
            print("\n❌ Operação falhou! O valor informado é inválido.")
        else:
            self._saldo -= valor
            print("\n✅ Saque realizado com sucesso!")
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n✅ Depósito realizado com sucesso!")
            return True
        else:
            print("\n❌ Operação falhou! O valor informado é inválido.")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite_valor_saque = float(limite)
        self._limite_qtde_saques = int(limite_saques)

    def sacar(self, valor):
        numero_saques_realizados = len([
            t for t in self.historico.transacoes if t["tipo"] == "Saque"
        ])

        if valor > self._limite_valor_saque:
            print(f"\n❌ Falha no saque! Valor excede o limite da conta (R$ {self._limite_valor_saque:.2f}).")
        elif numero_saques_realizados >= self._limite_qtde_saques:
            print(f"\n❌ Falha no saque! Número máximo de saques ({self._limite_qtde_saques}) foi atingido.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""
          Agência: {self.agencia}
          C/C:     {self.numero}
          Titular: {self.cliente.nome}
          CPF:     {self.cliente.cpf}
        """

class ContaJuridica(ContaCorrente):
    # Herda de ContaCorrente, mas adiciona campos para CNPJ e Razão Social.
    def __init__(self, numero, cliente, razao_social, cnpj, limite=5000.0, limite_saques=10):
        # Chama o construtor da classe pai (ContaCorrente)
        super().__init__(numero, cliente, limite, limite_saques)
        self.razao_social = razao_social
        self.cnpj = cnpj

    def __str__(self):
        # Sobrescreve a representação para incluir os dados da empresa.
        return f"""
          Agência:      {self.agencia}
          C/C:          {self.numero} (Conta Empresarial)
          Empresa:      {self.razao_social}
          CNPJ:         {self.cnpj}
          Responsável:  {self.cliente.nome} (CPF: {self.cliente.cpf})
        """

# =================================================================================
# FUNÇÕES DE INTERAÇÃO COM O USUÁRIO 
# =================================================================================

def menu():
    #Exibe o menu principal e retorna a opção do usuário.
    menu_texto = """
        ══════════════════════════════════════════════════════════
                           💳 MENU PRINCIPAL 💳                    
        ══════════════════════════════════════════════════════════
                                                                  
          [nu] 👤 Criar novo usuário
          [nc] 🏦 Criar nova conta (Pessoal ou Empresarial)
          [d]  💰 Realizar depósito                                
          [s]  💸 Realizar saque                                   
          [e]  📋 Consultar extrato
          [lc] 🧾 Listar contas existentes
          [r]  👁️  Consultar regras da conta                              
          [x]  🚪 Sair do sistema               
                                                                  
        ══════════════════════════════════════════════════════════
    """
    return input(textwrap.dedent(menu_texto) + "\n        ➤ Escolha uma operação: ").lower()

def encontrar_cliente(cpf, clientes):
    # Função simplificada: busca um cliente na lista apenas pelo CPF.
    clientes_encontrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_encontrados[0] if clientes_encontrados else None

def selecionar_conta_cliente(cliente):
    # Gerencia a seleção de conta para um cliente.
    if not cliente.contas:
        print("\n❌ Cliente não possui conta cadastrada!")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    print("\nEste cliente possui múltiplas contas. Por favor, selecione uma:")
    for i, conta in enumerate(cliente.contas):
        # Mostra o tipo de conta para facilitar a identificação
        tipo = "Empresarial" if isinstance(conta, ContaJuridica) else "Pessoal"
        print(f"  [{i+1}] Conta número {conta.numero} ({tipo})")
    
    while True:
        try:
            escolha = int(input("  ➤ Digite o número da conta desejada: "))
            if 1 <= escolha <= len(cliente.contas):
                return cliente.contas[escolha - 1]
            else:
                print("❌ Opção inválida. Tente novamente.")
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número.")

def criar_usuario(clientes):
    # Função simplificada para criar apenas clientes PessoaFisica.
    cpf = input("Informe o CPF do novo usuário (somente números): ")
    if encontrar_cliente(cpf, clientes):
        print("\n❌ Operação falhou! Já existe um usuário com este CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")
    
    novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo_cliente)
    print("\n✅ Usuário criado com sucesso!")

def criar_conta(numero_conta_sequencial, clientes, contas):
    # Função refatorada para permitir a criação de conta Pessoal ou Empresarial.
    cpf = input("Informe o CPF do titular para vincular a nova conta: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado. Crie o usuário primeiro.")
        return

     # Aqui criamos o texto da pergunta em um formato mais legível.
    prompt_tipo_conta = """
    Qual tipo de conta você quer criar?
      [1] Pessoal (PF)
      [2] Empresarial (PJ)
    """
    # Usamos textwrap.dedent para remover a indentação e depois pedimos a entrada.
    tipo_conta = input(textwrap.dedent(prompt_tipo_conta) + "➤ Escolha uma opção: ")

    if tipo_conta == '1':
        print(f"\nCriando uma Conta Corrente Pessoal para: {cliente.nome}")
        limite_p, saques_p = 500, 3
        limite = input(f"Informe o limite por saque (padrão R$ {limite_p:.2f}): ") or limite_p
        limite_saques = input(f"Informe a quantidade de saques diários (padrão {saques_p}): ") or saques_p
        
        nova_conta = ContaCorrente(
            numero=numero_conta_sequencial, cliente=cliente, 
            limite=limite, limite_saques=limite_saques
        )

    elif tipo_conta == '2':
        print(f"\nCriando uma Conta Empresarial vinculada a: {cliente.nome}")
        razao_social = input("Informe a Razão Social da empresa: ")
        cnpj = input("Informe o CNPJ da empresa: ")
        
        limite_p, saques_p = 5000, 10
        limite = input(f"Informe o limite por saque (padrão R$ {limite_p:.2f}): ") or limite_p
        limite_saques = input(f"Informe a quantidade de saques diários (padrão {saques_p}): ") or saques_p

        nova_conta = ContaJuridica(
            numero=numero_conta_sequencial, cliente=cliente, 
            razao_social=razao_social, cnpj=cnpj, 
            limite=limite, limite_saques=limite_saques
        )
    else:
        print("\n❌ Opção de tipo de conta inválida. Operação cancelada.")
        return

    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta)
    print("\n✅ Conta criada com sucesso!")


def depositar_em_conta(clientes):
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = selecionar_conta_cliente(cliente)
    if not conta: return

    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        conta.depositar(valor)
    except ValueError:
        print("\n❌ Valor inválido. A operação foi cancelada.")

def sacar_de_conta(clientes):
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = selecionar_conta_cliente(cliente)
    if not conta: return

    try:
        valor = float(input("Informe o valor do saque: R$ "))
        conta.sacar(valor)
    except ValueError:
        print("\n❌ Valor inválido. A operação foi cancelada.")

def exibir_extrato_conta(clientes):
    # Exibe o extrato detalhado de uma conta específica.
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = selecionar_conta_cliente(cliente)
    if not conta: return
    
    
    # 1. Pega o texto bruto do __str__ da conta.
    header_bruto = str(conta)
    # 2. Remove a indentação original do __str__ para normalizá-lo.
    header_normalizado = textwrap.dedent(header_bruto).strip()
    # 3. Adiciona uma nova indentação de 10 espaços para alinhar com o resto do extrato.
    header_indentado = textwrap.indent(header_normalizado, "          ")

    extrato = f"""
        ══════════════════════════════════════════════════════════
                           📋 EXTRATO DA CONTA 📋                    
        ══════════════════════════════════════════════════════════
{header_indentado}
        ══════════════════════════════════════════════════════════
    """
    

    if not conta.historico.transacoes:
        extrato += "\n          Não foram realizadas movimentações.\n"
    else:
        for transacao in conta.historico.transacoes:
             # Formata o valor com vírgula para milhares e duas casas decimais.
            valor_formatado = f"R$ {transacao['valor']:,.2f}"
            descricao = f"{transacao['tipo']} ({transacao['data']})"
            
            # Alinha a descrição à esquerda (em 35 caracteres) e o valor à direita (em 20 caracteres)
            linha = f"{descricao:<35}{valor_formatado:>20}"
            extrato += f"\n          {linha}"
               
    # Aplica a MESMA lógica de formatação para o saldo, garantindo o alinhamento.
    saldo_formatado = f"R$ {conta.saldo:,.2f}"
    linha_saldo = f"{'SALDO ATUAL':<35}{saldo_formatado:>20}"

    extrato += f"""

          --------------------------------------------------------
          {linha_saldo}

        ══════════════════════════════════════════════════════════
    """
    
    print(textwrap.dedent(extrato))

def listar_contas(contas):
    # Lógica de filtro corrigida para usar o tipo de CONTA, não de cliente.
    print("\nQual tipo de conta deseja listar?")
    print("  [1] Contas Pessoais (PF)")
    print("  [2] Contas Empresariais (PJ)")
    print("  [3] Todas as Contas")
    opcao = input("  ➤ Escolha uma opção: ")

    if opcao == '1':
        # type(c) is ContaCorrente garante que pegamos apenas contas PF, e não suas subclasses.
        contas_filtradas = [c for c in contas if type(c) is ContaCorrente]
        titulo = "Contas Pessoais (PF)"
    elif opcao == '2':
        contas_filtradas = [c for c in contas if isinstance(c, ContaJuridica)]
        titulo = "Contas Empresariais (PJ)"
    elif opcao == '3':
        contas_filtradas = contas
        titulo = "Todas as Contas Cadastradas"
    else:
        print("\n❌ Opção inválida.")
        return
    
    # A função auxiliar corrigida fará todo o trabalho de formatação.
    _formatar_e_exibir_lista_contas(contas_filtradas, titulo)

def _formatar_e_exibir_lista_contas(lista_de_contas, titulo):
    # Função auxiliar interna para formatar e imprimir qualquer lista de contas.
    contas_formatado = f"""
        ══════════════════════════════════════════════════════════
                         🧾 {titulo.upper()} 🧾                   
        ══════════════════════════════════════════════════════════
    """
    if not lista_de_contas:
        contas_formatado += "\n          Nenhuma conta encontrada para este filtro.\n"
    else:
        for i, conta in enumerate(lista_de_contas):
            
            # 1. Pega o texto bruto do __str__ da conta.
            texto_bruto_conta = str(conta)
            # 2. Remove a indentação original e espaços em branco extras.
            texto_normalizado = textwrap.dedent(texto_bruto_conta).strip()
            # 3. Adiciona a nova indentação desejada para alinhar com o layout.
            texto_indentado = textwrap.indent(texto_normalizado, "          ")
            
            # Adiciona o bloco de texto formatado à string principal.
            contas_formatado += f"\n{texto_indentado}\n"
            

            if i < len(lista_de_contas) - 1:
                # O separador agora também é indentado para manter o padrão.
                contas_formatado += "          --------------------------------------\n"

    contas_formatado += "\n        ══════════════════════════════════════════════════════════\n"
    print(textwrap.dedent(contas_formatado))

def exibir_regras_conta(clientes):
    # Função refatorada para mostrar regras específicas de uma conta.
    print("\nPara qual conta você deseja ver as regras?")
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = selecionar_conta_cliente(cliente)
    if not conta: return

    tipo_conta_str = "Empresarial" if isinstance(conta, ContaJuridica) else "Pessoal"

    regras_texto = f"""
        ══════════════════════════════════════════════════════════
                     👁️ REGRAS DA CONTA Nº {conta.numero} ({tipo_conta_str}) 👁️                    
        ══════════════════════════════════════════════════════════
              #1 Titular: {conta.cliente.nome}
              #2 Limite por Saque: R$ {conta.limite_valor_saque:.2f}
              #3 Quantidade de Saques Diários: {conta.limite_qtde_saques}
        ══════════════════════════════════════════════════════════"""
    print(textwrap.dedent(regras_texto))

# =================================================================================
# FUNÇÃO PRINCIPAL (main) E EXECUÇÃO
# =================================================================================

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d": depositar_em_conta(clientes)
        elif opcao == "s": sacar_de_conta(clientes)
        elif opcao == "e": exibir_extrato_conta(clientes)
        elif opcao == "nu": criar_usuario(clientes)
        elif opcao == "nc": criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "lc": listar_contas(contas)
        elif opcao == "r": exibir_regras_conta(clientes) # Chamada para a nova função
        elif opcao == "x":
            print("\n👋 Saindo do sistema. Até logo!")
            break
        else:
            print("\n❌ Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
