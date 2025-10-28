# 🍕 Sistema de E-commerce - Pizzaria Online

Este projeto foi desenvolvido como parte da disciplina de **Engenharia de Software**, com o objetivo de criar um sistema simples de e-commerce para uma pizzaria.

## 🧩 Tecnologias utilizadas
- **FastAPI** (backend)
- **Vercel** (hospedagem)
- **Python 3.10+**

## 🎯 Funcionalidades principais
- Cadastro e login de clientes
- Visualização do cardápio de pizzas
- Adição de pizzas ao carrinho
- Finalização de pedidos com escolha de forma de pagamento
- Acompanhamento de status dos pedidos

## 🏗️ Arquitetura do Backend

O sistema está organizado em módulos independentes, cada um responsável por uma parte específica da funcionalidade:

### 🔐 auth.py
- **Funcionalidades**:
  - Cadastro de novos usuários com validação de e-mail único
  - Login com autenticação segura
  - Retorno do ID do usuário para sessão

### 🏠 endereco.py
- **Funcionalidades**:
  - Consulta completa de endereços por ID de usuário
  - Retorno estruturado com:
    - CEP, logradouro, número
    - Complemento, bairro
    - Cidade/Estado

### 💰 pagamentos.py
- **Funcionalidades**:
  - Geração de QR Code PIX simulado
  - Vinculação ao ID do pedido

### 📦 pedido.py
- **Funcionalidades**:
  - Registro de novos pedidos
  - Consulta de histórico com:
    - Descrição detalhada dos itens
    - Datas formatadas no padrão brasileiro (DD/MM/YYYY)

### 🧠 recomendacao.py
- **Funcionalidades**:
  - Rede neural simples para sugestões personalizadas.
  - Recomenda até 2 pizzas não pedidas anteriormente
  - Considera frequência de pedidos passados
  - Retorna:
    - Pizzas recomendadas com preços
    - Lista completa de bebidas disponíveis
