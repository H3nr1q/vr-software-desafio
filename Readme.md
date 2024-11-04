# Desafio VR Software

Este projeto consiste em uma aplicação com um backend em Flask e um frontend em Vue.js, acompanhados de testes end-to-end (E2E) com Cypress. 

## Backend

O backend é desenvolvido utilizando Flask para a criação da API REST, com suporte para migrações de banco de dados com Flask-Migrate e serialização de dados com Marshmallow.

### Configuração do Ambiente

1. **Instale as dependências** do projeto:
  ```bash
   pip install -r requirements.txt
  ```

2. Execute as migrações para atualizar o banco de dados conforme o modelo já existente no repositório:

  ```bash
   flask db upgrade
  ```

3. Iniciar aplicação backend
  ```bash
   flask run
  ```

## Frontend
O frontend foi desenvolvido em Vue.js 2, utilizando as seguintes tecnologias:

* **Vue Router** para o gerenciamento de rotas
* **Axios** para as requisições HTTP
* **Bootstrap** para a estilização
* **Toast** para notificações ao usuário

Para executar o frontend, siga as instruções abaixo:

1. Instale as dependências do frontend:
  ```bash
   npm install
  ```

2. Inicir aplicação frontend
  ```bash
   npm run serve
  ```

## Testes End-To-End (E2E)

Os testes E2E foram desenvolvidos em Cypress, onde foi realizado um teste de integração para garantir:

* Sucesso na integração
* Verificação dos dados recebidos no corpo da resposta (body)

Para executar os testes E2E:

1. Instale as dependências do Cypress:
  ```bash
   npm install cypress
  ```

2. Execute os testes
  ```bash
   npx cypress open
  ```


