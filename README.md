# api_veiculos
API que usa banco de dados para cadastrar e gerenciar os veículos da empresa.

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

### 2. Obter Todos os Veículos
- **Endpoint:** `/veiculos`
- **Método:** `GET`
- **Descrição:** Obtém todos os veículos cadastrados.
- **Autenticação: Necessário token JWT.
  
**Resposta de Sucesso:**
  ```json
 [
   {
     "id": 1,
     "veiculo": "Carro Exemplo",
     "status": "CONNECTED"
   }
]
