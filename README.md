# Documentação da API de Veículos
Esta é uma API para gerenciamento de veículos, construída com Flask e Flask-RESTx. Ela permite a realização de operações CRUD (Criar, Ler, Atualizar e Deletar) em registros de veículos, além de suportar autenticação via JWT para proteger os endpoints.

## Instruções Adicionais
- **No arquivo Instrucoes_Adicionais.txt, tem algumas instruções de como criar o banco de dados, usuário utilizado e como popular as tabelas**
- **Existe também o arquivo test_api.py que testa os endpoints da API**

## Guia de Uso da API

## Endpoints

## Autenticação
A API utiliza autenticação via JWT (JSON Web Token). O token deve ser incluído no header da requisição no formato:

Authorization: Bearer <token>

## 1. Geração de Token
  - **Endpoint:** `/generate_token`
  - **Método:** `POST`
  - **Descrição:** Gera um token JWT.
  
  - **Parâmetros de Entrada:**
    - `MerchantId`: ID do Merchant (obrigatório)
    - `MerchantKey`: Chave do Merchant (obrigatório)
  
  - **Resposta de Sucesso:**
    - Código `200 OK`
    - Conteúdo: `{"token": "<JWT Token>"}`
  
  - **Respostas de Erro:**
    - 400 Bad Request: Quando MerchantId ou MerchantKey não são fornecidos.
    - 401 Unauthorized: Quando MerchantId ou MerchantKey são inválidos.
    - 500 Internal Server Error: Em caso de falha na geração do token.

## 2. Obter Todos os Veículos
  - **Endpoint:** `/veiculos`
  - **Método:** `GET`
  - **Descrição:** Obtém todos os veículos cadastrados.
  - **Autenticação:** Necessário token JWT.
  
  - **Resposta de Sucesso:**
    - Código `200 OK`
    - Conteúdo: Lista de veículos no formato:
    ```json
      [
        {
          "id": 1,
          "veiculo": "Carro Exemplo",
          "status": "CONNECTED"
        }
      ]
    ```
  - **Resposta de Erro:**
    - 401 Unauthorized: Token não fornecido ou inválido.
    - 400 Bad Request: Falha ao buscar os dados dos veículos.

## 3. Obter Veículo por ID
  - **Endpoint:** `/veiculos/<int:veiculo_id>`
  - **Método:** `GET`
  - **Descrição:** Obtém o veículo cadastrado pelo ID
  - **Autenticação:** Necessário token JWT.
  
  - **Parâmetros da URL:**
    - `veiculo_id`: ID do veículo (obrigatório)
  
  - **Resposta de Sucesso:**
    - Código `200 OK`
    - Conteúdo: Dados do veículo no formato:
    ```json
    [
      {
        "id": 1,
        "veículo": "Carro Exemplo",
        "status": "CONNECTED"
      }
    ]
    ```
  - **Resposta de Erro:**
    - 401 Unauthorized: Token não fornecido ou inválido.
    - 400 Bad Request: Falha ao buscar os dados dos veículos

## 4. Atualizar Status de Veículo
  - **Endpoint:** `/veiculos/UPDATE/<int:veiculo_id>/<int:novo_status>`
  - **Método:** `PUT`
  - **Descrição:** Atualiza o status do veículo cadastrado para 0 (DESCONECTADO) ou 1 (CONECTADO)
  - **Autenticação:** Necessário token JWT.
  
  - **Parâmetros da URL:**
    - `veiculo_id`: ID do veículo (obrigatório)
    - `novo_status`: NOvo status do veículo(0 ou 1)
  
  - **Resposta de Sucesso:**
    - Código `200 OK`
    - Conteúdo:
    ```json
    {
      "message": "Veículo atualizado com sucesso!"
    }
    ```
  - **Resposta de Erro:**
    - 401 Unauthorized: Token não fornecido ou inválido.
    - 404 Not Found: Veículo não encontrado.
    - 400 Bad Request: Status inválido

## 5. Deletar Veículo
  - **Endpoint:** `/veiculos/delete/<int:veiculo_id>`
  - **Método:** `DELETE`
  - **Descrição:** Apaga o veículo cadastrado pelo código informado.
  - **Autenticação:** Necessário token JWT.
  
  - **Parâmetros da URL:**
    - `veiculo_id`: ID do veículo (obrigatório)
  
  - **Resposta de Sucesso:**
    - Código `200 OK`
    - Conteúdo:
     ```json
       {
          "message": "Veículo deletado com sucesso"
       }
     ```
  - **Resposta de Erro:**
    - 401 Unauthorized: Token não fornecido ou inválido.
    - 404 Not Found: Veículo não encontrado.
    - 400 Bad Request: Falha ao deletar o veículo.


## 6. Adicionar Veículos
  - **Endpoint:** `/add_veiculos`
  - **Método:** `post`
  - **Descrição:** Adiciona um ou mais veículos.
  - **Autenticação:** Necessário token JWT.
  
  - **Parâmetros da URL:**
    - `veiculos`: Lista de veículos a serem adicionados (obrigatório)
  
  **Exemplo de Requisição:**
   ```json
     {
        "veiculos": ["Carro Exemplo 1", "Carro Exemplo 2"]
     }
   ```
  
  - **Resposta de Sucesso:**
    - Código `200 OK`
    - Conteúdo:
     ```json
      {
          "message": "Veículo(s) adicionado(s) com sucesso"
       }
    ```
  
  - **Resposta de Erro:**
    - 400 Bad Request: Falha ao adicionar o veículo.
    - 400 Bad Request: Entrada inválida.

---
# Modelos de Dados

## 1. Modelo de Veículo
- **Nome:** `Veiculos`
- **Estrutura:**
  - `veiculos` : Lista de strings representando os nomes dos veículos (obrigatório)

## 2. Modelo de Token
- **Nome:** `Veiculos`
- **Estrutura:**
  - MerchantId: ID do Merchant (obrigatório).
  - MerchantKey: Chave do Merchant (obrigatório).

---
## Banco de Dados
- **Nome:** `GerenciarVeiculos`
  - **Tabela:** `Veiculos`
    - **Colunas:**
      - `id`: Identificador único do veículo.
      - `veiculo`: Nome do veículo.
      - `status`: Status do veículo (CONNECTED ou DISCONNECTED).
   - **Descrição:**
     - Na tabela Veiculos ficará armazenado os dados de todos os veículos que forem cadastrados. Nesse modelo está sendo usando o banco de dados SQL Server
  
  - **Tabela:** `Merchants`
    - **Colunas:**
      - `id`: Identificador único da chave de acesso.
      - `MerchantId`: ID da chave de acesso.
      - `MerchantKey`: Chave de acesso.
   - **Descrição:**
     - Na tabela Merchants ficará armazenado as chaves de acesso para cada usuário, e que será necessário para gerar o Token.

