# api_veiculos
API que usa banco de dados para cadastrar e gerenciar os veículos da empresa.

# Documentação da API de Veículos
## Descrição
Esta é uma API para gerenciamento de veículos, construída com Flask e Flask-RESTx. Ela permite a realização de operações CRUD (Criar, Ler, Atualizar e Deletar) em registros de veículos, além de suportar autenticação via JWT para proteger os endpoints.

# Endpoints

## 1. Geração de Token
Endpoint: /generate_token <br>
Método: POST <br>
Descrição: Gera um token JWT com base no MerchantId e MerchantKey fornecidos. <br>
**Parâmetros de Entrada:** <br>
-MerchantId: ID do Merchant (obrigatório) <br>
-MerchantKey: Chave do Merchant (obrigatório) <br>
Resposta de Sucesso:

# Guia de Uso da API

## Endpoints

### 1. Geração de Token
- **Endpoint:** `/generate_token`
- **Método:** `POST`
- **Descrição:** Gera um token JWT.

  > **Parâmetros de Entrada:**
  > - `MerchantId`: ID do Merchant (obrigatório)
  > - `MerchantKey`: Chave do Merchant (obrigatório)

  **Resposta de Sucesso:**
  ```json
  {
    "token": "<JWT Token>"
  }
