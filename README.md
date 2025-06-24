 Sistema Bancário com Programação Orientada a Objetos

![Versão](https://img.shields.io/badge/versão-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.x-brightgreen)


Bem-vindo à versão 3.0 do Sistema Bancário! Este projeto foi refatorado para utilizar os princípios da **Programação Orientada a Objetos (POO)**, resultando em um código mais robusto, organizado e escalável. A aplicação simula as operações de um banco através de uma interface de linha de comando, gerenciando clientes e diferentes tipos de contas.

---

## ✨ Funcionalidades Principais

Este sistema vai além das operações básicas, oferecendo uma estrutura mais completa e realista:

*   **👤 Gestão de Clientes (Pessoa Física):**
    *   Cadastro de novos usuários (clientes) com nome, data de nascimento, CPF e endereço. O CPF é usado como identificador único.

*   **🏦 Criação de Contas Pessoais e Empresariais:**
    *   Um único cliente (Pessoa Física) pode abrir múltiplos tipos de conta.
    *   **Conta Pessoal (PF):** Uma conta corrente padrão para pessoas físicas.
    *   **Conta Empresarial (PJ):** Uma conta vinculada a um cliente PF responsável, contendo dados da empresa (CNPJ e Razão Social).

*   **⚙️ Regras de Negócio Personalizáveis:**
    *   Ao criar uma nova conta (PF ou PJ), o usuário pode definir o **limite de valor por saque** e a **quantidade de saques diários**.
    *   O sistema sugere valores padrão, que podem ser aceitos ou alterados.

*   **💸 Transações Bancárias:**
    *   **Depósito:** Adiciona valores a uma conta específica.
    *   **Saque:** Retira valores, respeitando o saldo, o limite por saque e a quantidade diária de saques da conta.

*   **🧾 Consultas Detalhadas:**
    *   **Extrato:** Exibe o histórico completo de transações (depósitos e saques) de uma conta selecionada, com cabeçalho formatado e saldo atual.
    *   **Listar Contas:** Permite visualizar todas as contas cadastradas, com a opção de filtrar por tipo (PF, PJ ou Todas).
    *   **Consultar Regras da Conta:** Mostra os limites personalizados (valor e quantidade de saques) de uma conta específica.

---

## 🚀 Tecnologias e Conceitos Utilizados

*   **Python 3:** Linguagem principal do projeto.
*   **Programação Orientada a Objetos (POO):**
    *   **Abstração:** Classes como `Conta` e `Transacao` definem contratos para outras classes mais específicas.
    *   **Encapsulamento:** Atributos importantes (como `_saldo`) são protegidos para evitar acesso direto.
    *   **Herança:** `ContaCorrente` herda de `Conta`, e `ContaJuridica` herda de `ContaCorrente`, reaproveitando e especializando o comportamento.
    *   **Polimorfismo:** Métodos como `__str__` e `sacar` se comportam de maneira diferente dependendo do tipo de conta.
*   **Módulos Nativos:**
    *   `textwrap`: Para formatação e alinhamento profissional dos textos exibidos no terminal.
    *   `datetime`: Para registrar a data e hora exatas de cada transação.
